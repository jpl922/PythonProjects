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

import logging

# getting the rendering to work
pio.renderers.default = 'browser'

# setting up a logger 
logger = logging.getLogger(__name__)
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
root_logger.addHandler(sh)


# Arena Location information 

arena_csv = 'C:/Users/17jlo/Desktop/PythonCode/PythonProjects/Maps/nba_travel/srcdata/arenas_list.csv'
arena_df = pd.read_csv(arena_csv)
arena_df = arena_df.assign(full_loc=arena_df.arena_name + ', ' + arena_df.arena_city)

# creating a function for obtaining locations 

def get_loc_resp(srch_str):
    
    
    import time 
    import requests
    #"C:\Users\17jlo\Desktop\PythonCode\PythonProjects\Maps\LocationIQToken.txt"
    with open('C:/Users/17jlo/Desktop/PythonCode/PythonProjects/Maps/LocationIQToken.txt','r') as f:
        prv_tkn = f.read().strip()
        
    # 2 request/second based on limit 
    time.sleep(0.5) 
    
    API_url = "https://us1.locationiq.com/v1/search.php?key=" + prv_tkn + "&q=" + srch_str + "&format=json"
    loc_resp = requests.get(API_url)
    
    return loc_resp

def get_lat_long(srch_str):
    
    import json
    # {} can be used to display a variable within the text string 
    try:
        logger.info(f'Searching for {srch_str}')
        loc_resp = get_loc_resp(srch_str)
        lat = json.loads(loc_resp.text)[0]['lat']
        lon = json.loads(loc_resp.text)[0]['lon']
        dispname = json.loads(loc_resp.text)[0]['display_name']
        logger.info(f'Found {dispname}')
    except:
        logger.exception('Something went wrong :(')
        lat = 0.0
        lon = 0.0
    return lat, lon 

arena_df = arena_df.assign(arena_loc=arena_df['full_loc'].apply(get_lat_long))
arena_df = arena_df.assign(lat = arena_df.arena_loc.apply(lambda x: x[0]).astype(float))
arena_df = arena_df.assign(lon = arena_df.arena_loc.apply(lambda x: x[1]).astype(float))

# .apply to the full_loc colum, looping through every entry through the get_lat_long
# returned array become arena_loc column 
# returned value is (lat, long) separated into lat/lon floating points 


# mapbox access token 
with open('MapKey.txt','r') as f: 
   mapboxkey = f.read().strip()


# plotting arenas 

fig = px.scatter_mapbox(arena_df, lat="lat", lon = "lon", zoom =3, hover_name = 'teamname')
fig.update_layout(mapbox_style="light",mapbox_accesstoken =mapboxkey) 
fig.show()



        