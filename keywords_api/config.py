#These will be in the function
PAGE_SIZE = 10

SELECTOR = {
    'searchParameters': [
    {'xsi_type': 'RelatedToQuerySearchParameter', 'queries': ['jumper']},
    {'xsi_type': 'LanguageSearchParameter','languages': [{'id': '1000'}]}],
    'ideaType': 'KEYWORD',
    'requestType': 'IDEAS',
    'requestedAttributeTypes': ['KEYWORD_TEXT',
                                'SEARCH_VOLUME',
                                'AVERAGE_CPC',
                                'COMPETITION',],
    'paging': {'startIndex': '0',
               'numberResults': str(PAGE_SIZE)}
}
