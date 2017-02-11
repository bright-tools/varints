ASCII Representation of Integers (AROI)
=======================================

[![Build Status](https://travis-ci.org/bright-tools/aroi.svg?branch=master)](https://travis-ci.org/bright-tools/aroi)

This is a Python module which is intended to assist with encoding integers (and
lists of integers) into more compact ASCII representations which use less
memory.

The motive for this module was initially during a large tree-search program
that I was implementing.  Each node in the tree had a list of integers
associated with it, but as the number of nodes grew, the memory occupied by the
millions of Python arrays became significant.  Encoding the content of the
arrays into strings, then decoding when required resulted in significant savings
when considering hundreds of thousands of nodes.
