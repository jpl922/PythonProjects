# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 00:46:27 2021
Following another medium article from Hwang and NBA travel
@author: @jpl922
"""


# import libraries 
import pandas as pd 
import plotly.express as px 
import plotly.io as pio 




# Arena Location information 

arena_csv = 'C:/Users/17jlo/Desktop/PythonCode/PythonProjects/Maps/nba_travel/srcdata/arenas_list.csv'
arena_df = pd.read_csv(arena_csv)
arena_df = arena_df.assign(full_loc=arena_df.arena_name + ', ' + arena_df.arena_city)

# creating a function for obtaining locations 

def get_loc_resp(srch_str):
    
    
    import time 
    import requests
    
    with open('../LocationIQToken.txt','r') as f:
        prv_tkn = f.read().strip()
        
    # 2 request/second based on limit 
    time.sleep(0.5) 
    
    API_url = "https://us1.locationiq.com/v1/search.php?key=" + prv_tkn + "&q=" + srch_str + "&format=json"
    loc_resp = requests.get(API_url)
    
    return loc_resp

def get_lat_long(srch_str):
    
    import json
    
    try: 
        