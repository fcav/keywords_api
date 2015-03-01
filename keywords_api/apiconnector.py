import pdb

import sys
import os
import csv
import argparse
from googleads.adwords import AdWordsClient
from keywords_api.config import SELECTOR, DATA_DIR, YAML_FILE



class ApiConnector(object):

    def getIdeaService(self):
        self.client = AdWordsClient.LoadFromStorage(path=YAML_FILE)
        self.service = self.client.GetService('TargetingIdeaService')
        return self.service


class IdeaSelector(object):

    def __init__(self, service, keywords):
        self.service = service
        self.keywords = keywords
    
    def _get_language(self, language):
        return 1000

    def buildSelector(self, keyword, language, results_per_request, location):
        pdb.set_trace()
        self.selector = SELECTOR
        language_code = str(self._get_language(language))
        keyword_param = {'xsi_type': 'RelatedToQuerySearchParameter', 'queries': [keyword]}
        language_param = {'xsi_type': 'LanguageSearchParameter','languages': [{'id': language_code}]}
        paging_param =  {'startIndex': '0','numberResults': str(results_per_request)}
        self.selector['searchParameters'] = [keyword_param, language_param]
        self.selector['localeCode'] = location
        self.selector['paging'] = paging_param

    def getIdeas(self):
        # this should return a dictionary of {[<original_keywords>]: [{'keyword': STRING, 'Rank': INT, 'SearchVolume': INT, 'AverageCPC': FLOAT, 'Competition': INT, DUPE: FLOAT}]}
        page = self.service.get(self.selector)
        ideas = page.entries
        clean_ideas = []
        for idea in ideas:
            clean_idea = {}
            for entry in idea.data:
                clean_idea[entry.key] = entry.value.value
        pdb.set_trace()
        return {self.keywords: 'test'}


class IdeasIterator():

    def __init__(self, results_per_request=10, iterations=5, language='English', location='UK'):
        self.results_per_request = results_per_request
        self.iterations = iterations
        self.language = language
        self.location = location
        self.output_path = DATA_DIR
        self.headers = None
        self.selector = None #ApiConnector().getIdeaService()

    def run(self, keywords):
        this_keywords = keywords
        for i in range(1, self.iterations+1):
            next_keywords = []
            for k in this_keywords:
                new_selector = IdeaSelector(self.selector, keywords)
                new_selector.buildSelector(k, self.language, self.results_per_request, self.location)
                this_ideas = new_selector.get_ideas()
                next_keywords += [x['keyword'] for x in this_ideas.values()]
                self.write_in_csv(this_ideas, i)
            this_keywords = next_keywords

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
    parser.add_argument("-r", "--results", default = 10, help="Number of results per iteration. If not given it will default to 10")
    parser.add_argument("-ln", "--language", default = 'English', help="Language. If not entered it will default to English")
    parser.add_argument("-lc", "--location", default = 'en_US', help="Location. If not entered it will default to UK")
    args = parser.parse_args()

    
    ideas = IdeasIterator(args.results, args.iterations, args.language, args.location)
    ideas.run(args.keywords)
