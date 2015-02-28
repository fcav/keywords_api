from keywords_api.apiconnector import ApiConnector
import argparse
from config import SELECTOR


#Here be functions
page = targeting_idea_service.get(SELECTOR)
if 'entries' in page:
    for result in page['entries']:
        attributes = {}
        for attribute in result['data']:
            attributes[attribute['key']] = getattr(attribute['value'], 'value', '0')
        #print attributes.keys()
        #here be the writing section
        print '{0}\t{1}\t{2}\t{3}'.format(attributes['KEYWORD_TEXT'],
                                          attributes['SEARCH_VOLUME'],
                                          float(attributes['AVERAGE_CPC'].microAmount / 1000000),
                                          attributes['COMPETITION'])

