import pdb

import unittest
from apiconnector import ApiConnector

class TestApiConnector(unittest.TestCase):

    def setUp(self):
        pass

    def test_return_status_is_200(self):
        con = ApiConnector()
        service = con.getIdeaService


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
