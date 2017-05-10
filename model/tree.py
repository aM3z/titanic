#!/usr/bin/env python

from math import log

# build a decision tree
def fit(dataset, max_depth, min_size):
    root = get_split(dataset)
    split(root, max_depth, min_size, 1)
    return root

# Print a decision tree
def print_tree(node, depth=0):
    if isinstance(node, dict):
        print('%s[X%d < %.3f]' % ((depth*' ', (node['index']+1), node['value'])))
        print_tree(node['left'], depth+1)
        print_tree(node['right'], depth+1)
    else:
        print('%s[%s]' % ((depth*' ', node)))

# create child splits for a node or make terminal
def split(node, max_depth, min_size, depth):

    left, right = node['groups']
    del(node['groups'])

    # check for a no split
    if not left or not right:
        node['left'] = node['right'] = to_terminal(left + right)
        return
    # check for max depth
    if depth >= max_depth:
        node['left'], node['right'] = to_terminal(left), to_terminal(right)
        return

    # process left child
    if len(left) <= min_size:
        node['left'] = to_terminal(left)
    else:
        node['left'] = get_split(left)
        split(node['left'], max_depth, min_size, depth+1)
    # process right child
    if len(right) <= min_size:
        node['right'] = to_terminal(right)
    else:
        node['right'] = get_split(right)
        split(node['right'], max_depth, min_size, depth+1)

# terminal node value
def to_terminal(dataset):
    outcomes = [row[-1] for row in dataset]
    return max(set(outcomes), key=outcomes.count)

# split a dataset based on an attribute and an attribute value
def test_split(feature_index, feature_value, dataset):
    left, right = list(), list()
    # assume last entry in row is label not feature
    if feature_index >= len(dataset[0]) - 1:
        raise ValueError("feature_index out of range")
    for row in dataset:
        if row[feature_index] < feature_value:
            left.append(row)
        else:
            right.append(row)
    return left, right

# select the best split
def get_split(dataset):
    b_index, b_value, b_gain, b_groups = 999, 999, 0, None
    for index in range(len(dataset[0]) - 1): # assume all rows in dataset are of the same length
        for row in dataset:
            groups = test_split(index, row[index], dataset)
            gain = binary_entropy_gain(dataset, groups, 2) # shannon entropy uses log base 2
            #print(index, row[index], subsets, gain)
            if gain >= b_gain:
                    b_index, b_value, b_gain, b_groups = index, row[index], gain, groups
    return { "index": b_index, "value": b_value, "groups": b_groups }

    
def binary_entropy_gain(dataset, subsets, base):
    '''
    Return weighted difference in entropies.
    '''
    gain = binary_entropy(dataset, base)
    data_size = len(dataset)
    num_subset_samples = 0

    for subset in subsets:
        sample_size = len(subset)
        num_subset_samples += sample_size
        gain = gain - sample_size / data_size * binary_entropy(subset, base)
        # print(sample_size, data_size, binary_entropy(subset, base))

    if data_size != num_subset_samples:
        raise ValueError("number of samples in dataset does not equal number of samples in all subsets")
    return gain

def binary_entropy(dataset, base):

    num_samples = len(dataset)
    if num_samples == 0:
        return 0

    pos = 0
    for sample in dataset:
        pos += sample[-1]
    neg = num_samples - pos

    p = pos / num_samples
    q = neg / num_samples

    entropy = 0

    if p > 0:
        entropy +=  p * log(p, base)
    if q > 0:
        entropy +=  q * log(q, base)

    if entropy != 0:
        return -entropy
    return entropy



__author__ = "Miguel Amezola"
__copyright__ = "Copyright 2017, Miguel Amezola"
__credits__ = ["Miguel Amezola"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Miguel Amezola"
__email__ = "math@miguelamezola.com"
__status__ = "Production"
