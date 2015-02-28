import sys

working_dir = '/Users/youcefkadri/Downloads/googleads-python-lib-master/'
yaml_file = working_dir + 'googleads.yaml'

sys.path.append(working_dir)
from googleads.adwords import AdWordsClient

client = AdWordsClient.LoadFromStorage(path=yaml_file)
targeting_idea_service = client.GetService('TargetingIdeaService')
