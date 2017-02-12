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

# Based on the encoding method described at
#  https://sqlite.org/src4/doc/trunk/www/varint.wiki

from ..varints import varint_storage,empty_varint_storage,num_types
from ..varints import store_to_num

ONE_BYTE_LIMIT = 240
TWO_BYTE_LIMIT = 2287
THREE_BYTE_LIMIT = 67823
FOUR_BYTE_LIMIT = 16777215
THREE_BYTE_HEADER = 249
FOUR_BYTE_HEADER = 250
BYTE_VALS = 256
SHORT_VALS = 65536

def encode( num ):
    ret_val = None
    if( isinstance(num, list)):
        ret_val = encode_list( num )
    elif( isinstance( num, num_types() )):
        ret_val = encode_int( num )
    return ret_val

def encode_list( num ):
    ret_val = empty_varint_storage()
    for val in num:
        ret_val = ret_val + encode_int( val )
    return ret_val

def encode_int( num ):
    ret_val = None
    if( num <= ONE_BYTE_LIMIT ):
        ret_val = varint_storage( num )
    elif( num <= TWO_BYTE_LIMIT ):
        top = num-ONE_BYTE_LIMIT
        ret_val = varint_storage( (top // BYTE_VALS)+ONE_BYTE_LIMIT+1 ) + \
                  varint_storage( top % BYTE_VALS )
    elif( num <= THREE_BYTE_LIMIT ):
        top = num-(TWO_BYTE_LIMIT+1)
        ret_val = varint_storage( THREE_BYTE_HEADER ) + \
                  varint_storage( top // BYTE_VALS ) + \
                  varint_storage( top % BYTE_VALS )
    elif( num <= FOUR_BYTE_LIMIT ):
        top = num % SHORT_VALS
        ret_val = varint_storage( FOUR_BYTE_HEADER ) + \
                  varint_storage( num // SHORT_VALS ) + \
                  varint_storage( top // BYTE_VALS ) + \
                  varint_storage( top % BYTE_VALS )
    return ret_val

def decode( num ):
    ret_val = None
    if( isinstance(num, (str,bytes))):
        ret_val = decode_list( num )
    return ret_val

def decode_list( num ):
    ret_val = None
    ptr = 0
    while ptr < len( num ):
        (int_val, bytes_used) = decode_val( num[ptr:] )
        ptr = ptr + bytes_used
        if ret_val is None:
            ret_val = int_val
        else:
            if isinstance( ret_val, num_types()):
                ret_val = [ret_val]
            ret_val.append( int_val )
    return ret_val

def decode_val( num ):
    ret_val = None
    bytes_used = 1
    first = store_to_num( num[ 0 ] )
    if( first <= ONE_BYTE_LIMIT ):
        ret_val = first
    elif( first < THREE_BYTE_HEADER ):
        second = store_to_num( num[ 1 ] )
        ret_val = ONE_BYTE_LIMIT+(BYTE_VALS*(first-(ONE_BYTE_LIMIT+1)))+second
        bytes_used = 2
    elif( first == THREE_BYTE_HEADER ):
        second = store_to_num( num[ 1 ] )
        third = store_to_num( num[ 2 ] )
        ret_val = (TWO_BYTE_LIMIT+1)+(BYTE_VALS*second)+third
        bytes_used = 3
    elif( first == FOUR_BYTE_HEADER ):
        second = store_to_num( num[ 1 ] )
        third = store_to_num( num[ 2 ] )
        fourth = store_to_num( num[ 3 ] )
        ret_val = (second*SHORT_VALS) + (third*BYTE_VALS) + fourth
        bytes_used = 4
    return (ret_val, bytes_used)
