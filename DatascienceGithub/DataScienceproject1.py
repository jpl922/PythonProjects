# -*- coding: utf-8 -*-
"""
Created on Sat May 29 22:01:14 2021
Starting github datascience projects learning basics in python
https://www.youtube.com/watch?v=T5pRlIbr6gg

Main Takeaway ML is much easier when not coded from scratch 


@author: Jason @jpl922
"""

from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import NearestCentroid
import numpy as np
# [ height, weight, shoe size]

X = [ [181,80,44], [177, 70, 43],[160, 60, 38], [154, 54, 37 ], [166,65,40], [190,90,47], [175,64,39], [177,70,40], [159,55,37],[171,75,42], [181,85,43]]

Y = ['male', 'female', 'female', 'female','male','male', 'male', 'female', 'male','female','male']

# clf: will be classifiere storage variable 
clf = tree.DecisionTreeClassifier()

clf = clf.fit(X,Y) # train classifier on the dataset

prediction = clf.predict([[190,70,43]]) # predict based on dataset 

print(prediction) 


# Challenge 
# Use any 3 scikit-learn models on the dataset (X,Y)
# compare results 
# print the best one 

# Random forest 
RFclf = RandomForestClassifier(n_estimators = 10)
RFclf = RFclf.fit(X,Y)

RFprediction = RFclf.predict([[190,70,43]])
print(RFprediction)


# Neural Network 
NNclf = MLPClassifier(solver = 'lbfgs',alpha = 1e-5, hidden_layer_sizes= (5,3), random_state = 1)
NNclf.fit(X,Y)
MLPClassifier(alpha = 1e-05, hidden_layer_sizes=(5,3),random_state = 1, solver = 'lbfgs')

NNPrediction = NNclf.predict([[190,70,43]])

print(NNPrediction) # these are overwriting 

# Nearest Centroid 
X2 = np.array(X)
Y2 = np.array(Y)

NCclf = NearestCentroid()
NCclf = NCclf.fit(X2,Y2)
NearestCentroid()
print(NCclf.predict([[190,70,43]]))
