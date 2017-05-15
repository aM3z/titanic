import features
import tree
from sklearn.ensemble import BaggingClassifier
from sklearn.model_selection import cross_val_score
from statistics import mean

RESULTS_DIR = './results/'

def tree(folds, tree_max_depth, tree_min_sample_size):
    
    X,y = features.get_data()
    # use first 0.7 for training
    X_train, y_train = X[:624], y[:624]

    results_filename = RESULTS_DIR + "tree_f%d_md%d_mss%d.csv" % (folds, tree_max_depth, tree_min_sample_size)
    with open(results_filename, "w") as f:
        for depth in range(1, tree_max_depth):
            for sample_size in range(1, tree_min_sample_size): 
                clf = tree.DecisionTreeClassifier(depth,sample_size)
                scores = cross_val_score(clf, X_train, y_train, cv=folds)
                mean_score = mean(scores)
                result = "%d, %d, %f\n" % (depth, sample_size, mean_score)
                print(result)
                f.write(result)

def bagging(folds, n_estimators):
 
    X,y = features.get_data()
    # use first 0.7 for training
    X_train, y_train = X[:624], y[:624]

    results_filename = RESULTS_DIR + "bagging_f%d_e%d.csv" % (folds, n_estimators)
    with open(results_filename, "w") as f:
        for n in range(1, n_estimators):
            clf = BaggingClassifier(n_estimators=n)
            scores = cross_val_score(clf, X_train, y_train, cv=folds)
            mean_score = mean(scores)
            result = "%d, %f\n" % (n, mean_score)
            print(result)
            f.write(result)


