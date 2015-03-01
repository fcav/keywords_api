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
        self.con = ApiConnector()
        self.service = self.con.getIdeaService()
        self.test_keyword = 'keyword for unittest'
        self.idea_selector = IdeaSelector(self.service, self.test_keyword)
        self.idea_selector.buildSelector()
        self.ideas = self.idea_selector.getIdeas()

    def test_getIdeas_returns_dict(self):
        self.assertIsInstance(self.ideas, dict)

    def test_getIdeas_returns_number_of_entries_asked_for(self):
        self.assertEquals(len(self.ideas[self.test_keyword]), PAGE_SIZE)

    def test_getIdeas_returns_required_attributes(self):
        requested_attrs = SELECTOR['requestedAttributeTypes']
        for idea in self.ideas[self.test_keyword]:
            # Assert list recieved and list requested are the same
            # RANK is derived (not requested) so we add that to request list for unittest
            self.assertItemsEqual(idea.keys(), requested_attrs+['RANK'])
        # Check that we get the number of results we wanted from API
        self.assertEquals(len(self.ideas[self.test_keyword]), PAGE_SIZE)

class TestIterator(unittest.TestCase):

    def setUp(self):
        pass

    def test_1s(self):
        pass

if __name__ == '__main__':
    api_con_suite = unittest.TestLoader().loadTestsFromTestCase(TestApiConnector)
    kw_sel_suite = unittest.TestLoader().loadTestsFromTestCase(TestIdeaSelector)
    iter_suite = unittest.TestLoader().loadTestsFromTestCase(TestIterator)

    unittest.TextTestRunner(verbosity=2).run(api_con_suite)
    unittest.TextTestRunner(verbosity=2).run(kw_sel_suite)
    unittest.TextTestRunner(verbosity=2).run(iter_suite)
