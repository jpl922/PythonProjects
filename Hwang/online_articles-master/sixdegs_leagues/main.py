# ========== (c) JP Hwang 2020-03-13  ==========

import logging

# ===== START LOGGER =====
logger = logging.getLogger(__name__)
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
root_logger.addHandler(sh)

import pandas as pd
import numpy as np
import random
import pickle
import pytz
import plotly.express as px
import plotly.graph_objects as go

desired_width = 320
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', desired_width)

# ===== LOAD DATA =====
# Load schedule
nba_sch_data = pd.read_csv('srcdata/2020_nba_schedule_fulldata.csv', index_col=0)
# Create datetime column
nba_sch_data = nba_sch_data.assign(datetime=pd.to_datetime(nba_sch_data.est_time))

# Load teamcolor dict
with open('srcdata/teamcolor_dict.pickle', 'rb') as f:
    teamcolor_dict = pickle.load(f)
teamcolor_dict = {k.replace(' ', '_').upper(): v for k, v in teamcolor_dict.items()}

# Get list of all teams
# Make a dataframe of [team, contacted, when]
teams_list = nba_sch_data.home_team.unique()

# ===============================================================
# ===== CALCULATE TEAM CONTACTED LIST FOR A PARTICULAR TEAM =====
# ===============================================================

# Pick a random/particular "seed" team
seed_date = '2020-03-10'  # YYYY-MM-DD
seed_tm = random.choice(teams_list)

# Create DataFrame
teams_contacted_list = [{'team': tm, 'contacted': False, 'date': None, 'con_from': None, 'deg_sep': None} for tm in teams_list]
teams_contacted_df = pd.DataFrame(teams_contacted_list)

# Calculate data
utc = pytz.UTC
filt_sch_data = nba_sch_data[nba_sch_data.datetime > utc.localize(pd.to_datetime(seed_date))]

teams_contacted_df.loc[teams_contacted_df.team == seed_tm, 'contacted'] = True
teams_contacted_df.loc[teams_contacted_df.team == seed_tm, 'con_from'] = seed_tm
teams_contacted_df.loc[teams_contacted_df.team == seed_tm, 'date'] = pd.to_datetime(seed_date).date()
teams_contacted_df.loc[teams_contacted_df.team == seed_tm, 'deg_sep'] = 0

# Iterate every row of schedule:
for temp_tup in filt_sch_data.itertuples():
    home_tm_contacted = teams_contacted_df.loc[teams_contacted_df.team == temp_tup.home_team, 'contacted']
    away_tm_contacted = teams_contacted_df.loc[teams_contacted_df.team == temp_tup.away_team, 'contacted']
    if home_tm_contacted.values[0] != away_tm_contacted.values[0]:

        home_away = [temp_tup.home_team, temp_tup.away_team]
        for i in range(len(home_away)):
            tm = home_away[i]
            other_tm = home_away[1-i]
            if teams_contacted_df.loc[teams_contacted_df.team == tm, 'date'].values[0] == None:
                teams_contacted_df.loc[teams_contacted_df.team == tm, 'contacted'] = True
                teams_contacted_df.loc[teams_contacted_df.team == tm, 'date'] = pd.to_datetime(temp_tup.est_time).date()
                teams_contacted_df.loc[teams_contacted_df.team == tm, 'con_from'] = other_tm
                other_tm_deg_sep = teams_contacted_df.loc[teams_contacted_df.team == other_tm, 'deg_sep'].values[0]
                teams_contacted_df.loc[teams_contacted_df.team == tm, 'deg_sep'] = other_tm_deg_sep + 1

teams_contacted_df.sort_values('date', inplace=True)
date_range = max(teams_contacted_df.date) - min(teams_contacted_df.date)


# =======================================
# ========== SIMPLE PLOTS ==========
# =======================================

# Histogram
fig = px.histogram(teams_contacted_df, x='deg_sep', template='plotly_white')
fig.update_layout(bargap=0.5)
fig.show()

# Days of separation
days = (teams_contacted_df.date-min(teams_contacted_df.date)) / np.timedelta64(1, 'D')
teams_contacted_df = teams_contacted_df.assign(days=days)

fig = px.bar(
    teams_contacted_df, x='days', y='team',
    orientation='h', template='plotly_white',
    labels={'team': 'Team', 'days': 'Days until contacted.'}
)
fig.update_layout(bargap=0.2)
fig.show()

# Days of separation, grouped by source team
fig = px.bar(
    teams_contacted_df, x='days', y='team',
    orientation='h', template='plotly_white', color='con_from',
    labels={'team': 'Team', 'days': 'Days until contacted', 'con_from': 'Contact source:'}
)
fig.update_layout(bargap=0.2)
fig.show()

# Change colors to team colors
for i in range(len(fig['data'])):
    fig['data'][i]['marker']['color'] = teamcolor_dict[fig['data'][i]['name']]
fig.show()

# =================================
# ========== SIMPLE PLOT ==========
# =================================

# ========== GET ARENA DATA ==========
arena_df = pd.read_csv('srcdata/arena_data.csv', index_col=0)
arena_df = arena_df.assign(teamupper=arena_df.teamname.str.replace(' ', '_').str.upper())

# ========== PLOT ARENA LOCATIONS ==========
# Load mapbox key
with open('../../tokens/mapbox_tkn.txt', 'r') as f:
    mapbox_key = f.read().strip()

# Plot a simple map
fig = px.scatter_mapbox(arena_df, lat="lat", lon="lon", zoom=3, hover_name='teamname')
fig.update_layout(mapbox_style="light", mapbox_accesstoken=mapbox_key)  # mapbox_style="open-street-map" to use without a token
fig.update_traces(marker=dict(size=10, color='orange'))
fig.show()

# ========== MAP CONNECTIONS ==========

teams_contacted_df = teams_contacted_df.assign(orig_lat=0, orig_lon=0, dest_lat=0, dest_lon=0)

for temp_tuple in teams_contacted_df.itertuples():
    if temp_tuple.con_from == None:
        from_name = temp_tuple.team
    else:
        from_name = temp_tuple.con_from
    teams_contacted_df.loc[temp_tuple.Index, 'orig_lat'] = arena_df[arena_df.teamupper == from_name]['lat'].values[0]
    teams_contacted_df.loc[temp_tuple.Index, 'orig_lon'] = arena_df[arena_df.teamupper == from_name]['lon'].values[0]
    teams_contacted_df.loc[temp_tuple.Index, 'dest_lat'] = arena_df[arena_df.teamupper == temp_tuple.team]['lat'].values[0]
    teams_contacted_df.loc[temp_tuple.Index, 'dest_lon'] = arena_df[arena_df.teamupper == temp_tuple.team]['lon'].values[0]

# ========== SINGLE PLOT ==========
# Initialise figure
fig = go.Figure()

# Add arenas
fig.add_trace(go.Scattergeo(
    lon=arena_df['lon'], lat=arena_df['lat'], marker=dict(size=8, color='slategray'),
    hoverinfo='text', text=arena_df['teamname'] + ' - ' + arena_df['arena_name'], name='Arenas'
))

for i in range(len(teams_contacted_df)):
    src_tm = teams_contacted_df['con_from'].values[i]
    tgt_tm = teams_contacted_df['team'].values[i]
    con_date = str(teams_contacted_df['date'].values[i])
    team_col = teamcolor_dict[src_tm]
    fig.add_trace(go.Scattergeo(
        locationmode='USA-states', mode="lines",
        lon=[teams_contacted_df['orig_lon'].values[i], teams_contacted_df['dest_lon'].values[i]],
        lat=[teams_contacted_df['orig_lat'].values[i], teams_contacted_df['dest_lat'].values[i]],
        line=dict(width=1, color=team_col), opacity=0.8,
        hoverinfo='none', name=con_date + ': ' + src_tm.split('_')[-1] + ' to ' + tgt_tm.split('_')[-1]
    ))

fig['data'][0]['marker']['symbol'] = 'triangle-left'

fig.update_layout(
    title_text="NBA Teams' degrees of separation:"
               + "<BR>Starting with the " + seed_tm + " on " + seed_date
               + ", all teams are connected within " + str(date_range.days) + " days.",
    geo=dict(
        scope='north america',
        projection_type='azimuthal equal area',
        showland=True,
        fitbounds="locations",
        landcolor='rgb(243, 243, 243)',
        countrycolor='rgb(204, 204, 204)',
    ),
)

fig.update_layout(title={'font': {'size': 15}}, font={'size': 9, 'family': 'Arial, Tahoma, Helvetica'})
fig.show()

# ========== SINGLE PLOT w/ TEXT ==========
# Initialise figure
fig = go.Figure()

txt_list = list()
for i in range(len(arena_df)):
    teamupper = arena_df.iloc[i].teamupper
    temp_row = teams_contacted_df[teams_contacted_df.team == teamupper]
    temp_txt = (
            temp_row.team.values[0].split('_')[-1]
            + '<BR>' + str(temp_row.deg_sep.values[0]) + ' degrees of sep.'
    )
    txt_list.append(temp_txt)

# Add arenas
fig.add_trace(go.Scattergeo(
    mode="markers+text",
    lon=arena_df['lon'], lat=arena_df['lat'], marker=dict(size=8, color='slategray'),
    hoverinfo='text', text=txt_list, name='Arenas'
))

for i in range(len(teams_contacted_df)):
    src_tm = teams_contacted_df['con_from'].values[i]
    tgt_tm = teams_contacted_df['team'].values[i]
    con_date = str(teams_contacted_df['date'].values[i])
    team_col = teamcolor_dict[src_tm]
    fig.add_trace(go.Scattergeo(
        locationmode='USA-states', mode="lines",
        lon=[teams_contacted_df['orig_lon'].values[i], teams_contacted_df['dest_lon'].values[i]],
        lat=[teams_contacted_df['orig_lat'].values[i], teams_contacted_df['dest_lat'].values[i]],
        line=dict(width=1, color=team_col), opacity=0.8,
        hoverinfo='none', name=con_date + ': ' + src_tm.split('_')[-1] + ' to ' + tgt_tm.split('_')[-1]
    ))

fig['data'][0]['marker']['symbol'] = 'triangle-left'

fig.update_layout(
    title_text="NBA Teams' degrees of separation:"
               + "<BR>Starting with the " + seed_tm + " on " + seed_date
               + ", all teams are connected within " + str(date_range.days) + " days.",
    geo=dict(
        scope='north america',
        projection_type='azimuthal equal area',
        showland=True,
        fitbounds="locations",
        landcolor='rgb(243, 243, 243)',
        countrycolor='rgb(204, 204, 204)',
    ),
)

fig.update_layout(title={'font': {'size': 15}}, font={'size': 9, 'family': 'Arial, Tahoma, Helvetica'})
fig.show()

fig.update_layout(
    annotations=[
        go.layout.Annotation(
            x=0.9,
            y=0.9,
            showarrow=False,
            text="Twitter: @_jphwang",
            xref="paper",
            yref="paper",
            textangle=0
        ),
    ])

