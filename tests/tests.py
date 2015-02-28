import pdb

import unittest
from keywords_api.apiconnector import ApiConnector, IdeaSelector
from keywords_api.config import SELECTOR

class TestApiConnector(unittest.TestCase):

    def setUp(self):
        pass

    def test_can_get_idea_service(self):
        try:
            con = ApiConnector()
            service = con.getIdeaService()
        finally:
            self.assertIsNotNone(service)

class TestIdeaSelector(unittest.TestCase):

    def setUp(self):
        self.selector = SELECTOR
        self.con = ApiConnector()
        self.service = self.con.getIdeaService()
        self.test_keywords = ['keywords', 'for', 'unittest']
        self.idea_selector = IdeaSelector(self.service, self.test_keywords)

    def test_getIdeas_returns_list_of_entries(self):
        self.idea_selector.buildSelector()
        page = self.service.get(self.idea_selector.selector)
        self.assertIsInstance(page.entries, list)

    def test_getIdeas_returns_number_of_entries_asked_for(self):
        self.idea_selector.buildSelector()
        page = self.service.get(self.idea_selector.selector)
        page_size_requested = self.idea_selector.selector['paging']['numberResults']
        self.assertEquals(len(page.entries), int(page_size_requested))

class TestIterator(unittest.TestCase):

    def setUp(self):
        pass

    def test_1s(self):
        pass

if __name__ == '__main__':
    api_con_suite = unittest.TestLoader().loadTestsFromTestCase(TestApiConnector)
    kw_sel_suite = unittest.TestLoader().loadTestsFromTestCase(TestKeywordSelector)

    unittest.TextTestRunner(verbosity=2).run(api_con_suite)
    unittest.TextTestRunner(verbosity=2).run(kw_sel_suite)
