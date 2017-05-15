#!/usr/bin/env python

from math import log
import time
import pydot

VIZ_DIR = "./viz/"

class DecisionTreeClassifier:

    def __init__(self, max_depth, min_samples_split, criterion='entropy'):
        self.max_depth = max_depth
        self.min_size = min_samples_split
        self.criterion = 'entropy'
        self.n_features = 0
        self.root = None

    def get_params(self, deep=False):
        return {'criterion':  self.criterion, 'min_samples_split': self.min_size, 'max_depth': self.max_depth}

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
        self.root = self.get_split(dataset)
        self.split(self.root, self.max_depth, self.min_size, 1)

    def score(self, X_test, y_test):
        predictions = list()
        for sample in X_test:
            predictions.append(self.predict(sample))
        return self.accuracy_metric(y_test, predictions)

    def accuracy_metric(self, actual, predicted):
        correct = 0
        for i in range(len(actual)):
            if actual[i] == predicted[i]:
                correct += 1
        return correct / float(len(actual))

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

    def export_png(self, out_file="tree.dot"):
        self.export_graphviz(VIZ_DIR + out_file)
        (graph,) = pydot.graph_from_dot_file(VIZ_DIR + out_file)
        graph.write_png(VIZ_DIR + out_file + ".png")


    def export_graphviz(self, out_file="tree.dot"):
        with open(out_file, "w") as f:
            f.write("digraph Tree {\nnode [shape=box] ;\n")
            f.write(self.export_graphviz_helper(self.root))
            f.write("}")

    def export_graphviz_helper(self, node, pid=None, side=None):
        nid = str(time.time())
        if isinstance(node, dict):
            #if pid is None:
            #    nid = "1"
            #else:
            #    nid = str(node['index']+1) + str(node['value'])
            result = '%s [label="X[%d] <= %.3f\\ngain = %.3f\\nsamples = %d"] ;\n' % ((nid, (node['index']+1), node['value'], node["gain"], node['samples']))
            # print('%s [label="X[%d] <= %.3f\\ngain = %.3f\\nsamples = %d"] ;' % ((nid, (node['index']+1), node['value'], node["gain"], node['samples'])))
            if pid is not None:
                result += "%s -> %s ;\n" % (pid, nid)
                #print("%s -> %s ;" % (pid, nid))
            result += self.export_graphviz_helper(node['left'], nid, side=0)
            result += self.export_graphviz_helper(node['right'], nid, side=1)
        else:
            #predictions = node['left'] + node['right']
            #pos = 0
            #for prediction in predictions:
            #    pos += prediction
            #neg = len(predictions) - pos
            if node == 1:
                node = "Survive"
                color = "green"
            else:
                node = "Die"
                color = "red"
            # print('%s [label="%s"] ;' % (nid, node))
            # print("%s -> %s ;" % (pid, nid))
            result = '%s [label = "%s", color = %s] ;\n' % (nid, node, color)
            #result = '%s [label = "pos: %d, neg: %d"] ;\n' % (nid, pos, neg)
            result += "%s -> %s ;\n" % (pid, nid)

        return result


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
        return { "index": b_index, "value": b_value, "groups": b_groups, "samples": len(dataset), "gain": b_gain }

        
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
