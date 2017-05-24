# titanic

Using decision trees to predict survival on the RMS Titanic.

## Demo
To run the demo, use the command line to navigate to the ./model/ directory. Then run "python3 demo.py"

## Import into Python Interpreter
Navigate to the ./model directory. Then run "python3" and enter the following:

```
>>> import features
>>> import tree
>>> X,y = features.get_data()
>>> clf = tree.DecisionTreeClassifier(3,1)
>>> clf.fit(X,y)
>>> clf.predict([1,2,3,4,5,6,7,8,9,10])
```

The predict method takes a single row vector with entries that represent the following passenger features:

```
1:"Ticket Class",
2:"Sex",
3:"Age",
4:"Sibsp",
5:"Parch",
6:"Embark Point",
7:"Title",
8:"Family Size",
9:"Age Interval",
10:"Deck"}
```

Please see the ./preprocessing/features.json file for examples.

