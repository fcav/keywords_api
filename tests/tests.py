import pdb

import unittest
from keywords_api.apiconnector import ApiConnector


class TestApiConnector(unittest.TestCase):

    def setUp(self):
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

    def test_can_get_idea_service(self):
        try:
            con = ApiConnector()
            service = con.getIdeaService
        finally:
            self.assertIsNotNone(service)


class TestKeywordSelector(unittest.TestCase):

    def setUp(self):
        pass

    def test_1s(self):
        pass

if __name__ == '__main__':
    api_con_suite = unittest.TestLoader().loadTestsFromTestCase(TestApiConnector)
    kw_sel_suite = unittest.TestLoader().loadTestsFromTestCase(TestKeywordSelector)

    unittest.TextTestRunner(verbosity=2).run(api_con_suite)
    unittest.TextTestRunner(verbosity=2).run(kw_sel_suite)
