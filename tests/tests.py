import pdb
import os
import unittest
from keywords_api.apiconnector import ApiConnector, IdeaSelector, IdeasIterator, LocationSelector, NonExistantCode
from keywords_api.config import SELECTOR
import csv
import mock

class TestApiConnector(unittest.TestCase):

    def test_can_get_idea_service(self):
        try:
            con = ApiConnector()
            service = con.getIdeaService()
        finally:
            self.assertIsNotNone(service)

class TestLocationSelector(unittest.TestCase):

    def setUp(self):
        self.selector = LocationSelector()

    def test_buildSelector_right_location(self):
        self.selector.buildselector('Italy')
        location_in_selector = [x['values'] for x in self.selector.selector['predicates']]
        self.assertIsInstance(self.selector.selector, dict)
        self.assertIn(['Italy'], location_in_selector)
        self.assertEqual(len(location_in_selector), 2)

    def test_getCode(self):
        uk_code = self.selector.get_code('UK')
        self.assertEqual(uk_code, 2826)
        self.assertRaises(NonExistantCode, self.selector.get_code,'not a place')

class TestIdeaSelector(unittest.TestCase):

    def setUp(self):
        self.con = ApiConnector()
        self.service = self.con.getIdeaService()
        self.test_keyword = 'keyword for unittest'
        self.idea_selector = IdeaSelector(self.service, self.test_keyword)
        self.idea_selector.buildSelector()
        self.ideas = self.idea_selector.getIdeas()


    def test_buildSelector_right_location(self):
        self.idea_selector.buildSelector(location='blah')
        location_in_selector = [x.get('locations', None) for x in self.idea_selector.selector['searchParameters']]
        self.assertIsInstance(self.idea_selector.selector, dict)
        self.assertIn([{'id': 'blah'}], location_in_selector)

    def test_getIdeas_returns_dict(self):
        self.assertIsInstance(self.ideas, dict)

    def test_getIdeas_returns_number_of_entries_asked_for(self):
        self.assertEquals(len(self.ideas[self.test_keyword]), self.idea_selector.page_size)

    def test_getIdeas_returns_required_attributes(self):
        requested_attrs = SELECTOR['requestedAttributeTypes']
        for idea in self.ideas[self.test_keyword]:
            # Assert list recieved and list requested are the same
            # RANK is derived (not requested) so we add that to request list for unittest
            self.assertItemsEqual(idea.keys(), requested_attrs+['RANK'])
        # Check that we get the number of results we wanted from API
        self.assertEquals(len(self.ideas[self.test_keyword]), self.idea_selector.page_size)

class TestIterator(unittest.TestCase):

    def setUp(self):
        self.test_ideas = {'keyword for unittest': [{'RANK': 1, 'AVERAGE_CPC': '3139613', 'SEARCH_VOLUME': '260', 'KEYWORD_TEXT': 'testing python', 'COMPETITION': '0.0361320208454'}, {'RANK': 2, 'AVERAGE_CPC': '1300835', 'SEARCH_VOLUME': '30', 'KEYWORD_TEXT': 'testing python code', 'COMPETITION': '0.0454545454545'}, {'RANK': 3, 'AVERAGE_CPC': None, 'SEARCH_VOLUME': '70', 'KEYWORD_TEXT': 'python test module', 'COMPETITION': '0.020979020979'}, {'RANK': 4, 'AVERAGE_CPC': '910906', 'SEARCH_VOLUME': '70', 'KEYWORD_TEXT': 'python test code', 'COMPETITION': '0.0314253647587'}, {'RANK': 5, 'AVERAGE_CPC': '2689673', 'SEARCH_VOLUME': '10', 'KEYWORD_TEXT': 'python class module', 'COMPETITION': '0.0179728317659'}, {'RANK': 6, 'AVERAGE_CPC': None, 'SEARCH_VOLUME': '30', 'KEYWORD_TEXT': 'python code test', 'COMPETITION': '0.0642424242424'}, {'RANK': 7, 'AVERAGE_CPC': None, 'SEARCH_VOLUME': '10', 'KEYWORD_TEXT': 'tests python', 'COMPETITION': '0.0136363636364'}, {'RANK': 8, 'AVERAGE_CPC': None, 'SEARCH_VOLUME': '20', 'KEYWORD_TEXT': 'what is function in python', 'COMPETITION': '0.0'}, {'RANK': 9, 'AVERAGE_CPC': None, 'SEARCH_VOLUME': '30', 'KEYWORD_TEXT': 'programming unit test', 'COMPETITION': '0.0534435261708'}, {'RANK': 10, 'AVERAGE_CPC': None, 'SEARCH_VOLUME': '10', 'KEYWORD_TEXT': 'python code testing', 'COMPETITION': '0.0661157024793'}]}
        self.test_keywords = ['keyword for unittest']
        #self.num_of_test_ideas = len(self.test_ideas['keyword for unittest'])
        self.test_headers = ['RANK', 'AVERAGE_CPC', 'SEARCH_VOLUME', 'KEYWORD_TEXT', 'COMPETITION', 'ITERATION', 'SEED_KEYWORD']
        self.iter = IdeasIterator(self.test_keywords, iterations=2)
        self.testfile = self.iter.output_file
        os.remove(self.testfile) if os.path.exists(self.testfile) else None

    def test_file_is_created(self):
        self.assertFalse(os.path.exists(self.testfile))
        self.iter.f = open(self.testfile, 'a')
        self.iter.append_to_csv(self.test_ideas, 1)
        self.assertTrue(os.path.exists(self.testfile))

    def test_run_calls_append_to_csv(self):
        self.iter.append_to_csv = mock.Mock()
        self.iter.run()
        # should be 11 calls, once for headers, once for every idea (10)
        self.assertEquals(self.iter.append_to_csv.call_count, 11)


if __name__ == '__main__':
    api_con_suite = unittest.TestLoader().loadTestsFromTestCase(TestApiConnector)
    kw_sel_suite = unittest.TestLoader().loadTestsFromTestCase(TestIdeaSelector)
    iter_suite = unittest.TestLoader().loadTestsFromTestCase(TestIterator)

    unittest.TextTestRunner(verbosity=2).run(api_con_suite)
    unittest.TextTestRunner(verbosity=2).run(kw_sel_suite)
    unittest.TextTestRunner(verbosity=2).run(iter_suite)
