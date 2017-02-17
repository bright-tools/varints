#!/usr/bin/python

import varints
import sys
import random

SET_SIZE = 1000
LOOPS = 19
ITER = 10

t=[0 for x in range(0,LOOPS)]
num_array=[0 for x in range(0,LOOPS)]
sqlite=[0 for x in range(0,LOOPS)]
leb128u=[0 for x in range(0,LOOPS)]
d=[0 for x in range(0,LOOPS)]
leb128s=[0 for x in range(0,LOOPS)]
sf = " {:15} |" * (LOOPS)

top = 10
i = 1

for x in range(0,LOOPS):
    r = [random.randint(0,top) for _ in range( SET_SIZE )]
    t[x] = "range(0..10^{})".format(i)
    num_array[x] = sys.getsizeof( r )
    for loop in range(0,ITER):
        sqlite[x] = sqlite[x] + sys.getsizeof( varints.sqliteu.encode( r ))
        leb128u[x] = leb128u[x] + sys.getsizeof( varints.leb128u.encode( r ))
        leb128s[x] = leb128s[x] + sys.getsizeof( varints.leb128s.encode( r ))
        d[x] = d[x] + sys.getsizeof( varints.dlugoszu.encode( r ))

    sqlite[x] = int(sqlite[x] / ITER)
    leb128u[x] = int(leb128u[x] / ITER)
    leb128s[x] = int(leb128s[x] / ITER)
    d[x] = int(d[x] / ITER)

    top = top * 10
    i = i + 1

print("| representation |"+sf.format(*t))
print("| integer array  |"+sf.format(*num_array))
print("| leb128u        |"+sf.format(*leb128u))
print("| leb128s        |"+sf.format(*leb128s))
print("| sqliteu        |"+sf.format(*sqlite))
print("| dlugoszu       |"+sf.format(*d))
