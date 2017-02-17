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

# Based on the signed integer encoding method described at
#  https://en.wikipedia.org/wiki/LEB128

from ..varints import varint_storage,empty_varint_storage,num_types,generic_encode,generic_decode
from ..varints import store_to_num

def encode( num ):
    return generic_encode( num, funcs )

def decode( num ):
    return generic_decode( num, funcs )

def encode_int( num ):
    ret_val = None
    working = num
    more = True
    
    while( more ):

        byte = working & 0x7F
        working = working >> 7

        if( ((( working == 0 ) and (( byte & 0x40) == 0 )) or \
             (( working == -1 ) and (( byte & 0x40 ) != 0 ))) ):
            more = False
        else:
            byte = byte | 0x80

        if( ret_val is None ):
            ret_val = empty_varint_storage()

        ret_val = ret_val + varint_storage( byte )

    return ret_val

def decode_val( num ):
    # TODO: reconsile this with leb128u
    ret_val = None
    bytes_used = 0
    cont = True

    while cont:
        val = store_to_num( num[ bytes_used ] )
        if(( val & 0x80 ) == 0):
            cont = False
        val = val & 0x7F

        if ret_val is None:
            ret_val = 0

        ret_val = ret_val | (val << (7*bytes_used))

        bytes_used = bytes_used + 1

    if( val & 0x40 ):
        ret_val |= (-1 << (7*bytes_used))

    return( ret_val, bytes_used )

funcs = { 'decode_val': decode_val,
          'encode_int': encode_int }
