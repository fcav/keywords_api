import sys
import os
from googleads.adwords import AdWordsClient

WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
YAML_FILE = WORKING_DIR + 'googleads.yaml'
sys.path.append(WORKING_DIR)

class ApiConnector(object):

    def getIdeaService(self):
        client = AdWordsClient.LoadFromStorage(path=YAML_FILE)
        service = client.GetService('TargetingIdeaService')
        return service

