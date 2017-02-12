#!/usr/bin/python

import sys

if sys.version_info[0] > 2:
    def varint_storage(b):
        return bytes((b, ))
    def store_to_num(b):
        return b
else:
    def varint_storage(b):
        return chr(b)
    def store_to_num(b):
        return ord(b)

def dump( num ):
    print( "Len: {}",len(num))
    for element in num:
        print( "{}".format( store_to_num(element) ))

def bitsUsed( num ):
    if num < 2:
        retVal = 0
    elif num < 4:
        retVal = 1
    elif num < 16:
        retVal = 2
    elif num < 32:
        retVal = 3
    return retVal

def num2flcompactascii( numArray ):

    highest = max( numArray )
    bits = bitsUsed( highest )

    retVal = ""
    accumulator = ""

    #print("===== Start =")

    for num in numArray:
        #print("Packing {}".format(num))
        accumulator += ("1" * bits) + "0"
        accumulator += bin( num )[2:]

        while len( accumulator ) > 7:
            val = accumulator[0:7]
            accumulator = accumulator[8:]
            #print("Shifting to accumulator: {}".format(val))
            retVal += chr(int(val,2))
            
        #print("Acc: {}".format(accumulator))
    
    if( len ( accumulator ) > 0 ):
        accumulator = accumulator.ljust(7,'0')
        retVal += chr(int(accumulator,2))
    
    return retVal

def to_var_len_ascii( numArray ):

    retVal = ""
    accumulator = ""

    #print("===== Start =")

    for num in numArray:
        #print("Packing {}".format(num))
        bits = bitsUsed( num )
        accumulator += ("1" * bits) + "0"
        accumulator += bin( num )[2:]

        while len( accumulator ) > 7:
            val = accumulator[0:7]
            accumulator = accumulator[8:]
            #print("Shifting to accumulator: {}".format(val))
            retVal += chr(int(val,2))
            
        #print("Acc: {}".format(accumulator))
    
    if( len ( accumulator ) > 0 ):
        accumulator = accumulator.ljust(7,'0')
        retVal += chr(int(accumulator,2))
    
    return retVal

def from_var_len_ascii( num_str ):

    ret_val = []

    return ret_val
