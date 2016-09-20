# -*- coding: utf-8 -*-

from .context import null

import unittest
import tempfile


class FileTestSuite(unittest.TestCase):
    """Basic test cases."""

    def setUp(self):
        # Create a temporary file and File object
        self.test_file = tempfile.NamedTemporaryFile(suffix='.zip')
        self.file = null.File(name=self.test_file.name)
      
    def tearDown(self):
        # Remove the directory after the test
        self.test_file.file.close()

    def test_File_creation(self):
        # Confirm creation of null.File object
        self.assertIsInstance(self.file, null.File)
        
    def test_null_count_initial(self):
        # Check inital null count is set to zero
        self.assertEqual(self.file.null_count, 0)

    def test_File_name(self):
        self.assertEqual(self.file.name, self.test_file.name)  

    def test_File_name_suffix(self):
        self.assertEqual(self.file.suffix, 'zip')

    def test_File_size(self):
        self.assertEqual(self.file.size, 0)

if __name__ == '__main__':
    unittest.main()
