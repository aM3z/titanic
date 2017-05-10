import json
from io import TextIOBase
import random

DATA_DIR = "../preprocessing/"

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
   

def get_data():
   featureSpace = json.loads(open(DATA_DIR + "features.json").read())
   survived = json.loads(open(DATA_DIR + "survived.json").read())
   featureSpace, survived = randomize(featureSpace, survived)
   return featureSpace, survived

