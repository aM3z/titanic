from sklearn.ensemble import BaggingClassifier
import random

'''
Module to provide easy use of the bagging meta-estimator.
'''

def train(dataset, n_estimators):



    random.shuffle(dataset)

    x_train = dataset[:int((len(dataset)+1)*.70)]
    x_test = dataset[int((len(dataset)+1)*.30):]

    random.shuffle(dataset)
    y_train = dataset[:int((len(dataset)+1)*.70)]
    y_test = dataset[int((len(dataset)+1)*.30):]

    #bagging
	bag = BaggingClassifier(n_estimators)

    bag.fit(x_train, y_train)

    score = bag.score(x_test, y_test)

    return score
