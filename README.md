Variable Length Integer Encoding
================================

[![Build Status](https://travis-ci.org/bright-tools/varints.svg?branch=master)](https://travis-ci.org/bright-tools/varints)

This is a Python module which is intended to assist with variable-length encoding integers (and lists of integers) into more compact representations which use less memory.

Generally in Python, integers are stored as [long](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-float-long-complex) meaning that they will use at least 32 bits.  When storing many numbers which do not require 32 bits, this becomes significantly wasteful; variable length representation can assist in such cases.
