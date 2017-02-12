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

class TestStringMethods(unittest.TestCase):

    def test_sqlite_single_number_zero(self):
        test_data = 0
        expected_result = varints.varint_storage(0)

        ascii_result = varints.sqlite.encode(test_data)
        num_result = varints.sqlite.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    def test_sqlite_single_number_max_one_byte(self):
        test_data = 240
        expected_result = varints.varint_storage(240)

        ascii_result = varints.sqlite.encode(test_data)
        num_result = varints.sqlite.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    def test_sqlite_single_number_min_two_byte(self):
        test_data = 241
        expected_result = varints.varint_storage( 241 ) + \
                          varints.varint_storage( 1 )

        ascii_result = varints.sqlite.encode(test_data)
        num_result = varints.sqlite.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    def test_sqlite_single_number_max_two_byte(self):
        test_data = 2287
        expected_result = varints.varint_storage( 248 ) + \
                          varints.varint_storage( 255 )

        ascii_result = varints.sqlite.encode(test_data)
        num_result = varints.sqlite.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    def test_sqlite_single_number_min_three_byte(self):
        test_data = 2288
        expected_result = varints.varint_storage( 249 ) + \
                          varints.varint_storage( 0 ) + \
                          varints.varint_storage( 0 )

        ascii_result = varints.sqlite.encode(test_data)
        num_result = varints.sqlite.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    def test_sqlite_single_number_max_three_byte(self):
        test_data = 67823 
        expected_result = varints.varint_storage( 249 ) + \
                          varints.varint_storage( 255 ) + \
                          varints.varint_storage( 255 )

        ascii_result = varints.sqlite.encode(test_data)
        num_result = varints.sqlite.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    def test_sqlite_single_number_min_four_byte(self):
        test_data = 67824
        expected_result = varints.varint_storage( 250 ) + \
                          varints.varint_storage( 1 ) + \
                          varints.varint_storage( 8 ) + \
                          varints.varint_storage( 240 )

        ascii_result = varints.sqlite.encode(test_data)
        num_result = varints.sqlite.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    def test_sqlite_single_number_min_four_byte(self):
        test_data = 16777215
        expected_result = varints.varint_storage( 250 ) + \
                          varints.varint_storage( 255 ) + \
                          varints.varint_storage( 255 ) + \
                          varints.varint_storage( 255 )

        ascii_result = varints.sqlite.encode(test_data)
        num_result = varints.sqlite.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

if __name__ == '__main__':
    unittest.main()
