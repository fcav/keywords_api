import sys
from googleads.adwords import AdWordsClient

WORKING_DIR = '/home/seanblumenfeld/projects/keywords_api/bin/'
YAML_FILE = WORKING_DIR + 'googleads.yaml'
sys.path.append(WORKING_DIR)

class ApiConnector(object):

    def getIdeaService(self):
        client = AdWordsClient.LoadFromStorage(path=YAML_FILE)
        service = client.GetService('TargetingIdeaService')
        return service

