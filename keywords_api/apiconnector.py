import pdb

import csv
import argparse
from googleads.adwords import AdWordsClient
from keywords_api.config import SELECTOR, DATA_DIR, YAML_FILE



class ApiConnector(object):

    def __init__(self, service_name='TargetingIdeaService'):
        self.service_name = service_name

    def getIdeaService(self):
        self.client = AdWordsClient.LoadFromStorage(path=YAML_FILE)
        self.service = self.client.GetService(self.service_name)
        return self.service


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

    def buildSelector(self, language='English', location='en_US', page_size=10):
        self.page_size = page_size
        self.selector = SELECTOR
        language_code = str(self._get_language(language))
        keyword_param = {'xsi_type': 'RelatedToQuerySearchParameter', 'queries': [self.keyword]}
        language_param = {'xsi_type': 'LanguageSearchParameter','languages': [{'id': language_code}]}
        paging_param =  {'startIndex': '0','numberResults': str(page_size)}
        self.selector['searchParameters'] = [keyword_param, language_param]
        self.selector['localeCode'] = location
        self.selector['paging'] = paging_param

    def getIdeas(self):
        """
        returns a dictionary:
            {<original_keyword>: [{KEYWORD_TEXT: STRING,
                                   AVERAGE_CPC: STRING,
                                   SEARCH_VOLUME: STRING,
                                   COMPETITION: STRING,
                                   RANK: INT,
                                   }]
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
            clean_idea['RANK'] = ideas.index(idea)
            clean_ideas.append(clean_idea)
        return {self.keyword: clean_ideas}


class IdeasIterator():

    def __init__(self, page_size=10, iterations=5, language='English', location='UK'):
        self.page_size = page_size
        self.iterations = iterations
        self.language = language
        self.location = location
        self.output_path = DATA_DIR
        self.headers = None
        self.selector = None #ApiConnector().getIdeaService()

    def run(self, keyword_list):
        this_keyword_list = keyword_list
        for i in range(1, self.iterations+1):
            next_keyword_list = []
            for k in this_keyword_list:
                new_selector = IdeaSelector(self.selector, k)
                new_selector.buildSelector(self.language, self.location, self.page_size)
                this_ideas = new_selector.get_ideas()
                next_keyword_list += [x['keyword'] for x in this_ideas.values()]
                self.write_in_csv(this_ideas, i)
            this_keyword_list = next_keyword_list

    def write_in_csv(self, res_dic, iteration):
        if not self.headers:
            self.headers = ['Iteration', 'SeedKeyword']
            self.headers += res_dic.keys()
            with open('names.csv', 'w') as csvfile:
                pass

if __name__ == '__main__':

    #arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', "--keywords", help="The keywords you want to start with", nargs='+')
    parser.add_argument('-i', "--iterations", default = 5, help="Number of iteration. If not given it will defaults to 5")
    parser.add_argument("-r", "--page_size", default = 10, help="Number of results per iteration. If not given it will default to 10")
    parser.add_argument("-ln", "--language", default = 'English', help="Language. If not entered it will default to English")
    parser.add_argument("-lc", "--location", default = 'en_US', help="Location. If not entered it will default to UK")
    args = parser.parse_args()


    ideas = IdeasIterator(args.page_size, args.iterations, args.language, args.location)
    ideas.run(args.keywords)
