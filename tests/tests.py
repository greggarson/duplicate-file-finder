import os
import unittest
import duplicate_finder.finder


EMPTY_FILES = [os.path.join(os.path.dirname(__file__), this_file) for this_file
               in [
                   'test_files/subdir1/file1a',
                   'test_files/subdir2/file1b',
                   'test_files/subdir3/subdir3subdir1/subdir3subdir1subdir1'
                   '/file1c']]

SINGLE_LINE_FILES = [os.path.join(os.path.dirname(__file__), this_file)
                     for this_file in [
                        'test_files/subdir1/file2a',
                        'test_files/subdir2/subdir2subdir1/file2b',
                        'test_files/subdir3/subdir3subdir1/file2c']]

MULTI_LINE_FILES = [os.path.join(os.path.dirname(__file__), this_file)
                    for this_file in [
                        'test_files/subdir2/subdir2subdir1/file4a',
                        'test_files/subdir3/subdir3subdir1/'
                        'subdir3subdir1subdir1/file4b']]

UNDUPLICATED_FILES = [os.path.join(os.path.dirname(__file__), this_file)
                      for this_file in [
                          'test_files/subdir3/subdir3subdir1/file3a',]]


class DuplicateFinderTests(unittest.TestCase):

    def setUp(self):
        self.results = [list(files) for files in
                        duplicate_finder.finder.find_duplicates(os.path.join(
                            os.path.dirname(__file__), 'test_files'))]

    def test_empty_files_match_each_other(self):
        self.assertIn(EMPTY_FILES, self.results)

    def test_single_line_files_match_each_other(self):
        self.assertIn(SINGLE_LINE_FILES, self.results)

    def test_multi_line_files_match_each_other(self):
        self.assertIn(MULTI_LINE_FILES, self.results)

    def test_results_do_not_contain_unduplicated_files(self):
        self.assertNotIn(UNDUPLICATED_FILES, self.results)


if __name__ == "__main__":

    unittest.main()