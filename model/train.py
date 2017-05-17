import features
from tree import DecisionTreeClassifier as our_tree
from sklearn import tree as py_tree
from sklearn.ensemble import BaggingClassifier
from sklearn.model_selection import cross_val_score
from statistics import mean
import argparse

RESULTS_DIR = './results/'
FOLDS = 3

def tree(folds, max_depth, min_sample_size):
    
    X,y = features.get_data()
    # use first 0.7 for training
    X_train, y_train = X[:624], y[:624]

    results_filename = RESULTS_DIR + "tree_f%d_md%d_mss%d.csv" % (folds, max_depth, min_sample_size)

    with open(results_filename, "w") as f:
        for depth in range(1, max_depth + 1):
            for sample_size in range(1, min_sample_size + 1): 
                clf = our_tree(depth,sample_size)
                scores = cross_val_score(clf, X_train, y_train, cv=folds)
                mean_score = mean(scores)
                result = "%d, %d, %f\n" % (depth, sample_size, mean_score)
                print(result)
                f.write(result)

def bagging(folds, n_estimators, random_state, max_depth, min_sample_size):
 
    X,y = features.get_data()
    # use first 0.7 for training
    X_train, y_train = X[:624], y[:624]

    results_filename = RESULTS_DIR + "bagging_f%d_e%d_rs%d_md%d_mss%d.csv" % (folds, n_estimators, random_state, max_depth, min_sample_size)

    with open(results_filename, "w") as f:
        for n in range(1, n_estimators + 1):
            for depth in range(1, max_depth + 1):
                for sample_size in range(1, min_sample_size + 1): 
                    their_tree = py_tree.DecisionTreeClassifier(criterion='entropy', max_depth=max_depth,random_state=random_state, min_samples_split=min_sample_size)
                    clf = BaggingClassifier(base_estimator=their_tree, n_estimators=n, random_state=random_state)
                    scores = cross_val_score(clf, X_train, y_train, cv=folds)
                    mean_score = mean(scores)
                    result = "%d, %d, %d, %f\n" % (n, depth, sample_size, mean_score)
                    print(result)
                    f.write(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train Decision Tree and Bagging Classifiers")

    parser.add_argument('-n', metavar='estimators', dest='n', type=int, nargs='?', help='number of estimators used for bagging')
    parser.add_argument('-r', metavar='random_state', dest='rand', type=int, nargs='?', help='random state')
    parser.add_argument('-d', metavar='max_depth', dest='d', type=int, nargs='?', help='max tree depth')
    parser.add_argument('-s', metavar='min_sample_size', dest='s', type=int, nargs='?', help='min sample size')

    args = parser.parse_args()

    # bagging(folds=FOLDS, n_estimators=args.n, random_state=args.rand, max_depth=args.d, min_sample_size=args.s)
    tree(folds=FOLDS, max_depth=args.d, min_sample_size=args.s)


