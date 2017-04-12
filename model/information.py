#!/usr/bin/env python

'''
Module containing mathematical functions commonly used in information theory.
'''

from math import log

def sum_naturals(arr):
    '''
    Return the sum of a list of nonnegative integers.
    '''
    n_sum = 0 # empty sum
    for n in arr:
        if n % 1 != 0 or n < 0: # nonnegative integer check
            raise Exception("information.py:entropy:n in arr must a nonnegative integer")
        n_sum = n_sum + n
    return int(n_sum)


def entropy(arr, base):
    '''
    Return entropy of arr in given base.
    '''
    n_sum = sum_naturals(arr) # sum arr
    if n_sum == 0:
        return 0
    result = 0 #empty sum
    for n in arr:
        if n > 0: # skip negative values of n
            p = n / n_sum
            result = result + p * log(p, base)
    if result == 0: # don't negate 0
        return result
    else:
        return -result

def gain(data, subsets, base):
    '''
    Return weighted difference in entropies.
    '''
    gain = entropy(data, base)
    dataSize = sum_naturals(data)
    for subset in subsets:
        gain = gain - sum_naturals(subset) / dataSize * entropy(subset, base)
    return gain

__author__ = "Miguel Amezola"
__copyright__ = "Copyright 2017, Miguel Amezola"
__credits__ = ["Miguel Amezola"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Miguel Amezola"
__email__ = "math@miguelamezola.com"
__status__ = "Production"
