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

from ..varints import varint_storage,empty_varint_storage,num_types,generic_encode,generic_decode
from ..varints import store_to_num

ONE_BYTE_LIMIT = 240
TWO_BYTE_LIMIT = 2287
THREE_BYTE_LIMIT = 67823

FOUR_BYTE_LIMIT = 16777215
FIVE_BYTE_LIMIT = 4294967295
SIX_BYTE_LIMIT = 1099511627775
SEVEN_BYTE_LIMIT = 281474976710655
EIGHT_BYTE_LIMIT = 72057594037927935
NINE_BYTE_LIMIT = 18446744073709551615
THREE_BYTE_HEADER = 249
FOUR_BYTE_HEADER = 250
FIVE_BYTE_HEADER = 251
SIX_BYTE_HEADER = 252
SEVEN_BYTE_HEADER = 253
EIGHT_BYTE_HEADER = 254
NINE_BYTE_HEADER = 255
BYTE_VALS = 256
SHORT_VALS = 65536

BUCKET_OFFSET = 2

buckets = [ { 'limit': FOUR_BYTE_LIMIT,
              'header': FOUR_BYTE_HEADER },
            { 'limit': FIVE_BYTE_LIMIT,
              'header': FIVE_BYTE_HEADER },
            { 'limit': SIX_BYTE_LIMIT,
              'header': SIX_BYTE_HEADER },
            { 'limit': SEVEN_BYTE_LIMIT,
              'header': SEVEN_BYTE_HEADER },
            { 'limit': EIGHT_BYTE_LIMIT,
              'header': EIGHT_BYTE_HEADER },
            { 'limit': NINE_BYTE_LIMIT,
              'header': NINE_BYTE_HEADER },
          ]

def encode( num ):
    return generic_encode( num, funcs )

def encode_int( num ):
    ret_val = None
    if num < 0:
        raise ValueError("Negative numbers not handled")

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
    else:
        start = 0

        # Work out how many bytes are needed to store this value
        while(( start < len( buckets )) and
              ( num > buckets[start]['limit'])):
            start = start + 1

        if( start == len( buckets )):
            raise ValueError("Too large")

        ret_val = varint_storage( buckets[start]['header'] )
        mod = (buckets[start]['limit']+1) // BYTE_VALS
        start = start + BUCKET_OFFSET

        while( start >= 0 ):
            start = start - 1
            ret_val = ret_val + varint_storage( num // mod )
            num = num % mod
            mod = mod // BYTE_VALS

    return ret_val

def decode( num ):
    return generic_decode( num, funcs )

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
    else:
        data_bytes = first-247
        start = data_bytes - 1
        ret_val = 0
        i = 1

        mod = (buckets[start-BUCKET_OFFSET]['limit']+1) // BYTE_VALS

        while( start >= 0 ):
            ret_val = ret_val + (mod * store_to_num( num[ i ] )) 
            i = i + 1
            start = start - 1
            mod = mod // BYTE_VALS

        bytes_used = data_bytes + 1

    return (ret_val, bytes_used)

funcs = { 'decode_val': decode_val,
          'encode_int': encode_int }
