import sys
from googleads.adwords import AdWordsClient

WORKING_DIR = '/home/seanblumenfeld/projects/keywords_api/bin/'
YAML_FILE = WORKING_DIR + 'googleads.yaml'
sys.path.append(WORKING_DIR)

client = AdWordsClient.LoadFromStorage(path=yaml_file)
targeting_idea_service = client.GetService('TargetingIdeaService')
