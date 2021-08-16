# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 18:37:41 2021
Used to pull my map key from mapbox from a text file. Makes the process easy for the map 
@author: jpl922
"""



# Defining functions at start 
# Function to compare the location list 

def loc_in_list(loc, loc_list):

    loc_list = list(set([i.strip().lower() for i in loc_list if len(i.strip().lower()) > 0]))
    loc_list += ['the ' + i for i in loc_list if i[:4] != 'the ']
    loc_list += [i[4:] for i in loc_list if i[:4] == 'the ']

    for t_char in ["'", "-"]:
        loc_list += [i.replace(t_char, "") for i in loc_list if t_char in i]
        loc_list += [i.replace(t_char, " ") for i in loc_list if t_char in i]
    
    loc = loc.replace("’", "'")
    loc = loc.strip().lower()
    
    loc_in_list_bool = (loc in loc_list) or (loc.replace("'", "") in loc_list)

    return loc_in_list_bool 


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
# can use the os to find directory 

# this code does not work ( find the issue) ( )

#data_dir = 'data_csvs'
# ends with not ends width 
# data_files = [i for i in os.listdir(data_dir) if i.endswidth('.csv')]

# for csv_file in data_files: 
#     with open(os.path.join(data_dir, csv_file),'r') as f:
#         locs_txt = f.read()
#     temp_locs = locs_txt.split('\n')
#     locs_bool = [loc_in_list(i, temp_locs) for i in list(loc_df['location'])]
#     loc_df = loc_df.assign(**{csv_file: locs_bool})
    
# loc_df = loc_df.assign(counts=loc_df[data_files].sum(axis=1))
# loc_df.sort_values(by='counts', inplace=True, ascending=False)

## Fixed adding most  popular destination

data_dir = 'data_csvs'
data_files = [i for i in os.listdir(data_dir) if i.endswith('.csv')]

for csv_file in data_files: 
    with open(os.path.join(data_dir, csv_file),'r') as f:
        locs_txt = f.read()
    temp_locs = locs_txt.split('\n')
    locs_bool = [loc_in_list(i, temp_locs) for i in list(loc_df['location'])]
    loc_df = loc_df.assign(**{csv_file: locs_bool})
    
loc_df = loc_df.assign(counts=loc_df[data_files].sum(axis=1))
loc_df.sort_values(by='counts', inplace=True, ascending=False)

# plotting again with the most popular desination 

fig = px.scatter_mapbox( loc_df, lat="lat", lon="lon", color = "type", 
size="counts", hover_name='location', hover_data =['type'], zoom=12, size_max = 15)
fig.update_layout(mapbox_style = "light", mapbox_accesstoken=mapboxkey)
fig.show()



# dealing with overlapping areas on the map 

loc_df = loc_df.assign(dup_row=0)
loc_thresh = 0.0001

for i in range(len(loc_df)): 
    src_ind = loc_df.iloc[i].name
    for j in range (i+1, len(loc_df)): 
        tgt_ind = loc_df.iloc[j].name 
        lat_dist = loc_df.loc[src_ind]['lat'] - loc_df.loc[tgt_ind]['lat']
        lon_dist = loc_df.loc[src_ind]['lon']-loc_df.loc[tgt_ind]['lon']
        tot_dist = (lat_dist ** 2 + lon_dist ** 2) ** 0.5
        if tot_dist < loc_thresh: 
            print(f'Found duplicate item "{loc_df.loc[tgt_ind]["location"]}", index {tgt_ind}')
            for csv_file in data_files:
                if loc_df.loc[tgt_ind, csv_file]:
                    loc_df.loc[src_ind, csv_file] = True 
                if loc_df.loc[tgt_ind, 'location'] not in loc_df.loc[src_ind, 'location']: 
                    loc_df.loc[src_ind, 'location'] = loc_df.loc[src_ind, 'location'] + ' | ' + loc_df.loc[tgt_ind, 'location']
                    loc_df.loc[tgt_ind, 'dup_row'] = 1
loc_df = loc_df[loc_df.dup_row == 0]
loc_df = loc_df.assign(counts=loc_df[data_files].sum(axis=1))
loc_df.sort_values(by='counts', inplace=True, ascending=False)

# plotting without overlaps

fig = px.scatter_mapbox(loc_df, lat="lat", lon = "lon", color="type", size = "counts", hover_name = 'location', hover_data = ['type'], zoom=12, size_max=15)
fig.update_layout(mapbox_style = "light", mapbox_accesstoken=mapboxkey)
fig.show( config ={'displayModeBar': False, 'editable': False, }, )


