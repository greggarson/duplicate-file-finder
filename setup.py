from setuptools import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='duplicate_file_finder',
    version='0.1',
    description='Script to allow for the location of files containing the same '
                'content within a given directory tree',
    long_description=read('README'),
    author='Greg Garson',
    packages=['duplicate_finder', 'tests',],
    author_email='greggarson@gmail.com',
    maintainer='Greg Garson',
    maintainer_email='greggarson@gmail.com',
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'duplicate_finder = duplicate_finder.finder:print_duplicates',
        ]
    },
    test_suite='tests',
)