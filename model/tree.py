#!/usr/bin/env python

from math import log

class DecisionTree:

    def __init__(self, max_depth, min_size):
        self.max_depth = max_depth
        self.min_size = min_size
        self.n_features = 0
        self.root = None

    # build a decision tree
    def fit(self, X, y):
        if len(X) != len(y):
            raise ValueError("the number of samples in X must be equal to the number of labels in y")

        dataset = list()

        for index, row in enumerate(X):
            if self.n_features == 0:
                self.n_features = len(row)
            elif self.n_features != len(row):
                raise ValueError("all samples are not the same length")
            sample = row + [y[index]]
            dataset.append(sample)
        print(dataset)
        self.root = self.get_split(dataset)
        self.split(self.root, self.max_depth, self.min_size, 1)
        return self.root

    def predict(self, sample):
        return self.predict_helper(self.root, sample)

    def predict_helper(self, node, sample):
        if sample[node['index']] < node['value']:
            if isinstance(node['left'], dict):
                return self.predict_helper(node['left'], sample)
            else:
                return node['left']
        else:
            if isinstance(node['right'], dict):
                return self.predict_helper(node['right'], sample)
            else:
                return node['right']


    def print(self, depth=0):
        self.print_helper(self.root)

    # Print a decision tree
    def print_helper(self, node, depth=0):
        if isinstance(node, dict):
            print('%s[X%d < %.3f]' % ((depth*' ', (node['index']+1), node['value'])))
            self.print_helper(node['left'], depth+1)
            self.print_helper(node['right'], depth+1)
        else:
            print('%s[%s]' % ((depth*' ', node)))

    # create child splits for a node or make terminal
    def split(self, node, max_depth, min_size, depth):

        left, right = node['groups']
        del(node['groups'])

        # check for a no split
        if not left or not right:
            node['left'] = node['right'] = self.to_terminal(left + right)
            return
        # check for max depth
        if depth >= max_depth:
            node['left'], node['right'] = self.to_terminal(left), self.to_terminal(right)
            return

        # process left child
        if len(left) <= min_size:
            node['left'] = self.to_terminal(left)
        else:
            node['left'] = self.get_split(left)
            self.split(node['left'], max_depth, min_size, depth+1)
        # process right child
        if len(right) <= min_size:
            node['right'] = self.to_terminal(right)
        else:
            node['right'] = self.get_split(right)
            self.split(node['right'], max_depth, min_size, depth+1)

    # terminal node value
    def to_terminal(self, dataset):
        outcomes = [row[-1] for row in dataset]
        return max(set(outcomes), key=outcomes.count)

    # split a dataset based on an attribute and an attribute value
    def test_split(self, feature_index, feature_value, dataset):
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
    def get_split(self, dataset):
        b_index, b_value, b_gain, b_groups = 999, 999, 0, None
        for index in range(len(dataset[0]) - 1): # assume all rows in dataset are of the same length
            for row in dataset:
                groups = self.test_split(index, row[index], dataset)
                gain = self.binary_entropy_gain(dataset, groups, 2) # shannon entropy uses log base 2
                #print(index, row[index], subsets, gain)
                if gain >= b_gain:
                        b_index, b_value, b_gain, b_groups = index, row[index], gain, groups
        return { "index": b_index, "value": b_value, "groups": b_groups }

        
    def binary_entropy_gain(self, dataset, subsets, base):
        '''
        Return weighted difference in entropies.
        '''
        gain = self.binary_entropy(dataset, base)
        data_size = len(dataset)
        num_subset_samples = 0

        for subset in subsets:
            sample_size = len(subset)
            num_subset_samples += sample_size
            gain = gain - sample_size / data_size * self.binary_entropy(subset, base)
            # print(sample_size, data_size, binary_entropy(subset, base))

        if data_size != num_subset_samples:
            raise ValueError("number of samples in dataset does not equal number of samples in all subsets")
        return gain

    def binary_entropy(self, dataset, base):

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
