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


LOCATION_SELECTOR = {
      'fields': ['Id', 'LocationName', 'DisplayType', 'CanonicalName',
                 'ParentLocations', 'Reach', 'TargetingStatus'],
      'predicates': [
      {
          'field': 'Locale',
          'operator': 'EQUALS',
          'values': ['en']
      }]
  }

LANGUAGE_SELECTOR = {
      'fields': ['Id', 'LocationName', 'DisplayType', 'CanonicalName',
                 'ParentLocations', 'Reach', 'TargetingStatus'],
      'predicates': [
      {
          'field': 'Locale',
          'operator': 'EQUALS',
          'values': ['en']
      }]
  }

LANGUAGE = {'Swedish': 1015, 'Icelandic': 1026, 'Estonian': 1043, 'Turkish': 1037, 'Romanian': 1032,
            'Serbian': 1035, 'Slovenian': 1034, 'Hindi': 1023, 'Dutch': 1010, 'Korean': 1012, 'Danish': 1009, 
            'Bulgarian': 1020, 'Vietnamese': 1040, 'Filipino': 1042, 'Hungarian': 1024, 'Ukrainian': 1036,
            'Lithuanian': 1029, 'Malay': 1102, 'French': 1002, 'Norwegian': 1013, 'Russian': 1031, 'Thai': 1044, 
            'Croatian': 1039, 'Finnish': 1011, 'Hebrew': 1027, 'Indonesian': 1025, 'Greek': 1022, 'Chinese ': 1018, 
            'Latvian': 1028, 'English': 1000, 'Chinese (simplified)': 1017, 'Catalan': 1038, 'Italian': 1004, 
            'Portuguese': 1014, 'German': 1001, 'Japanese': 1005, 'Czech': 1021, 'Persian': 1064, 'Slovak': 1033,
            'Spanish': 1003, 'Urdu': 1041, 'Polish': 1030, 'Arabic': 1019}