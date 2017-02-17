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
#  http://www.dlugosz.com/ZIP2/VLI.html

from ..varints import varint_storage,empty_varint_storage,num_types,generic_encode,generic_decode
from ..varints import store_to_num

ONE_BYTE_LIMIT = 127
TWO_BYTE_LIMIT = 16383
THREE_BYTE_LIMIT = 2097151
FOUR_BYTE_LIMIT = 134217727
FIVE_BYTE_LIMIT = 34359738367
SIX_BYTE_LIMIT = 1099511627776
EIGHT_BYTE_LIMIT = 576460752303423487
NINE_BYTE_LIMIT = 18446744073709551615

minint = 0
maxint = NINE_BYTE_LIMIT

buckets = [ { 'limit': ONE_BYTE_LIMIT,
              'prefix': 0x0,
              'mod': 1,
              'val_mask': 0x7F },
            { 'limit': TWO_BYTE_LIMIT,
              'prefix': 0x80,
              'mod': 256,
              'val_mask': 0x3F },
            { 'limit': THREE_BYTE_LIMIT,
              'prefix': 0xC0,
              'mod': 256*256,
              'val_mask': 0x1F },
            { 'limit': FOUR_BYTE_LIMIT,
              'prefix': 0xE0,
              'mod': 256*256*256,
              'val_mask': 0x07 },
            { 'limit': FIVE_BYTE_LIMIT,
              'prefix': 0xE8,
              'mod': 256*256*256*256,
              'val_mask': 0x07 },
            { 'limit': SIX_BYTE_LIMIT,
              'prefix': 0xF8,
              'mod': 256*256*256*256*256,
              'val_mask': 0x00 },
            { 'limit': EIGHT_BYTE_LIMIT,
              'prefix': 0xF0,
              'mod': 256*256*256*256*256*256*256,
              'val_mask': 0x07 },
            { 'limit': NINE_BYTE_LIMIT,
              'prefix': 0xF9,
              'mod': 256*256*256*256*256*256*256*256,
              'val_mask': 0x00 }
          ]

def encode( num ):
    return generic_encode( num, funcs )

def encode_int( num ):
    if( num < 0 ):
        raise ValueError("Negative numbers not handled")
    
    ret_val = None

    prefix = None
    for b in buckets:
        if( num <= b['limit'] ):
            prefix = b['prefix']
            val_mask = b['val_mask']
            mod = b['mod']
            break

    if prefix is None:
        raise ValueError("Too large")

    ret_val = empty_varint_storage()
    while( mod > 0 ):
        val = 0

        if( prefix > 0 ):
            val = val + prefix
            prefix = 0

        if( val_mask > 0 ):
            quant = num // mod
            val = val + quant
            num = num % mod
            mod = mod // 256
                
        ret_val += varint_storage( val )
        val_mask = 0xFF

    return ret_val

def decode( num ):
    return generic_decode( num, funcs )

def decode_val( num ):
    first = store_to_num( num[ 0 ] )
    for b in buckets:
        if(( first & ~b['val_mask'] ) == b['prefix'] ):
            val_mask = b['val_mask']
            mod = b['mod']
            break

    bytes_used = 0
    ret_val = 0
    while mod>0:
        val = store_to_num( num[ bytes_used ] )
        if( val_mask < 255 ):
            val = val & val_mask
            val_mask = 255
        ret_val = ret_val + (mod * val)
        mod = mod // 256
        bytes_used = bytes_used + 1

    return ( ret_val, bytes_used )

funcs = { 'decode_val': decode_val,
          'encode_int': encode_int }
