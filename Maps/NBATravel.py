# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 00:46:27 2021
Following another medium article from Hwang and NBA travel

look up brackets and braces within python main [][]
https://medium.com/swlh/interactive-animated-travel-data-visualizations-mapping-nba-travel-a154a2e7c18d
@author: @jpl922
"""


# import libraries 
import pandas as pd 
import plotly.express as px 
import plotly.io as pio 
import plotly.graph_objects as go # more control 
import logging
import numpy as np

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



# Team color dictionary
teamcolor_dict = {
    'Atlanta Hawks': '#e03a3e',
    'Boston Celtics': '#008348',
    'Brooklyn Nets': 'Black',
    'Charlotte Hornets': '#1d1160',
    'Chicago Bulls': '#ce1141',
    'Cleveland Cavaliers': '#6f2633',
    'Dallas Mavericks': '#0053bc',
    'Denver Nuggets': '#8b2332',
    'Detroit Pistons': '#1d428a ',
    'Golden State Warriors': '#006bb6',
    'Houston Rockets': '#ce1141',
    'Indiana Pacers': '#fdbb30',
    'Los Angeles Clippers': '#1d428a',
    'Los Angeles Lakers': '#552583',
    'Memphis Grizzlies': '#5d76a9',
    'Miami Heat': '#98002e',
    'Milwaukee Bucks': '#00471b',
    'Minnesota Timberwolves': '#0c2340',
    'New Orleans Pelicans': '#b4975a',
    'New York Knicks': '#f58426',
    'Oklahoma City Thunder': '#f05133',
    'Orlando Magic': '#0077c0',
    'Philadelphia 76ers': '#002b5c',
    'Phoenix Suns': '#e56020',
    'Portland Trail Blazers': '#e03a3e',
    'Sacramento Kings': '#5b2b82',
    'San Antonio Spurs': '#000000',
    'Toronto Raptors': '#cd1141',
    'Utah Jazz': '#002b5c',
    'Washington Wizards': '#002b5c'
}
teamcolor_dict = {k.replace(' ', '_').upper(): v for k, v in teamcolor_dict.items()}



# Function ( copied for cleaner chart format)
def clean_chart_format(fig, namelocs=(0.9, 0.02)):

    import plotly.graph_objects as go

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        annotations=[
            go.layout.Annotation(
                x=namelocs[0],
                y=namelocs[1],
                showarrow=False,
                text="@jpl922",
                xref="paper",
                yref="paper",
                textangle=0
            ),
        ],
    )
    fig.update_traces(marker=dict(line=dict(width=1, color='Navy')),
                      selector=dict(mode='markers'))
    fig.update_traces(marker=dict(line=dict(color='navy')))
    fig.update_coloraxes(
        colorbar=dict(
            thicknessmode="pixels", thickness=15,
            outlinewidth=1,
            outlinecolor='#909090',
            lenmode="pixels", len=300,
            yanchor="top",
            y=1,
        ))
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    return True









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


### Look into using python path manager in the future 



# adding age and capacity to the map
from datetime import datetime 

cur_yr = datetime.today().year 

arena_df = arena_df.assign(age=(cur_yr-arena_df.opened))
arena_df = arena_df.assign(capacity = arena_df.capacity.str.replace(',','').astype(int))

fig = px.scatter_mapbox(arena_df,lat="lat",lon="lon",zoom=3, size = 'capacity', color = 'age', size_max=15, hover_name='teamname')
fig.update_layout(mapbox_style="light",mapbox_accesstoken=mapboxkey)
fig.show()


# Team travel data ( can use the long/lat for distance travelled)

schedule_df = pd.read_csv('C:/Users/17jlo/Desktop/PythonCode/PythonProjects/Maps/nba_travel/srcdata/2020_nba_schedule.csv', index_col=0)
arena_df = arena_df.assign(teamupper=arena_df.teamname.str.replace(' ','_').str.upper())


# Function to determine home arena

def get_home_arena(teamname): 
    rows = arena_df[arena_df.teamupper == teamname]
    
    return rows 


schedule_df = schedule_df.assign(lat=schedule_df.home_team.apply(lambda x: get_home_arena(x)['lat'].values[0]))
schedule_df = schedule_df.assign(lon=schedule_df.home_team.apply(lambda x: get_home_arena(x)['lon'].values[0]))

travel_data_list = list()

for teamname in schedule_df.home_team.unique():
    import math 
    team_sch = schedule_df[(schedule_df.away_team == teamname) | (schedule_df.home_team == teamname)]
    team_sch = team_sch.assign(dist=0)
    team_sch.reset_index(drop=True, inplace=True)
    for i, row in team_sch.iterrows():
        if i > 0: 
            # haversine formula implementation 
            avg_lat = (row['lat'] + team_sch.iloc[i-1]['lat'])/2
            lon_conv = math.cos(math.radians(avg_lat))
            lat1_rad = math.radians(team_sch.iloc[i-1]['lat'])
            lat2_rad = math.radians(row['lat'])
            lat_dist = math.radians(row['lat']-team_sch.iloc[i-1]['lat'])
            lon_dist = math.radians(row['lon']-team_sch.iloc[i-1]['lon'])
            temp_var = (
                (math.sin(lat_dist/2) * math.sin(lat_dist/2)) +
                (math.cos(lat1_rad) * math.cos(lat2_rad)) *
                (math.sin(lon_dist/2) * math.sin(lon_dist/2))
            )
            temp_var2 = (
                    2 * math.atan2(math.sqrt(temp_var), math.sqrt(1-temp_var))
            )
            tot_dist = 6371e3 * temp_var2 / 1000
                
            if tot_dist > 0: 
                travel_data_list.append(dict(
                    game_time=row['start_time'],
                    travel_date=pd.datetime.date(pd.to_datetime(row['start_time'])),
                    teamname = teamname, 
                    travel_dist=tot_dist, 
                    orig_lat = team_sch.iloc[i-1]['lat'],
                    orig_lon = team_sch.iloc[i-1]['lon'],
                    dest_lat = row['lat'],
                    dest_lon = row['lon']
                ))
travel_df = pd.DataFrame(travel_data_list)

travel_team_df = pd.DataFrame(travel_df.groupby('teamname')['travel_dist'].sum())
travel_team_df = travel_team_df.assign(trips=travel_df.groupby('teamname')['travel_dist'].count())
travel_team_df = travel_team_df.assign(km_per_trip=travel_team_df.travel_dist / travel_team_df.trips)
travel_team_df.reset_index(inplace=True)
travel_team_df=travel_team_df.assign(teamname=travel_team_df.teamname.str.replace('_',' ').str.title())


# bar chart 
fig = px.bar(
    travel_team_df.sort_values('travel_dist'), x='travel_dist', y='teamname', orientation='h',
    labels={'teamname': 'Team', 'travel_dist': 'Total distance (km)', 'km_per_trip': 'km/trip'},
    color='km_per_trip', color_continuous_scale=px.colors.sequential.GnBu, hover_name='teamname')
clean_chart_format(fig, namelocs=[0.9, 0.1])
fig.update_layout(title='Total travelled distances - NBA Teams (19-20 season)')
fig.show()

# scatter plot
fig = px.scatter(
    travel_team_df.sort_values('travel_dist'), x='travel_dist', y='teamname', orientation='h',
    labels={'teamname': 'Team', 'travel_dist': 'Total distance (km)', 'km_per_trip': 'km/trip'},
    color='km_per_trip', color_continuous_scale=px.colors.sequential.GnBu, hover_name='teamname')
clean_chart_format(fig, namelocs=[0.9, 0.1])
fig.update_layout(title='Total travelled distances - NBA Teams (19-20 season)')
fig.show()


fig = go.Figure()

# scatter geo scatter plot with lon/lat data 
fig.add_trace(go.Scattergeo(
    lon = arena_df['lon'], lat = arena_df['lat'], marker = dict(size = 8,
color = 'slategray'),
    hoverinfo='text', text = arena_df['teamname'] + ' - ' +
arena_df['arena_name'], name = 'Arenas'
    ))




teamname = 'PHILADELPHIA_76ERS'
travel_team_df = travel_df[travel_df.teamname == teamname]
team_col = teamcolor_dict[teamname]

fig.add_trace(go.Scattergeo(
    locationmode='USA-states', mode="lines",
    lon=np.append(travel_team_df['orig_lon'].values,
travel_team_df['dest_lon'].values[-1]),
    lat=np.append(travel_team_df['orig_lat'].values,
travel_team_df['dest_lat'].values[-1]),
    line = dict(width=1, color=team_col), opacity =0.8,
    hoverinfo='none', name=teamname
))


# Plotting the travel of a single team relevant to personal travel

fig['data'][0]['marker']['symbol'] = 'triangle-left'

fig.update_layout(
    title_text='NBA Travel paths',
    geo=dict(
        scope='north america',
        projection_type ='azimuthal equal area',
        showland =True,
        fitbounds="locations",
        landcolor='rgb(243,243,243)',
        countrycolor='rgb(204,204,204)',
    ),
)
fig.show()












# For completion sakes (whole league copied)

# NOW FOR THE WHOLE LEAGUE
# Initialise figure
fig = go.Figure()

# Add arenas
fig.add_trace(go.Scattergeo(
    lon=arena_df['lon'], lat=arena_df['lat'], marker=dict(size=8, color='slategray'),
    hoverinfo='text', text=arena_df['teamname'] + ' - ' + arena_df['arena_name'], name='Arenas'
))

# Add team flight traces
for teamname in travel_df.teamname.unique():
    travel_team_df = travel_df[travel_df.teamname == teamname]
    team_col = teamcolor_dict[teamname]
    fig.add_trace(go.Scattergeo(
        locationmode='USA-states', mode="lines",
        lon=np.append(travel_team_df['orig_lon'].values, travel_team_df['dest_lon'].values[-1]),
        lat=np.append(travel_team_df['orig_lat'].values, travel_team_df['dest_lat'].values[-1]),
        line=dict(width=1, color=team_col), opacity=0.4,
        hoverinfo='none', name=teamname
    ))

fig['data'][0]['marker']['symbol'] = 'triangle-left'

fig.update_layout(
    title_text='NBA Travel paths',
    geo=dict(
        scope='north america',
        projection_type='azimuthal equal area',
        showland=True,
        fitbounds="locations",
        landcolor='rgb(243, 243, 243)',
        countrycolor='rgb(204, 204, 204)',
    ),
)
fig.show()





# For completions sake Animation

# ========== ANIMATE TRAVEL PATHS ==========
# FOR ONE TEAM
teamname = 'PHILADELPHIA_76ERS'
travel_team_df = travel_df[travel_df.teamname == teamname]
team_col = teamcolor_dict[teamname]

lon_vals = np.append(travel_team_df['orig_lon'].values, travel_team_df['dest_lon'].values[-1])
lat_vals = np.append(travel_team_df['orig_lat'].values, travel_team_df['dest_lat'].values[-1])

frames = list()
lon_data = np.array(lon_vals[0])
lat_data = np.array(lat_vals[0])

for i in range(len(lon_vals)):
    frames.append(
        go.Frame(data=[go.Scattergeo(lon=lon_data, lat=lat_data)])
    )
    lon_data = np.append(lon_data, lon_vals[i])
    lat_data = np.append(lat_data, lat_vals[i])

fig = go.Figure(
    data=[
        go.Scattergeo(
            locationmode='USA-states', mode="lines",
            lon=np.append(lon_vals[0], lon_vals[0]),
            lat=np.append(lat_vals[0], lat_vals[0]),
            line=dict(width=1, color=team_col), opacity=0.1,
            hoverinfo='none', name=teamname
        )
    ],
    layout=go.Layout(
        title="Start Title",
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play", method="animate", args=[None])])]
    ),
    frames=frames
)
fig.add_trace(go.Scattergeo(
    lon=arena_df['lon'], lat=arena_df['lat'], marker=dict(size=8, color='slategray'),
    hoverinfo='text', text=arena_df['teamname'] + ' - ' + arena_df['arena_name'], name='Arenas'
))
fig['data'][1]['marker']['symbol'] = 'triangle-left'
fig.update_layout(
    title_text='NBA Travel paths',
    geo=dict(
        scope='north america',
        projection_type='azimuthal equal area',
        showland=True,
        fitbounds="locations",
        landcolor='rgb(243, 243, 243)',
        countrycolor='rgb(204, 204, 204)',
    ),
)
fig.show()   
    
    
    