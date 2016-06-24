import os
from hashlib import sha512
import argparse


class FileMetadata(object):
    """ A class representing the relevant metadata of a file """

    def __init__(self, file_path):
        """ Initialize metadata """
        self.file_path = file_path
        self._file_hash = FileMetadata.hash_file(sha512(), file_path)
        self._file_size = FileMetadata.file_size(file_path)

    @classmethod
    def file_size(cls, file_path):
        """ For a given file_path determine the size of the underlying file """
        return os.path.getsize(file_path)

    @classmethod
    def hash_file(cls, hasher, file_path):
        """ Generate a hash representation of a file for a given hash algo """
        with open(file_path, mode='rb') as file:
            for line in file:
                hasher.update(line)
        return hasher.digest()

    @property
    def id(self):
        """ Generate an id that can be used to match this file with others

            Rather than just use the file_hash to represent the file,
            additionally including the file_size will allow for an even more
            accurate match.  While the likelihood of a hash collision with
            sha512 is highly minimal including file_size allows to handle the
            situation in all cases but the one where the files are the same
            size.
        """
        return "{file_hash}#{file_size}".format(
                file_hash=self._file_hash,
                file_size=self._file_size)


def find_duplicates(root_dir):
    """Walk the directory tree, gather file metadata, determine duplicates"""

    files_found = {}

    for directory, _, files in os.walk(root_dir):
        for current_file in files:
            file_path = os.path.join(directory, current_file)
            try:
                file_metadata = FileMetadata(file_path)
                files_found = _record_file(file_metadata, files_found)
            except (FileNotFoundError, PermissionError):
                # For now in the case where the file has been removed or we
                # do not have access to it, just ignore it.  These facts could
                # also potentially be logged somewhere if that would be of use.
                pass

    return ((this_file.file_path for this_file in files)
            for _, files in files_found.items() if len(files) > 1)


def _record_file(file_metadata, files_found):
    """ Manage the storage of the file based on its id

        If the files_found dictionary already contains the metadata id
        we've found another file containing duplicate contents, add this
        metadata object to the list attached to that id, otherwise create a
        new list, add the metadata object to that list and assign the list to
        the files_found dictionary with the metadata id as the key.

        Open question: Do we want to consider files containing no data as
        duplicates of each other?  At this point the program does.
    """

    file_id = file_metadata.id
    files_for_hash_key = files_found.get(file_id, [])
    files_for_hash_key.append(file_metadata)
    files_found[file_id] = files_for_hash_key
    return files_found


def print_duplicates(*args, **kwargs):
    """ Convenience function to print results to the command line """

    parser = argparse.ArgumentParser(
        description='Find files with duplicate '
                    'content within a directory tree.')
    parser.add_argument('root_dir', type=str, action='store',
                        help='The root directory to scan for duplicates from.')

    args = parser.parse_args()

    duplicates = find_duplicates(args.root_dir)

    print("\nFiles Containing Duplicate Content:\n")
    for files in duplicates:
        for file in files:
            print(file)
        print("-----")


if __name__ == "__main__":

    print_duplicates()
