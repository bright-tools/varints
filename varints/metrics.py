#!/usr/bin/python

import varints
import sys
import random

SET_SIZE = 1000
LOOPS = 19

t=[0 for x in range(0,LOOPS)]
n=[0 for x in range(0,LOOPS)]
s=[0 for x in range(0,LOOPS)]
l=[0 for x in range(0,LOOPS)]
d=[0 for x in range(0,LOOPS)]
sf = " {} |" * (LOOPS)

top = 10
i = 1

for x in range(0,LOOPS):
    r = [random.randint(0,top) for _ in range( SET_SIZE )]
    t[x] = "range(0..10^{})".format(i)
    n[x] = sys.getsizeof( r )
    s[x] = sys.getsizeof( varints.sqliteu.encode( r ))
    l[x] = sys.getsizeof( varints.leb128u.encode( r ))
    d[x] = sys.getsizeof( varints.dlugoszu.encode( r ))

    top = top * 10
    i = i + 1

print("| representation | "+sf.format(*t))
print("| integer array  | "+sf.format(*n))
print("| leb128u        | "+sf.format(*s))
print("| sqliteu        | "+sf.format(*l))
print("| dlugoszu       | "+sf.format(*d))
