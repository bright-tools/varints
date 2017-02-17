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

    """ Test the leb128s varint format, using passing None """
    def test_leb128s_none(self):
        test_data = None
        expected_result = None

        ascii_result = varints.leb128s.encode(test_data)
        num_result = varints.leb128s.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    """ Test the leb128s varint format, using a value of zero """
    def test_leb128s_single_number_zero(self):
        test_data = 0
        expected_result = varints.varint_storage(0)

        ascii_result = varints.leb128s.encode(test_data)
        num_result = varints.leb128s.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    """ Test the leb128s varint format, using minimum positive non-zero value """
    def test_leb128s_single_number_non_zero(self):
        test_data = 1
        expected_result = varints.varint_storage(1)

        ascii_result = varints.leb128s.encode(test_data)
        num_result = varints.leb128s.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    """ Test the leb128s varint format, using smallest negative non-zero value """
    def test_leb128s_single_number_small_neg(self):
        test_data = -1
        expected_result = varints.varint_storage(0x7F)

        ascii_result = varints.leb128s.encode(test_data)
        self.assertEqual(ascii_result,expected_result)

        num_result = varints.leb128s.decode(ascii_result)
        self.assertEqual(num_result,test_data)

    """ Test the leb128s varint format, using max positive value which can be 
        stored in a single byte """
    def test_leb128s_single_number_pos_max(self):
        test_data = 63
        expected_result = varints.varint_storage(63)

        ascii_result = varints.leb128s.encode(test_data)
        self.assertEqual(ascii_result,expected_result)

        num_result = varints.leb128s.decode(ascii_result)
        self.assertEqual(num_result,test_data)

    """ Test the leb128s varint format, using max negative value which can be 
        stored in a single byte """
    def test_leb128s_single_number_neg_max(self):
        test_data = -64
        expected_result = varints.varint_storage(64)

        ascii_result = varints.leb128s.encode(test_data)
        self.assertEqual(ascii_result,expected_result)

        num_result = varints.leb128s.decode(ascii_result)
        self.assertEqual(num_result,test_data)

    """ Test the leb128s varint format, using minimum positive value necessary for 2 byte
        storage """
    def test_leb128s_two_number_pos_min(self):
        test_data = 64
        expected_result = varints.varint_storage(0xC0) + \
                          varints.varint_storage(0)

        ascii_result = varints.leb128s.encode(test_data)
        self.assertEqual(ascii_result,expected_result)

        num_result = varints.leb128s.decode(ascii_result)
        self.assertEqual(num_result,test_data)

    """ Test the leb128s varint format, using minimum negative value necessary for 2 byte
        storage """
    def test_leb128s_two_number_neg_min(self):
        test_data = -65
        expected_result = varints.varint_storage(0xBF) + \
                          varints.varint_storage(0x7F)

        ascii_result = varints.leb128s.encode(test_data)
        self.assertEqual(ascii_result,expected_result)

        num_result = varints.leb128s.decode(ascii_result)
        self.assertEqual(num_result,test_data)

    """ Test the leb128s varint format, using maximum positive value necessary for 2 byte
        storage """
    def test_leb128s_two_number_pos_max(self):
        test_data = 8191
        expected_result = varints.varint_storage(255) + \
                          varints.varint_storage(63)

        ascii_result = varints.leb128s.encode(test_data)
        num_result = varints.leb128s.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    """ Test the leb128s varint format, using maximum negative value necessary for 2 byte
        storage """
    def test_leb128s_two_number_neg_max(self):
        test_data = -8192
        expected_result = varints.varint_storage(0x80) + \
                          varints.varint_storage(0x40)

        ascii_result = varints.leb128s.encode(test_data)
        num_result = varints.leb128s.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    """ Test the leb128s varint format, using minimum value necessary for 3 byte
        storage """
    def test_leb128s_three_number_min(self):
        return
        test_data = 16384
        expected_result = varints.varint_storage(128) + \
                          varints.varint_storage(128) + \
                          varints.varint_storage(1)

        ascii_result = varints.leb128s.encode(test_data)
        num_result = varints.leb128s.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    """ Test the leb128s varint format, using maximum value necessary for 3 byte
        storage """
    def test_leb128s_three_number_max(self):
        return
        test_data = 2097151
        expected_result = varints.varint_storage(255) + \
                          varints.varint_storage(255) + \
                          varints.varint_storage(127)

        ascii_result = varints.leb128s.encode(test_data)
        num_result = varints.leb128s.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    """ Test the leb128s varint format, using minimum value necessary for 4 byte
        storage """
    def test_leb128s_four_number_min(self):
        return
        test_data = 2097152
        expected_result = varints.varint_storage(128) + \
                          varints.varint_storage(128) + \
                          varints.varint_storage(128) + \
                          varints.varint_storage(1)

        ascii_result = varints.leb128s.encode(test_data)
        num_result = varints.leb128s.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    """ Test the leb128s varint format, using maximum value necessary for 4 byte
        storage """
    def test_leb128s_four_number_max(self):
        return
        test_data = 268435455
        expected_result = varints.varint_storage(255) + \
                          varints.varint_storage(255) + \
                          varints.varint_storage(255) + \
                          varints.varint_storage(127)

        ascii_result = varints.leb128s.encode(test_data)
        num_result = varints.leb128s.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    """ Test the leb128s varint format, using minimum value necessary for 5 byte
        storage """
    def test_leb128s_five_number_min(self):
        return
        test_data = 268435456
        expected_result = varints.varint_storage(128) + \
                          varints.varint_storage(128) + \
                          varints.varint_storage(128) + \
                          varints.varint_storage(128) + \
                          varints.varint_storage(1)

        ascii_result = varints.leb128s.encode(test_data)
        num_result = varints.leb128s.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    """ Test the leb128s varint format, using maximum value necessary for 5 byte
        storage """
    def test_leb128s_five_number_max(self):
        return
        test_data = 34359738367
        expected_result = varints.varint_storage(255) + \
                          varints.varint_storage(255) + \
                          varints.varint_storage(255) + \
                          varints.varint_storage(255) + \
                          varints.varint_storage(127)

        ascii_result = varints.leb128s.encode(test_data)
        num_result = varints.leb128s.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

if __name__ == '__main__':
    unittest.main()
