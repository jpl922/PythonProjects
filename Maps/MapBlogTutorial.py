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

import os


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
#fig = px.scatter_mapbox(loc_df, lat="lat", lon = "lon", color = "type")
#fig.update_layout(mapbox_style="open-street-map")
#fig.show()

#modifying the map parameters 
fig = px.scatter_mapbox(loc_df, lat = "lat", lon = "lon", color = "type",
hover_name = 'location', hover_data = ['type'], zoom = 12)

# now also adding mapbox 
fig.update_layout(mapbox_style = "light", mapbox_accesstoken = mapboxkey)
fig.show()


# start at finding the most popular 
#https://towardsdatascience.com/interactive-maps-with-python-pandas-and-plotly-following-bloggers-through-sydney-c24d6f30867e


# Adding popular data destinations 

data_dir = 'data_csvs'
data_files = [ i for i in os.listdir(data_dir) if i.endswidth('.csv')]

for csv_file in data_files: 
    with open(os.path.join(data_dir, csv_file),'r') as f:
        locs_txt = f.read()
    temp_locs = locs_txt.split('\n')
    locs_bool = [loc_in_list(i,temp_locs) for i in list(loc_df['location'])]
    loc_df = loc_df.assign(**{csv_file: locs_bool})
    
loc_df = loc_df.assign(counts = loc_df[data_files].sum(axis=1))
loc_df.sort_values(by = 'counts', inplace=True, ascending=False)








