# -*- coding: utf-8 -*-

from .context import null

import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_absolute_truth_and_meaning(self):
        assert True

    def test_absolute_despair(self):
        assert False



if __name__ == '__main__':
    unittest.main()