from sklearn.ensemble import BaggingClassifier
import random


def train(dataset, n_estimators, max_tree_depth, min_node_records):



    random.shuffle(dataset)

    x_train = dataset[:int((len(dataset)+1)*.70)]
    x_test = dataset[int((len(dataset)+1)*.30):]
    y_train = x_train
    y_test = x_test

    #bagging
    ensemble.fit(x_train, y_train)

    score = ensemble.score(x_test, y_test)

    save(score)
