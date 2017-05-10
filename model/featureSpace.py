import json
from io import TextIOBase
import random

def randomize(featureSpace, survived):
   ind_list = list(range(len(featureSpace)))
   print(ind_list)
   random.shuffle(ind_list)
   print(ind_list)
   featureGroup = []
   survival = []
   for index in ind_list:
      featureGroup.append(featureSpace[index])
      survival.append(survived[index])
   print(featureGroup)
   print(survival)
   return featureGroup, survival
   

def getData():
   featureSpace = json.loads(open("../../titanic/preprocessing/features.json").read())
   survived = json.loads(open("../../titanic/preprocessing/survived.json").read())
   featureSpace, survived = randomize(featureSpace, survived)
   return featureSpace, survived

getData()