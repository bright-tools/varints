#!/usr/bin/python

import sys

if sys.version_info[0] > 2:
    def empty_varint_storage():
        return bytes()
    def varint_storage(b):
        return bytes((b, ))
    def store_to_num(b):
        return b
    def num_types():
        return (int)
else:
    def empty_varint_storage():
        return ""
    def varint_storage(b):
        return chr(b)
    def store_to_num(b):
        return ord(b)
    def num_types():
        return (int,long)

def dump( num ):
    print( "Len: {}".format( len(num) ))
    for element in num:
        print( "B: {}".format( store_to_num(element) ))

def generic_encode( num, funcs ):
    ret_val = None
    if( isinstance(num, list)):
        ret_val = encode_list( num, funcs )
    elif( isinstance( num, num_types() )):
        ret_val = funcs['encode_int']( num )
    return ret_val

def encode_list( num, funcs ):
    ret_val = empty_varint_storage()
    for val in num:
        ret_val = ret_val + funcs['encode_int']( val )
    return ret_val

def generic_decode( num, funcs ):
    ret_val = None
    if( isinstance(num, (str,bytes))):
        ptr = 0
        while ptr < len( num ):
            (int_val, bytes_used) = funcs['decode_val']( num[ptr:] )
            ptr = ptr + bytes_used
            if ret_val is None:
                ret_val = int_val
            else:
                if isinstance( ret_val, num_types()):
                    ret_val = [ret_val]
                ret_val.append( int_val )
    return ret_val

# Stuff to eventually be deleted is below

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
