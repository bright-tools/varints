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

import unittest
import varints
import sys

class TestStringMethods(unittest.TestCase):

    """ Test the dlugoszu varint format, using passing None """
    def test_dlugoszu_none(self):
        test_data = None
        expected_result = None

        ascii_result = varints.dlugoszu.encode(test_data)
        self.assertEqual(ascii_result,expected_result)

        num_result = varints.dlugoszu.decode(ascii_result)
        self.assertEqual(num_result,test_data)

    """ Test the dlugoszu varint format, using a negative number """
    def test_dlugoszu_single_number_negative(self):
        test_data = -1

        self.assertRaises(ValueError,varints.dlugoszu.encode,test_data)

    """ Test the dlugoszu varint format, using a value of zero """
    def test_dlugoszu_single_number_zero(self):
        test_data = 0
        expected_result = varints.varint_storage(0)

        ascii_result = varints.dlugoszu.encode(test_data)
        self.assertEqual(ascii_result,expected_result)

        num_result = varints.dlugoszu.decode(ascii_result)
        self.assertEqual(num_result,test_data)

    """ Test the dlugoszu varint format, using minimum non-zero value """
    def test_dlugoszu_single_number_non_zero(self):
        test_data = 1
        expected_result = varints.varint_storage(1)

        ascii_result = varints.dlugoszu.encode(test_data)
        self.assertEqual(ascii_result,expected_result)

        num_result = varints.dlugoszu.decode(ascii_result)
        self.assertEqual(num_result,test_data)

    """ Test the dlugoszu varint format, using max value which can be stored in a single byte """
    def test_dlugoszu_single_number_max(self):
        test_data = 127
        expected_result = varints.varint_storage(127)

        ascii_result = varints.dlugoszu.encode(test_data)
        self.assertEqual(ascii_result,expected_result)

        num_result = varints.dlugoszu.decode(ascii_result)
        self.assertEqual(num_result,test_data)

    """ Test the dlugoszu varint format, using minimum value necessary for 2 byte
        storage """
    def test_dlugoszu_two_number_min(self):
        test_data = 128
        expected_result = varints.varint_storage(128) + \
                          varints.varint_storage(128)

        ascii_result = varints.dlugoszu.encode(test_data)
        self.assertEqual(ascii_result,expected_result)

        num_result = varints.dlugoszu.decode(ascii_result)
        self.assertEqual(num_result,test_data)

    """ Test the dlugoszu varint format, using maximum value necessary for 2 byte
        storage """
    def test_dlugoszu_two_number_max(self):
        test_data = 16383
        expected_result = varints.varint_storage(191) + \
                          varints.varint_storage(255)

        ascii_result = varints.dlugoszu.encode(test_data)
        self.assertEqual(ascii_result,expected_result)

        num_result = varints.dlugoszu.decode(ascii_result)
        self.assertEqual(num_result,test_data)

    """ Test the dlugoszu varint format, using minimum value necessary for 3 byte
        storage """
    def test_dlugoszu_three_number_min(self):
        test_data = 16384
        expected_result = varints.varint_storage(0xC0) + \
                          varints.varint_storage(0x40) + \
                          varints.varint_storage(0x00)

        ascii_result = varints.dlugoszu.encode(test_data)
        self.assertEqual(ascii_result,expected_result)

        num_result = varints.dlugoszu.decode(ascii_result)
        self.assertEqual(num_result,test_data)

    """ Test the dlugoszu varint format, using maximum value necessary for 3 byte
        storage """
    def test_dlugoszu_three_number_max(self):
        test_data = 2097151
        expected_result = varints.varint_storage(223) + \
                          varints.varint_storage(255) + \
                          varints.varint_storage(255)

        ascii_result = varints.dlugoszu.encode(test_data)
        self.assertEqual(ascii_result,expected_result)

        num_result = varints.dlugoszu.decode(ascii_result)
        self.assertEqual(num_result,test_data)

    """ Test the dlugoszu varint format, using minimum value necessary for 4 byte
        storage """
    def test_dlugoszu_four_number_min(self):
        test_data = 2097152
        expected_result = varints.varint_storage(224) + \
                          varints.varint_storage(0x20) + \
                          varints.varint_storage(0) + \
                          varints.varint_storage(0)

        ascii_result = varints.dlugoszu.encode(test_data)
        self.assertEqual(ascii_result,expected_result)

        num_result = varints.dlugoszu.decode(ascii_result)
        self.assertEqual(num_result,test_data)

    """ Test the dlugoszu varint format, using maximum value necessary for 4 byte
        storage """
    def test_dlugoszu_four_number_max(self):
        test_data = 134217727
        expected_result = varints.varint_storage(231) + \
                          varints.varint_storage(255) + \
                          varints.varint_storage(255) + \
                          varints.varint_storage(255)

        ascii_result = varints.dlugoszu.encode(test_data)
        self.assertEqual(ascii_result,expected_result)

        num_result = varints.dlugoszu.decode(ascii_result)
        self.assertEqual(num_result,test_data)

    """ Test the dlugoszu varint format, using minimum value necessary for 5 byte
        storage """
    def test_dlugoszu_five_number_min(self):
        test_data = 134217728
        expected_result = varints.varint_storage(232) + \
                          varints.varint_storage(8) + \
                          varints.varint_storage(0) + \
                          varints.varint_storage(0) + \
                          varints.varint_storage(0)

        ascii_result = varints.dlugoszu.encode(test_data)
        self.assertEqual(ascii_result,expected_result)

        num_result = varints.dlugoszu.decode(ascii_result)
        self.assertEqual(num_result,test_data)

    """ Test the dlugoszu varint format, using maximum value necessary for 5 byte
        storage """
    def test_dlugoszu_five_number_max(self):
        test_data = 34359738367
        expected_result = varints.varint_storage(239) + \
                          varints.varint_storage(255) + \
                          varints.varint_storage(255) + \
                          varints.varint_storage(255) + \
                          varints.varint_storage(255)

        ascii_result = varints.dlugoszu.encode(test_data)
        self.assertEqual(ascii_result,expected_result)

        num_result = varints.dlugoszu.decode(ascii_result)
        self.assertEqual(num_result,test_data)

if __name__ == '__main__':
    unittest.main()
