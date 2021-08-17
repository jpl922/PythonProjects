# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 18:22:18 2021
Setup a glacier map actually seems more interesting (trailheads etc..)

Plan 
Glacier national park; therefore montana map 
Try to do something with trail data 
Datas 
@author: @jpl922
"""


## Importing general libraries 
import pandas as pd 
import numpy as np 
import logging


## Plotly libraries and setup 
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go 

pio.renderers.default = 'browser'



## Creating the logger used by location functions 
logger = logging.getLogger(__name__)
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
root_logger.addHandler(sh)


## Defining the Functions for long/lat values 


# use location IQ token and send over requests to the server?  
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

#Function used to obtain the long/lat values for locations from the Location CSV

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



## Loading in the CSV file with relevant park information 

glacier_csv = '/GlacierNP.csv' # may need full directory 
glacier_df = pd.read_csv(glacier_csv)
glacier_df = glacier_df.assign() 
# look into the .assign and read_csv to figure out with dates



## Calling the Functions to determine long/lat 







