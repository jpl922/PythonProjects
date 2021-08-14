# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 19:15:05 2021
https://www.youtube.com/watch?v=9gBC9R-msAk&list=PL2-dafEMk2A6QKz1mrk1uIGfHkC1zZ6UU&index=4
Following a recommender system tutorial for a project with lightFM
@author: Jason @jpl922
"""

import numpy as np
from lightfm.datasets import fetch_movielens
from lightfm import LightFM


# Fetch data and format it 
data = fetch_movielens(min_rating = 4.0)

# print training and testing data
print(repr(data['train']))
print(repr(data['test']))

# create the model

model = LightFM(loss='warp')# weighted approximate rank; gradient descent

#train model
model.fit(data['train'],epochs = 30, num_threads = 2)

def sample_recommendation(model, data, user_ids):
    # number of users and movies in training data 
    n_users, n_items = data['train'].shape
    
    # generate recommendations for each user we input 
    for user_id in user_ids:
        # movies they already like 
        known_positives = data['item_labels'][data['train'].tocsr()[user_id].indices]
        
        # movies our model predicts they will like 
        scores = model.predict(user_id, np.arange(n_items))
        # rank from most to least liked 
        top_items = data['item_labels'][np.argsort(-scores)]
        
        # print out results
        print("User %s" % user_id)
        print("    Known positives:")
        
        for x in known_positives[:3]:
            print("              %s" %x)
            
        print("    Recommended:")
        
        for x in top_items[:3]:
            print("       %s" %x)
            
sample_recommendation(model, data, [3, 25, 450]) # 3 random user ids
