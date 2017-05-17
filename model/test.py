import features
from tree import DecisionTreeClassifier as our_tree
from sklearn import tree as py_tree
from sklearn.ensemble import BaggingClassifier
import argparse

RESULTS_DIR = './results/testing/'

def tree(max_depth, start_min_sample_size, end_min_sample_size):
    
    X,y = features.get_data()
    # use first 0.7 for training
    X_train, y_train = X[:624], y[:624]
    X_test, y_test = X[624:], y[624:]

    results_filename = RESULTS_DIR + "tree.csv"
    with open(results_filename, "a") as f:
        for s in range(start_min_sample_size, end_min_sample_size + 1):

            clf = our_tree(max_depth,s)
            clf.fit(X_train, y_train)
            score = clf.score(X_test, y_test)
            result = "%d, %d, %f\n" % (max_depth, s, score)

            print(result)
            f.write(result)

def bagging(n_estimators, random_state, start_max_depth, end_max_depth, start_min_sample_size, end_min_sample_size):

    X,y = features.get_data()
    # use first 0.7 for training
    X_train, y_train = X[:624], y[:624]
    X_test, y_test = X[624:], y[624:]

    results_filename = RESULTS_DIR + "bagging.csv"

    with open(results_filename, "a") as f:
        for d in range(start_max_depth, end_max_depth + 1):
            for s in range(start_min_sample_size, end_min_sample_size + 1):
         
                their_tree = py_tree.DecisionTreeClassifier(criterion='entropy', max_depth=d,random_state=random_state, min_samples_split=s)
                clf = BaggingClassifier(base_estimator=their_tree, n_estimators=n_estimators, random_state=random_state)
                clf.fit(X_train, y_train)
                score = clf.score(X_test, y_test)
                result = "%d, %d, %d, %f\n" % (n_estimators, d, s, score)

                print(result)
                f.write(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train Decision Tree and Bagging Classifiers")

    parser.add_argument('-m', metavar='model', dest='model', type=int, nargs='?', help='1 for bagging, 2 for tree, 3 for bagging and tree')
    parser.add_argument('-n', metavar='estimators', dest='n', type=int, nargs='?', help='number of estimators used for bagging')
    parser.add_argument('-r', metavar='random_state', dest='rand', type=int, nargs='?', help='random state')
    parser.add_argument('-d', metavar='start_max_depth', dest='d', type=int, nargs='?', help='start max tree depth')
    parser.add_argument('-e', metavar='end_max_depth', dest='e', type=int, nargs='?', help='end max tree depth')
    parser.add_argument('-s', metavar='start_min_sample_size', dest='s', type=int, nargs='?', help='start min sample size')
    parser.add_argument('-t', metavar='end_min_sample_size', dest='t', type=int, nargs='?', help='end min sample size')


    args = parser.parse_args()

    if args.model == 1:
        bagging(n_estimators=args.n, random_state=args.rand, start_max_depth=args.d, end_max_depth=args.e, start_min_sample_size=args.s, end_min_sample_size=args.t)
    elif args.model == 2:
        tree(max_depth=args.d, start_min_sample_size=args.s, end_min_sample_size=args.t)
    elif args.model == 3:
        bagging(n_estimators=args.n, random_state=args.rand, start_max_depth=args.d, end_max_depth=args.e, start_min_sample_size=args.s, end_min_sample_size=args.t)
        tree(max_depth=args.d, start_min_sample_size=args.s, end_min_sample_size=args.t)



