# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 18:37:41 2021
Used to pull my map key from mapbox from a text file. Makes the process easy for the map 
@author: jpl922
"""
import pandas as pd 
import plotly.express as px
# need to set the renderer
import plotly.io as pio
pio.renderers.default = 'browser'



# Used to read the map key and use it within the program 
with open('MapKey.txt','r') as f: 
    mapboxkey = f.read().strip()


# creating data frames for location data
# pd.read_csv; filepath step 1: copy path step 2: flip slashes 
loc_df = pd.read_csv('C:/Users/17jlo/Desktop/PythonCode/PythonProjects/Maps/loc_data.csv',index_col = 0)
print(loc_df.head())


# list types of columns 
columntypes = loc_df.type.unique()
# manipulate loc_df to replace NaN with Misc
loc_df.type.fillna('Misc',inplace=True) 

# first map need to make sure default renderer is set 
fig = px.scatter_mapbox(loc_df, lat="lat", lon = "lon", color = "type")
fig.update_layout(mapbox_style="open-street-map")
fig.show()