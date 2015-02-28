import apiconnector

#These will be in the function
page_size = 10

selector = {
    'searchParameters': [{
        'xsi_type': 'RelatedToQuerySearchParameter',
        #Variable input with function here
        'queries': ['jumper']
    },
    {
        #Language setting from variable here
        'xsi_type': 'LanguageSearchParameter',
        'languages': [{'id': '1000'}]
    }],
    'ideaType': 'KEYWORD',
    'requestType': 'IDEAS',
    'requestedAttributeTypes': ['KEYWORD_TEXT',
                                'SEARCH_VOLUME',
                                'AVERAGE_CPC',
                                'COMPETITION',],
    'paging': {'startIndex': '0',
               'numberResults': str(page_size)}
}

#Here be functions
page = targeting_idea_service.get(selector)
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

