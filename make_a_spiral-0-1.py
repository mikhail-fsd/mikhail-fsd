import numpy as np
import math
"""
martix size >= 5

"""

def sp1(size):

    spiral = np.zeros((size, size), dtype='int8')
    for x in range(math.ceil(size/2)):
        if x % 2 == 1:
            spiral[x:size-x, x:size-x] = 0
            spiral[x+1, x] = 1
        else:
            spiral[x:size-x, x:size-x] = 1
            spiral[x+1, x] = 0
    if size % 2 == 0 and x % 2 == 1: spiral[x+1, x] = 0 
    return spiral

def sp2(size):

    spiral = np.zeros((size, size), dtype='int8')
    for x in range(math.ceil(size/2)):
            spiral[x:size-x, x:size-x] = 1 - x%2
            spiral[x+1, x] = 0 + x%2
    if size % 2 == 0 and x % 2 == 1: spiral[x+1, x] = 0 
    return spiral.tolist()


