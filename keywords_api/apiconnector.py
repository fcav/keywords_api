import pdb
import os
import csv
import time
import argparse
import sys
import datetime
from googleads.adwords import AdWordsClient
from keywords_api.config import SELECTOR, DATA_DIR, YAML_FILE, LANGUAGE, LOCATION_SELECTOR
import threading

class NonExistantCode(Exception):
    pass

class ApiConnector(object):
    def __init__(self, service_name='TargetingIdeaService'):
        self.service_name = service_name

    def getIdeaService(self):
        self.client = AdWordsClient.LoadFromStorage(path=YAML_FILE)
        self.service = self.client.GetService(self.service_name)
        return self.service

class LanguageSelector():

    def __init__(self):
        self.service = ApiConnector('ConstantDataService').getIdeaService()

    def get_code(self):
        languages = self.service.getLanguageCriterion()
        if not languages:
            raise
        return languages

class LocationSelector():

    def __init__(self):
        self.service = ApiConnector('LocationCriterionService').getIdeaService()

    def buildselector(self, location):
        self.selector = LOCATION_SELECTOR
        location_param = {'field': 'LocationName', 'operator': 'IN','values': [location]}
        self.selector['predicates'].append(location_param)

    def get_code(self, location):
        self.buildselector(location)
        a = self.service.get(self.selector)
        if not a:
            raise NonExistantCode('The location that you have given does not exist')
        return [x.location.id for x in a][0]


class IdeaSelector(object):

    def __init__(self, service, keyword):
        self.service = service
        self.page_size = None
        if isinstance(keyword, str):
            self.keyword = keyword
        else:
            raise TypeError('keyword must be a string')

    def buildSelector(self, language='1000', location='2826', page_size=10):
        self.page_size = page_size
        self.selector = SELECTOR
        keyword_param = {'xsi_type': 'RelatedToQuerySearchParameter', 'queries': [self.keyword]}
        language_param = {'xsi_type': 'LanguageSearchParameter','languages': [{'id': language}]}
        location_param = {'xsi_type': 'LocationSearchParameter','locations': [{'id': location}]}
        paging_param =  {'startIndex': '0','numberResults': str(page_size)}
        self.selector['searchParameters'] = [keyword_param, location_param, language_param]
        self.selector['paging'] = paging_param

    def getIdeas(self):
        """
        returns a dictionary where:
            key: seed keyword
            value: list of keyword ideas
            {<original_keyword>: [{[KEYWORD_TEXT]: STRING,
                                   AVERAGE_CPC: REAL
                                   COMPETITION: STRING,
                                   RANK: INT`,
                                   },
                                   ...]
            }
        """
        page = self.service.get(self.selector)
        clean_ideas = []
        try:
            ideas = page.entries
        except AttributeError:
             ideas = []
        for idea in ideas:
            clean_idea = {}
            for entry in idea.data:
                if entry.key == "AVERAGE_CPC":
                    try:
                        clean_idea[str(entry.key)] = entry.value.value.microAmount/1000000
                    except AttributeError:
                        clean_idea[str(entry.key)] = None
                else:
                    try:
                        clean_idea[str(entry.key)] = str(entry.value.value)
                    except AttributeError:
                        clean_idea[str(entry.key)] = None
            clean_idea['RANK'] = ideas.index(idea)+1
            clean_ideas.append(clean_idea)
        return {self.keyword: clean_ideas}


class IdeasIterator():

    def __init__(self, seed_keywords, page_size=10, iterations=5, language='1000', location='2826', output_file = 'output.csv'):
        self.seed_keywords = seed_keywords
        self.page_size = page_size
        self.iterations = iterations
        self.language = language
        self.location = location
        self.headers = None
        self.service = ApiConnector().getIdeaService()
        now = datetime.datetime.utcnow()
        time = str(now)[:19].replace(' ', '_')
        self.output_file = os.path.join(DATA_DIR, time + '_' +output_file)
        self.all_ideas = []

    def worker(self, keyword, i):
        max_tries = 5
        ideas = None
        for x in range(max_tries):
            try:
                selector = IdeaSelector(self.service, keyword)
                selector.buildSelector(self.language, self.location, self.page_size)
                ideas = selector.getIdeas()
                break
            except:
                time.sleep(min(i*i*5, 60))
        if not ideas:
            print('Warning - API Call rate exceeded 1 set of ideas could not be retrieved: keyord {0}.'.format(keyword))
            print('          Continuing with other ideas.')
            print('          Output file will be reduced.')
            exit(1)
        for idea in ideas[keyword]:
            self.next_seed_keywords.append(idea['KEYWORD_TEXT'])
            self.append_to_csv(ideas, i)

    def run(self):
        self.f = open(self.output_file, 'a')
        for i in range(1, self.iterations+1):
            print("Iteration #{0}".format(i))
            self.all_ideas = []
            threads = []
            self.next_seed_keywords = []
            for keyword in self.seed_keywords:
                t = threading.Thread(name=keyword, target=self.worker, args=(keyword,i,))
                threads.append(t)

            [x.start() for x in threads]
            [x.join() for x in threads]

            self.seed_keywords = self.next_seed_keywords
        self.f.close()


    def append_to_csv(self, ideas, iteration):
        """
        Append a "seed_keyword dictionary" to a csv file
        """
        if not self.headers:
            self.headers = ['ITERATION', 'SEED_KEYWORD', 'RANK']
            self.headers += SELECTOR['requestedAttributeTypes']
            self.writer = csv.DictWriter(self.f, fieldnames=self.headers, restval="ERROR")
            self.writer.writeheader()
        for seed_keyword in ideas:
            rows_to_write = ideas[seed_keyword]
            for i in range(len(rows_to_write)):
                rows_to_write[i].update({'ITERATION': iteration})
                rows_to_write[i].update({'SEED_KEYWORD': seed_keyword})
            self.writer.writerows(rows_to_write)


if __name__ == '__main__':

    #arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', "--keywords", help="Seed keywords - format: -k 'keyword1' 'keyword2' 'keyword3'", nargs='+', type=str, required=True)
    parser.add_argument('-i', "--iterations", default = 5, help="Number of iterations; default = 5", type=int)
    parser.add_argument("-r", "--page_size", default = 10, help="Number of results per iteration; default = 10")
    parser.add_argument("-ln", "--language", default = 'English', choices = LANGUAGE.keys() + ['list'], help="Language; default = English")
    parser.add_argument("-lc", "--location", default = 'UK',  help="Location; default = UK. To list the choices type: -ln list")
    xargs = parser.parse_args()


    if xargs.language == 'list':
        print LANGUAGE.keys()
        sys.exit()

    locationcode = LocationSelector().get_code(xargs.location)
    languagecode = str(LANGUAGE[xargs.language])

    ideas = IdeasIterator(xargs.keywords, xargs.page_size, xargs.iterations, languagecode, locationcode)

    ideas.run()
