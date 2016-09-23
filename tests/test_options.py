# -*- coding: utf-8 -*-

from .context import null

import unittest
from contextlib import contextmanager
from StringIO import StringIO
import sys

# from StackOverflow
# http://stackoverflow.com/questions/18651705/argparse-unit-tests-suppress-the-help-message


@contextmanager
def capture_sys_output():
    capture_out, capture_err = StringIO(), StringIO()
    current_out, current_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = capture_out, capture_err
        yield capture_out, capture_err
    finally:
        sys.stdout, sys.stderr = current_out, current_err


class OptionsTestSuite(unittest.TestCase):
    """Command line option test cases."""

    # ----------------------------------------------------

    def test_Option_categories_valid(self):
        config_dict = {'Categories': {'cat1': 10, 'cat2': 20, 'cat3': 40}}
        args = ['-c', '1', '2', '3']
        expected = {'cat1': 1, 'cat2': 2, 'cat3': 3}
        self.assertEqual(expected, null.parse_args(
            config_dict, args)['Categories'])

    def test_Option_categories_valid_no_arg(self):
        config_dict = {'Categories': {'cat1': 10, 'cat2': 20, 'cat3': 40}}
        args = []
        expected = {'cat1': 10, 'cat2': 20, 'cat3': 40}
        self.assertEqual(expected, null.parse_args(
            config_dict, args)['Categories'])

    def test_Option_categories_invalid(self):
        config_dict = {'Categories': {'cat1': 10, 'cat2': 20, 'cat3': 40}}
        args = ['-c', '1', 'd', '3']
        with self.assertRaises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                null.parse_args(config_dict, args)

        self.assertEqual(cm.exception.code, 2)

    def test_Option_categories_too_few_arguments(self):
        config_dict = {'Categories': {'cat1': 10, 'cat2': 20, 'cat3': 40}}
        args = ['-c', '1']
        with self.assertRaises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                null.parse_args(config_dict, args)

        self.assertEqual(cm.exception.code, 2)

    # ----------------------------------------------------

    def test_Option_category_extension_valid(self):
        config_dict = {}
        args = ['-ce', 'txt', '2', '3', '20']
        expected = {'cat1': 2, 'cat2': 3, 'cat3': 20}
        self.assertEqual(expected, null.parse_args(
            config_dict, args)['txt'])

    def test_Option_category_extension_valid_no_arg(self):
        config_dict = {}
        args = []
        expected = {'start_directory': '.',
                    'recursive': False, 'verbose': False}
        self.assertEqual(expected, null.parse_args(config_dict, args))

    def test_Option_category_extension_multiple_valid(self):
        config_dict = {}
        args = ['-ce', 'txt', '2', '3', '20', '-ce', 'mp4', '20', '40', '80']
        expected_txt = {'cat1': 2, 'cat2': 3, 'cat3': 20}
        expected_mp4 = {'cat1': 20, 'cat2': 40, 'cat3': 80}

        config_dict = null.parse_args(config_dict, args)
        self.assertEqual(expected_txt, config_dict['txt'])
        self.assertEqual(expected_mp4, config_dict['mp4'])

    def test_Option_category_extension_invalid(self):
        config_dict = {}
        args = ['-ce', 'txt', 'd', '3', '4']
        with self.assertRaises(ValueError) as cm:
            with capture_sys_output() as (stdout, stderr):
                null.parse_args(config_dict, args)

    def test_Option_category_extension_too_few_arguments(self):
        config_dict = {}
        args = ['-ce', 'txt', '1']
        with self.assertRaises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                null.parse_args(config_dict, args)

        self.assertEqual(cm.exception.code, 2)

    # ----------------------------------------------------

    def test_Option_c1_valid(self):
        config_dict = {'Categories': {'cat1': 10, 'cat2': 20, 'cat3': 40}}
        args = ['-c1', '20']
        expected = {'cat1': 20, 'cat2': 20, 'cat3': 40}
        self.assertEqual(expected, null.parse_args(
            config_dict, args)['Categories'])

    def test_Option_c1_valid_no_arg(self):
        config_dict = {'Categories': {'cat1': 10, 'cat2': 20, 'cat3': 40}}
        args = []
        expected = {'cat1': 10, 'cat2': 20, 'cat3': 40}
        self.assertEqual(expected, null.parse_args(
            config_dict, args)['Categories'])

    def test_Option_c1_invalid(self):
        config_dict = {'Categories': {'cat1': 10, 'cat2': 20, 'cat3': 40}}
        args = ['-c1', 's']
        with self.assertRaises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                null.parse_args(config_dict, args)

        self.assertEqual(cm.exception.code, 2)

    def test_Option_c1_too_few_arguments(self):
        config_dict = {'Categories': {'cat1': 10, 'cat2': 20, 'cat3': 40}}
        args = ['-c1']
        with self.assertRaises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                null.parse_args(config_dict, args)

        self.assertEqual(cm.exception.code, 2)

    # ----------------------------------------------------

    def test_Option_c2_valid(self):
        config_dict = {'Categories': {'cat1': 10, 'cat2': 20, 'cat3': 40}}
        args = ['-c2', '30']
        expected = {'cat1': 10, 'cat2': 30, 'cat3': 40}
        self.assertEqual(expected, null.parse_args(
            config_dict, args)['Categories'])

    def test_Option_c2_invalid(self):
        config_dict = {'Categories': {'cat1': 10, 'cat2': 20, 'cat3': 40}}
        args = ['-c2', 's']
        with self.assertRaises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                null.parse_args(config_dict, args)

        self.assertEqual(cm.exception.code, 2)

    def test_Option_c2_too_few_arguments(self):
        config_dict = {'Categories': {'cat1': 10, 'cat2': 20, 'cat3': 40}}
        args = ['-c2']
        with self.assertRaises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                null.parse_args(config_dict, args)

        self.assertEqual(cm.exception.code, 2)

    # ----------------------------------------------------

    def test_Option_c3_valid(self):
        config_dict = {'Categories': {'cat1': 10, 'cat2': 20, 'cat3': 40}}
        args = ['-c3', '20']
        expected = {'cat1': 10, 'cat2': 20, 'cat3': 20}
        self.assertEqual(expected, null.parse_args(
            config_dict, args)['Categories'])

    def test_Option_c3_invalid(self):
        config_dict = {'Categories': {'cat1': 10, 'cat2': 20, 'cat3': 40}}
        args = ['-c3', 's']
        with self.assertRaises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                null.parse_args(config_dict, args)

        self.assertEqual(cm.exception.code, 2)

    def test_Option_c3_too_few_arguments(self):
        config_dict = {'Categories': {'cat1': 10, 'cat2': 20, 'cat3': 40}}
        args = ['-c3']
        with self.assertRaises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                null.parse_args(config_dict, args)

        self.assertEqual(cm.exception.code, 2)

    # ----------------------------------------------------

    def test_Option_null_char_valid(self):
        config_dict = {'null_char': '\x00'}
        args = ['-n', '20']
        expected = '\x20'
        self.assertEqual(expected, null.parse_args(
            config_dict, args)['null_char'])

    def test_Option_null_char_valid_no_arg(self):
        config_dict = {'null_char': '\x11'}
        args = []
        expected = '\x11'
        self.assertEqual(expected, null.parse_args(
            config_dict, args)['null_char'])

    def test_Option_null_char_invalid(self):
        config_dict = {'null_char': '\x00'}
        args = ['-n', 's']
        with self.assertRaises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                null.parse_args(config_dict, args)

        self.assertEqual(cm.exception.code, 2)

    def test_Option_null_char_too_few_arguments(self):
        config_dict = {'null_char': '\x00'}
        args = ['-n']
        with self.assertRaises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                null.parse_args(config_dict, args)

        self.assertEqual(cm.exception.code, 2)

    # ----------------------------------------------------

    def test_Option_start_directory_valid(self):
        config_dict = {'start_directory': 'c:\\'}
        args = ['-s', '.']
        expected = '.'
        self.assertEqual(expected, null.parse_args(
            config_dict, args)['start_directory'])

    def test_Option_start_directory_valid_no_arg(self):
        config_dict = {'start_directory': 'c:\\'}
        args = []
        expected = '.'
        self.assertEqual(expected, null.parse_args(
            config_dict, args)['start_directory'])

    def test_Option_start_directory_invalid(self):
        config_dict = {'start_directory': '.'}
        args = ['-s', 's']
        with self.assertRaises(ValueError) as cm:
            with capture_sys_output() as (stdout, stderr):
                null.parse_args(config_dict, args)

    def test_Option_start_directory_too_few_arguments(self):
        config_dict = {'start_directory': '.'}
        args = ['-s']
        with self.assertRaises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                null.parse_args(config_dict, args)

        self.assertEqual(cm.exception.code, 2)

    # ----------------------------------------------------

    def test_Option_recursive_valid(self):
        config_dict = {'recursive': False}
        args = ['-r']
        expected = True
        self.assertEqual(expected, null.parse_args(
            config_dict, args)['recursive'])

    def test_Option_recursive_valid_no_arg(self):
        config_dict = {'recursive': False}
        args = []
        expected = False
        self.assertEqual(expected, null.parse_args(
            config_dict, args)['recursive'])

    def test_Option_recursive_too_many_arguments(self):
        config_dict = {'recursive': False}
        args = ['-r', '2']
        with self.assertRaises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                null.parse_args(config_dict, args)

        self.assertEqual(cm.exception.code, 2)

    # ----------------------------------------------------

    def test_Option_verbose_valid(self):
        config_dict = {'verbose': False}
        args = ['-v']
        expected = True
        self.assertEqual(expected, null.parse_args(
            config_dict, args)['verbose'])

    def test_Option_verbose_valid_no_arg(self):
        config_dict = {'verbose': False}
        args = []
        expected = False
        self.assertEqual(expected, null.parse_args(
            config_dict, args)['verbose'])

    def test_Option_null_char_too_many_arguments(self):
        config_dict = {'verbose': False}
        args = ['-v', '2']
        with self.assertRaises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                null.parse_args(config_dict, args)

        self.assertEqual(cm.exception.code, 2)

if __name__ == '__main__':
    unittest.main()
