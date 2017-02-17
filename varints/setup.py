#!/usr/bin/python

#   Copyright 2017 John Bailey
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from setuptools import setup
import unittest

def varints_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite

setup(name='varints',
      version='0.1.7',
      description='Variable-length encoding of integers',
      url='http://github.com/bright-tools/varints',
      author='John Bailey',
      author_email='dev@brightsilence.com',
      license='Apache',
      long_description=open('README', 'rt').read(),
      packages=['varints','varints.leb128u','varints.dlugoszu','varints.sqliteu'],
      test_suite='setup.varints_test_suite',
      keywords = ['varint', 'integer', 'variable', 'length' ],
      # See https://PyPI.python.org/PyPI?%3Aaction=list_classifiers
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      zip_safe=False)
