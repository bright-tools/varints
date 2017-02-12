Variable Length Integer Encoding
================================

[![Build Status](https://travis-ci.org/bright-tools/varints.svg?branch=master)](https://travis-ci.org/bright-tools/varints)

This is a Python module which is intended to assist with variable-length encoding integers (and lists of integers) into more compact representations which use less memory.

Notes on Memory Usage
---------------------

Generally in Python, integers are stored as [long](https://docs.python.org/2/library/stdtypes.html#numeric-types-int-float-long-complex) meaning that they will use at least 32 bits.  When storing many numbers which do not require 32 bits, this would seem to be significantly wasteful; variable length representation should be able to assist in such cases.

Unfortunately, Python 2 gives us the following

```python
>>> import sys
>>> i = 1
>>> sys.getsizeof(i)
12
>>> b = bytearray([0] * 4)
>>> sys.getsizeof(b)
29
```

and the situation is no better in Python 3

```python
>>> import sys
>>> i = 1
>>> sys.getsizeof(i)
14
>>> b = bytearray([0] * 4)
>>> sys.getsizeof(b)
33
```

What we can see however is that the Python overhead for bytearray is fixed.  Increasing the size of the bytearray only increases the memory usage by the amount of bytes we've used:

```python
>>> import sys
>>> b1 = bytearray([0])
>>> sys.getsizeof(b1)
30
>>> b10 = bytearray([0] * 10)
>>> sys.getsizeof(b10)
40
```

So this means that currently:
* Memory overhead for bytearray objects is higher in Python 3 than Python 2
* Using varint encoding will actually *cost* us memory rather than saving us memory

If we consider arrays of numbers the situation is somewhat better.  If we take the example where we want to store ten zeros.  A varint encoding should mean that each zero can be stored in a single byte, meaning that we'd end up with a bytearray with 10 elements.  So ...

```python
>>> import sys
>>> i1 = [0] * 10
>>> i1
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
>>> sys.getsizeof(i1)
72
>>> b1 = bytearray(i1)
>>> sys.getsizeof(b1)
36
```

Meaning that:
* There is potential for saving memory by utilising varint encoding if we are storing arrays of integers
  * The amount of memory we save will depend on the numbers that are being stored.  The larger the varint representation, the smaller the saving, hence the more numbers will need to be stored in order to compensate for the bytearray overhead
* We will incur a processing overhead in order to save this memory.  e.g.  
  * Random access to varints stored in a bytearray would be O(n) rather than O(1)
  * We will incur an overhead each time we want to convert to and from varint representation

So why use varint in Python?  In the case that we need a compact method to store a list of (frequently small) numbers, and we do not generally need random access to the numbers contained.

One application is during [tree-search](https://en.wikipedia.org/wiki/Search_tree).  Typically we will end up with a number of nodes held in memory and not being accessed while other nodes in the tree are being processed.  If we want to store a state associated with each node (e.g. pieces on a chess board), then we can represent these as as list of integers and minimise the memory usage by using varint representations.
