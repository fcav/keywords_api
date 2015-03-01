import os
import sys

WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
YAML_FILE = os.path.join(WORKING_DIR, 'googleads.yaml')
DATA_DIR = os.path.join(WORKING_DIR, '..', 'data')
sys.path.append(WORKING_DIR)

SELECTOR = {
    'ideaType': 'KEYWORD',
    'requestType': 'IDEAS',
    'requestedAttributeTypes': ['KEYWORD_TEXT',
                                'SEARCH_VOLUME',
                                'AVERAGE_CPC',
                                'COMPETITION',],
}


LANGUAGE_SELECTOR = {
      'fields': ['Id', 'LocationName', 'DisplayType', 'CanonicalName',
                 'ParentLocations', 'Reach', 'TargetingStatus'],
      'predicates': [{
          'field': 'LocationName',
          'operator': 'IN',
          'values': ['Italy']
      }, {
          'field': 'Locale',
          'operator': 'EQUALS',
          'values': ['en']
      }]
  }
## lan : 1000
##