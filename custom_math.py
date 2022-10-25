#!/usr/bin/env python3

# Import Packages
import math
import cmath
import numpy as np

# Matlab: Rounding
def m_round(value):
    my_round = np.vectorize(lambda x: round(x))
    result = my_round(value)
    return result

# Matlab: Index slicing
def m_slicing(start,stop,step):
    if start == stop:
        slices = np.array([start])
    else:
        slices = np.arange(start,stop,step)
        if stop % step == 0:
            slices = np.append(slices,stop)
    return slices

# Matlab: Magic function
def magic(n):
    n = int(n)
    if n < 2:
        raise ValueError("Size must be at least 2")
    if n == 2:
        M = np.array([[1,3],[4,2]])
    if n % 2 != 0:
        M = np.mod((np.arange(n)[:, None] + np.arange(n)) + (n-1)//2+1, n)*n + \
          np.mod((np.arange(1, n+1)[:, None] + 2*np.arange(n)), n) + 1
    elif n % 4 == 0:
        M = np.empty([n, n], dtype=int)
        M[:, :n//2] = np.arange(1, n**2//2+1).reshape(-1, n).T
        M[:, n//2:] = np.flipud(M[:, :n//2]) + (n**2//2)
        M[1:n//2:2, :] = np.fliplr(M[1:n//2:2, :])
        M[n//2::2, :] = np.fliplr(M[n//2::2, :])
    return M

## Matlab: Linear (2D) Array Indexing
## Index arrays along a single dimension
#def m_2DindexA(array,start,stop,step=1):
#    if start == stop:
#        array = np.array[start]
#    else:
#        array = array[start:(stop + 1):step]
#    return array
#    
## Matlab: List Indexing
#def m_indexL(list,start,stop,step=1):
#    if start == stop:
#        newlist = list[start]
#    else:
#        newlist = list[start:stop:step]
#        if stop % step == 0:
#            newlist.append(stop)
#    return newlist

# General: Distance formula
def distance(x1,x2,y1,y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist
