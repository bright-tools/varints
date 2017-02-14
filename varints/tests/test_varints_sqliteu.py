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

    """ Test the sqliteu varint format, using passing None """
    def test_sqliteu_none(self):
        test_data = None
        expected_result = None

        ascii_result = varints.sqliteu.encode(test_data)
        num_result = varints.sqliteu.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    """ Test the sqliteu varint format, using a negative number """
    def test_sqliteu_single_number_negative(self):
        test_data = -1

        self.assertRaises(ValueError,varints.sqliteu.encode,test_data)

    """ Test the sqliteu varint format, using a value of zero """
    def test_sqliteu_single_number_zero(self):
        test_data = 0
        expected_result = varints.varint_storage(0)

        ascii_result = varints.sqliteu.encode(test_data)
        num_result = varints.sqliteu.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    """ Test the sqliteu varint format, using the maximum value which can be
        represented by a single varint byte """
    def test_sqliteu_single_number_max_one_byte(self):
        test_data = 240
        expected_result = varints.varint_storage(240)

        ascii_result = varints.sqliteu.encode(test_data)
        num_result = varints.sqliteu.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    """ Test the sqliteu varint format, using the minimum value which can be
        represented by a two byte varint """
    def test_sqliteu_single_number_min_two_byte(self):
        test_data = 241
        expected_result = varints.varint_storage( 241 ) + \
                          varints.varint_storage( 1 )

        ascii_result = varints.sqliteu.encode(test_data)
        num_result = varints.sqliteu.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    """ Test the sqliteu varint format, using the maximum value which can be
        represented by a two byte varint """
    def test_sqliteu_single_number_max_two_byte(self):
        test_data = 2287
        expected_result = varints.varint_storage( 248 ) + \
                          varints.varint_storage( 255 )

        ascii_result = varints.sqliteu.encode(test_data)
        num_result = varints.sqliteu.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    """ Test the sqliteu varint format, using the minimum value which can be
        represented by a three byte varint """
    def test_sqliteu_single_number_min_three_byte(self):
        test_data = 2288
        expected_result = varints.varint_storage( 249 ) + \
                          varints.varint_storage( 0 ) + \
                          varints.varint_storage( 0 )

        ascii_result = varints.sqliteu.encode(test_data)
        num_result = varints.sqliteu.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    """ Test the sqliteu varint format, using the maximum value which can be
        represented by a three byte varint """
    def test_sqliteu_single_number_max_three_byte(self):
        test_data = 67823 
        expected_result = varints.varint_storage( 249 ) + \
                          varints.varint_storage( 255 ) + \
                          varints.varint_storage( 255 )

        ascii_result = varints.sqliteu.encode(test_data)
        num_result = varints.sqliteu.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    """ Test the sqliteu varint format, using the minimum value which can be
        represented by a four byte varint """
    def test_sqliteu_single_number_min_four_byte(self):
        test_data = 67824
        expected_result = varints.varint_storage( 250 ) + \
                          varints.varint_storage( 1 ) + \
                          varints.varint_storage( 8 ) + \
                          varints.varint_storage( 240 )

        ascii_result = varints.sqliteu.encode(test_data)
        num_result = varints.sqliteu.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    """ Test the sqliteu varint format, using the maximum value which can be
        represented by a four byte varint """
    def test_sqliteu_single_number_max_four_byte(self):
        test_data = 16777215
        expected_result = varints.varint_storage( 250 ) + \
                          varints.varint_storage( 255 ) + \
                          varints.varint_storage( 255 ) + \
                          varints.varint_storage( 255 )


        ascii_result = varints.sqliteu.encode(test_data)
        num_result = varints.sqliteu.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    """ Test the sqliteu varint format, using the maximum value which can be
        represented by this encoding format """
    def test_sqliteu_single_max(self):
        test_data = 2 ** 64 - 1
        expected_result = varints.varint_storage( 255 ) + \
                          varints.varint_storage( 255 ) + \
                          varints.varint_storage( 255 ) + \
                          varints.varint_storage( 255 ) + \
                          varints.varint_storage( 255 ) + \
                          varints.varint_storage( 255 ) + \
                          varints.varint_storage( 255 ) + \
                          varints.varint_storage( 255 ) + \
                          varints.varint_storage( 255 )

        ascii_result = varints.sqliteu.encode(test_data)
        num_result = varints.sqliteu.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    """ Test the sqliteu varint format, using a value outside the range which
        can be represented by this encoding format """
    def test_sqliteu_single_over_range(self):
        test_data = 2 ** 64

        self.assertRaises(ValueError,varints.sqliteu.encode,test_data)

    """ Test the sqliteu varint format, using an array of length zero """
    def test_sqliteu_array_empty(self):
        test_data = []

        ascii_result = varints.sqliteu.encode(test_data)
        num_result = varints.sqliteu.decode(ascii_result)

        self.assertEqual(len(ascii_result),0)
        self.assertEqual(num_result,None)

    """ Test the sqliteu varint format, using a two element array, both resulting
        in a single byte varint"""
    def test_sqliteu_two_nums_small(self):
        test_data = [1,2]
        expected_result = varints.varint_storage(1) + \
                          varints.varint_storage(2)

        ascii_result = varints.sqliteu.encode(test_data)
        num_result = varints.sqliteu.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)

    """ Test the sqliteu varint format, using a two element array, both
        resulting in different length varints """
    def test_sqliteu_two_nums_large(self):
        test_data = [67824,2288]
        expected_result = varints.varint_storage(250) + \
                          varints.varint_storage(1) + \
                          varints.varint_storage(8) + \
                          varints.varint_storage(240) + \
                          varints.varint_storage(249) + \
                          varints.varint_storage(0) + \
                          varints.varint_storage(0)

        ascii_result = varints.sqliteu.encode(test_data)
        num_result = varints.sqliteu.decode(ascii_result)

        self.assertEqual(ascii_result,expected_result)
        self.assertEqual(num_result,test_data)



if __name__ == '__main__':
    unittest.main()
