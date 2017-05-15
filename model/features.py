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
   

def get_data(rand=False):
   featureSpace = json.loads(open(DATA_DIR + "features.json").read())
   survived = json.loads(open(DATA_DIR + "survived.json").read())
   if rand:
        featureSpace, survived = randomize(featureSpace, survived)
   return featureSpace, survived

def get_feature_labels():
   labels = {0:"Passenger ID",
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
   return labels
