#!/usr/bin/python

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

#    def test_single_number_min(self):
#        self.assertEqual(num2compactascii([1]),chr(int('0100000',2)))

#    def test_single_number_max(self):
#        self.assertEqual(num2compactascii([9]),chr(int('1101001',2)))
    
#    def test_double_digit_min(self):
#        self.assertEqual(num2compactascii([10]),chr(int('1101010',2)))

#    def test_two_digits_min(self):
#        self.assertEqual(num2compactascii([0,0]),chr(int('0000000',2)))
    
#    def test_two_digits_min(self):
#        self.assertEqual(num2compactascii([0,0]),chr(int('0000000',2)))

if __name__ == '__main__':
    unittest.main()
