#!/usr/bin/python

import unittest
import aroi

class TestStringMethods(unittest.TestCase):

    def test_single_number_zero(self):
        test_data = [0]
        expected_result = chr(0)
        ascii_result = aroi.to_var_len_ascii(test_data)
        num_result = aroi.from_var_len_ascii(ascii_result)
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
