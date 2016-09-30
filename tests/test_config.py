# -*- coding: utf-8 -*-

from .context import null

import unittest
import tempfile
import os


class ConfigTestSuite(unittest.TestCase):
    """Config test cases."""

    def setUp(self):
        # Create temporary good and bad config files
        try:
            os.remove(null.Default.GOOD_CONFIG)
            os.remove(null.Default.BAD_CONFIG)
        except:
            pass

        null.create_default_config(null.Default.GOOD_CONFIG)
        open(null.Default.BAD_CONFIG, 'wb').close()

        self.default = {'verbose': null.Default.VERBOSE,
                        'recursive': null.Default.RECURSIVE,
                        'null_char': null.Default.NULL_CHAR,
                        'category_1_name': null.Default.CAT_1_NAME,
                        'category_2_name': null.Default.CAT_2_NAME,
                        'category_3_name': null.Default.CAT_3_NAME,
                        'Categories': {
                            'cat1': null.Default.CAT_1,
                            'cat2': null.Default.CAT_2,
                            'cat3': null.Default.CAT_3
                            },
                        'start_directory': null.Default.START_DIRECTORY
                        # 'txt': {'cat1': 5, 'cat2': 20, 'cat3': 85}
                        }

    def tearDown(self):
        # Remove the config files after test
        os.remove(null.Default.GOOD_CONFIG)
        os.remove(null.Default.BAD_CONFIG)

    def test_Config_read_good(self):
        config_dict = null.read_config(null.Default.GOOD_CONFIG)
        self.assertEqual(self.default, config_dict)

    def test_Config_read_bad(self):
        config_dict = null.read_config(null.Default.BAD_CONFIG)
        self.assertEqual(self.default, config_dict)

if __name__ == '__main__':
    unittest.main()
