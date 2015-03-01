import pdb

import csv
import argparse
import sys
from googleads.adwords import AdWordsClient
from keywords_api.config import SELECTOR, DATA_DIR, YAML_FILE, LANGUAGE, LOCATION_SELECTOR



class ApiConnector(object):

    def __init__(self, service_name='TargetingIdeaService'):
        self.service_name = service_name

    def getIdeaService(self):
        self.client = AdWordsClient.LoadFromStorage(path=YAML_FILE)
        self.service = self.client.GetService(self.service_name)
        return self.service

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
            raise
        return [x.location.id for x in a][0]




class IdeaSelector(object):

    def __init__(self, service, keyword):
        self.service = service
        self.page_size = None
        if isinstance(keyword, str):
            self.keyword = keyword
        else:
            raise TypeError('keyword must be a string')

    def _get_language(self, language):
        return 1000

    def buildSelector(self, language='en_US', location=2826, page_size=10):
        self.page_size = page_size
        self.selector = SELECTOR
        keyword_param = {'xsi_type': 'RelatedToQuerySearchParameter', 'queries': [self.keyword]}
        language_param = {'xsi_type': 'LanguageSearchParameter','languages': [{'id': language}]}
        location_param = {'xsi_type': 'LocationSearchParameter','locations': [{'id': location}]}
        paging_param =  {'startIndex': '0','numberResults': str(page_size)}
        self.selector['searchParameters'] = [keyword_param, location_param]
        self.selector['localeCode'] = language
        self.selector['paging'] = paging_param

    def getIdeas(self):
        """
        returns a dictionary where:
            key: seed keyword
            value: list of keyword ideas
            {<original_keyword>: [{KEYWORD_TEXT: STRING,
                                   AVERAGE_CPC: STRING,
                                   SEARCH_VOLUME: STRING,
                                   COMPETITION: STRING,
                                   RANK: INT,
                                   },
                                   ...]
            }
        """
        page = self.service.get(self.selector)
        ideas = page.entries
        clean_ideas = []
        for idea in ideas:
            clean_idea = {}
            for entry in idea.data:
                if entry.key == "AVERAGE_CPC":
                    try:
                        clean_idea[str(entry.key)] = str(entry.value.value.microAmount)
                    except AttributeError:
                        clean_idea[str(entry.key)] = None
                else:
                    clean_idea[str(entry.key)] = str(entry.value.value)
            clean_idea['RANK'] = ideas.index(idea)+1
            clean_ideas.append(clean_idea)
        return {self.keyword: clean_ideas}


class IdeasIterator():

    def __init__(self, seed_keywords, page_size=10, iterations=5, language='English', location='UK', output_file = 'output.csv'):
        self.seed_keywords = seed_keywords
        self.page_size = page_size
        self.iterations = iterations
        self.language = language
        self.location = location
        self.output_file = os.path.join(DATA_DIR, output_file)
        self.headers = None
        self.service = ApiConnector().getIdeaService()

    def run(self):
        for i in range(1, self.iterations+1):
            next_keywords = []
            for keyword in self.seed_keywords:
                selector = IdeaSelector(self.service, keyword)
                selector.buildSelector(self.language, self.location, self.page_size)
                ideas = selector.getIdeas()
                self.append_to_csv(ideas, i)


    def append_to_csv(self, iteration):
        """
        Append an "seed_keyword dictionary" to a csv file
        """
        for seed_keyword in self.seed_keywords:
            rows_to_write = self.seed_keywords[seed_keyword]
            for row in rows_to_write:
                rows_to_write[row]['ITERATION'] = iteration
                rows_to_write[row]['SEED_KEYWORD'] = seed_keyword
            if not self.headers:
                self.headers = ['ITERATION', 'SEED_KEYWORD', 'RANK']
                self.headers += SELECTOR['requestedAttributeTypes']
            with open(self.output_file, 'w') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers, restval="ERROR")
                writer.writeheader()
                writer.writerows(rows_to_write)

if __name__ == '__main__':

    #arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', "--keywords", help="The keywords you want to start with", nargs='+')
    parser.add_argument('-i', "--iterations", default = 5, help="Number of iteration. If not given it will defaults to 5")
    parser.add_argument("-r", "--page_size", default = 10, help="Number of results per iteration. If not given it will default to 10")
    parser.add_argument("-ln", "--language", default = 'en_US', choices = LANGUAGE.keys() + ['list'], help="Language. TIf not entered it will default to English")
    parser.add_argument("-lc", "--location", default = 'UK',  help="Location. If not entered it will defaulo see teh choices, type: -ln list. t to UK")
    args = parser.parse_args()

    if args.language == 'list':
        for k,w in LANGUAGE.iteritems():
            print k + ' : ' + w
        sys.exit()

    locationcode = LocationSelector().get_code(args.location)
    pdb.set_trace()
    ideas = IdeasIterator(args.page_size, args.iterations, args.language, locationcode, args.keywords)
    ideas.run(args.keywords)
