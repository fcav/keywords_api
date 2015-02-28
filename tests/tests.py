import pdb

import unittest
from keywords_api.apiconnector import ApiConnector
from keywords_api.config import SELECTOR

class TestApiConnector(unittest.TestCase):

    def setUp(self):
        self.selector = SELECTOR
        self.con = ApiConnector()
        self.service = self.con.getIdeaService()

    def test_can_get_idea_service(self):
        try:
            con = ApiConnector()
            service = con.getIdeaService()
        finally:
            self.assertIsNotNone(service)

    def test_getIdeas_returns_dict(self):
        test_keywords = ['keywords', 'for', 'unittest']
        self.con.getIdeaService()
        test_page = self.service.get(self.selector)
        pdb.set_trace()
        #self.assertIsInstance(self.con.getIdeas(test_keywords, 1), dict)


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
