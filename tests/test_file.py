# -*- coding: utf-8 -*-

from .context import null

import unittest, tempfile


class FileTestSuite(unittest.TestCase):
    """Basic test cases."""

    def setUp(self):
        # Create a temporary file and File object
        self.test_file = tempfile.NamedTemporaryFile(suffix='.zip')
        self.file = null.File(path=self.test_file.name)
      
    def tearDown(self):
        # Remove the directory after the test
        self.test_file.file.close()

    def test_File_creation(self):
        # Confirm creation of null.File object
        assertIsInstance(self.file, null.File)
        
    def test_null_count_initial(self):
        # Check inital null count is set to zero
        assertEqual(self.file.null_count, 0)

    def test_File_name(self):
        assertEqual(self.file.name, self.test_file.name)  

    def test_File_name_suffix(self):
        assertEqual(self.file.suffix, 'zip')

    def test_File_size(self):
        assertEqual(self.file.size, 0)

if __name__ == '__main__':
    unittest.main()