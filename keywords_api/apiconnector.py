import pdb

import sys
import os
import argparse
from googleads.adwords import AdWordsClient
from keywords_api.config import SELECTOR


WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
YAML_FILE = WORKING_DIR + '/googleads.yaml'
sys.path.append(WORKING_DIR)


class ApiConnector(object):

    def getIdeaService(self):
        self.client = AdWordsClient.LoadFromStorage(path=YAML_FILE)
        self.service = self.client.GetService('TargetingIdeaService')
        return self.service


class IdeaSelector(object):

    def __init__(self, service, keywords):
        self.service = service
        self.keywords = keywords

    def buildSelector(self, keyword):
        pass

    def getIdeas(self, selector, keywords, iterations):
        # this should return a dictionary of {<original_keyword>: {'keyword': STRING, 'Rank': INT, 'SearchVolume': INT, 'AverageCPC': FLOAT, 'Competition': INT, DUPE: FLOAT}
        pass


class IdeasIterator():

    def __init__(self, results_per_request=10, iterations=5, language='English', location='UK'):
        self.results_per_request = results_per_request
        self.iterations = iterations
        self.language = language
        self.localaion = location
        self.output_path = ''


    def run(self, keywords):
        next_keywords = [keywords]
        for i in range(1, self.iterations+1):
            new_selector = ApiConnector()
            new_selector.instantiateService(self.language, self.location)
            this_ideas = new_selector.get_ideas(keywords, self.iterations)
            next_keywords = [x['keyword'] for x in this_ideas.values()]
            self.write_in_csv(this_ideas, i)

    def write_in_csv(self, res_dic, iteration):
        pass



if __name__ == '__main__':

    #arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', "--keyword", help="The keyword you want to start with")
    parser.add_argument('-i', "--iterations", default = 5, help="Number of iteration. If not given it will defaults to 5")
    parser.add_argument("--r", "--results", defaukt = 10, help="Number of results per iteration. If not given it will default to 10")
    parser.add_argument("--ln", "--language", default = 'English', help="Language. If not entered it will default to English")
    parser.add_argument("--lc", "--location", default = 'UK', help="Location. If not entered it will default to UK")
    args = parser.parse_args()

    ideas = IdeasIterator(args.results, args.iterations, args.language, args.localtion)
    ideas.run(args.keyword)
