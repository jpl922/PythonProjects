# ========== (c) JP Hwang 2020-02-25  ==========

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

desired_width = 320
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', desired_width)

# ========== GET TEAMS' SCHEDULES ==========
# Load teams' schedules
schedule_df = pd.read_csv('srcdata/2019_nba_schedule.csv', index_col=0)
schedule_df = schedule_df.assign(game_date=pd.to_datetime(schedule_df.est_time).dt.date)

# ========== GET GAME BOX SCORES ==========

box_df = pd.read_csv('srcdata/2019_nba_team_box_scores.csv', index_col=0)

# =====================================
# ========== GET BASIC PLOTS ==========
# =====================================

import plotly.express as px

# How many games in each category? Rest days.
temp_grp_df = box_df.groupby('rest_cats').count().reset_index(drop=False)
fig = px.bar(temp_grp_df, y='rest_cats', x='outcome', orientation='h')
fig.show()

# How many games in each category? Rest days & travel.
temp_grp_df = box_df.groupby(['rest_cats', 'travelled']).count().reset_index(drop=False)
temp_grp_df = temp_grp_df.assign(travelled=temp_grp_df.travelled.astype(str))
fig = px.bar(temp_grp_df, y='rest_cats', x='outcome', orientation='h', color='travelled', barmode='group')
fig.show()

# ========== GET WIN % ==========

travel_cats = ['rest_cats', 'travelled']
travel_grp_df = box_df.groupby(travel_cats).sum()
travel_grp_df = travel_grp_df.assign(games=box_df.groupby(travel_cats)['minutes_played'].count())
travel_grp_df['WIN%'] = travel_grp_df.win/travel_grp_df.games * 100
travel_grp_df.reset_index(drop=False, inplace=True)
travel_grp_df = travel_grp_df.assign(travelled=travel_grp_df.travelled.astype(str))

fig = px.bar(travel_grp_df, y='rest_cats', x='WIN%', orientation='h', color='travelled', barmode='group')
fig.show()

# With subplots

travel_cats = ['home', 'rest_cats', 'travelled']
travel_grp_df = box_df.groupby(travel_cats).sum()
travel_grp_df = travel_grp_df.assign(games=box_df.groupby(travel_cats)['minutes_played'].count())
travel_grp_df['WIN%'] = travel_grp_df.win/travel_grp_df.games * 100
travel_grp_df.reset_index(drop=False, inplace=True)
travel_grp_df = travel_grp_df.assign(travelled=travel_grp_df.travelled.astype(str))
fig = px.bar(travel_grp_df, y='rest_cats', x='WIN%', facet_col='home', orientation='h', color='travelled', barmode='group')
fig.show()

# =================================================
# ========== FURTHER SCHEDULE BREAKDOWNS ==========
# =================================================

# Inspect a table
travel_cats = ['home', 'travelled', 'rest_cats']
travel_grp_df = box_df.groupby(travel_cats).sum()
travel_grp_df = travel_grp_df.assign(games=box_df.groupby(travel_cats)['minutes_played'].count())
travel_grp_df.reset_index(drop=False, inplace=True)
print(travel_grp_df[travel_cats + ['games']])

# PARALLEL CATEGORIES CHART - TWO VARIABLES
box_df = box_df.assign(win_num=box_df.win.astype(int))


travel_cats = ['home', 'travelled']
fig = px.parallel_categories(box_df, dimensions=travel_cats, color='win_num')
fig.show()

# PARALLEL CATEGORIES - THREE CATEGORIES AND WIN %
travel_cats = ['home', 'travelled', 'rest_cats']
fig = px.parallel_categories(box_df, dimensions=travel_cats, color='win_num')
fig.show()

# TREEMAPS
travel_cats = ['home', 'travelled', 'rest_cats']
travel_grp_df = box_df.groupby(travel_cats).sum()
travel_grp_df = travel_grp_df.assign(games=box_df.groupby(travel_cats)['minutes_played'].count())
travel_grp_df.reset_index(drop=False, inplace=True)

chart_cats = ['home_str', 'travelled_str', 'rest_cats']
home_away = pd.Series(['Home ' * i for i in travel_grp_df.home.values]) + pd.Series(['Away ' * (1-i) for i in travel_grp_df.home.values])
travel_grp_df['home_str'] = home_away
travelled = pd.Series(['Travelled ' * i for i in travel_grp_df.travelled.values]) + pd.Series(['Stayed ' * (1-i) for i in travel_grp_df.travelled.values])
travel_grp_df['travelled_str'] = travelled
travel_grp_df['rest_cats'] = travel_grp_df['rest_cats'] + "'<BR>Rest"
travel_grp_df['WIN%'] = travel_grp_df.win/travel_grp_df.games * 100

fig = px.treemap(
    travel_grp_df, path=['home_str', 'travelled_str', 'rest_cats'], values='games', color='WIN%', color_continuous_midpoint=50, color_continuous_scale=px.colors.diverging.Portland)
fig.show()

fig = px.treemap(
    travel_grp_df, path=['home_str', 'rest_cats', 'travelled_str'], values='games', color='WIN%', color_continuous_midpoint=50, color_continuous_scale=px.colors.diverging.Portland)
fig.show()


# ADD OPPONENTS' REST DATA
box_df = pd.read_csv('srcdata/2019_nba_team_box_scores_2.csv', index_col=0)

travel_cats = ['home', 'travelled', 'rest_cats', 'opp_rest_cats']
travel_grp_df = box_df.groupby(travel_cats).sum()
travel_grp_df = travel_grp_df.assign(games=box_df.groupby(travel_cats)['minutes_played'].count())
travel_grp_df.reset_index(drop=False, inplace=True)

chart_cats = ['home_str', 'travelled_str', 'rest_cats', 'opp_rest_cats']
home_away = pd.Series(['Home ' * i for i in travel_grp_df.home.values]) + pd.Series(['Away ' * (1-i) for i in travel_grp_df.home.values])
travel_grp_df['home_str'] = home_away
travelled = pd.Series(['Travelled ' * i for i in travel_grp_df.travelled.values]) + pd.Series(['Stayed ' * (1-i) for i in travel_grp_df.travelled.values])
travel_grp_df['travelled_str'] = travelled
travel_grp_df['rest_cats'] = travel_grp_df['rest_cats'] + "' Rest"
travel_grp_df['opp_rest_cats'] = 'Opponent: <BR>' + travel_grp_df['opp_rest_cats'] + "'<BR>Rest"
travel_grp_df['WIN%'] = travel_grp_df.win/travel_grp_df.games * 100

fig = px.treemap(
    travel_grp_df, path=['home_str', 'rest_cats', 'travelled_str', 'opp_rest_cats'], values='games', color='WIN%', color_continuous_midpoint=50, color_continuous_scale=px.colors.diverging.Portland)
fig.show()

# REMOVE TRAVEL DATA FOR SIMPLICITY
travel_cats = ['home', 'rest_cats', 'opp_rest_cats']
travel_grp_df = box_df.groupby(travel_cats).sum()
travel_grp_df = travel_grp_df.assign(games=box_df.groupby(travel_cats)['minutes_played'].count())
travel_grp_df.reset_index(drop=False, inplace=True)

chart_cats = ['home_str', 'rest_cats', 'opp_rest_cats']
home_away = pd.Series(['Home ' * i for i in travel_grp_df.home.values]) + pd.Series(['Away ' * (1-i) for i in travel_grp_df.home.values])
travel_grp_df['home_str'] = home_away
travel_grp_df['rest_cats'] = travel_grp_df['rest_cats'] + "' Rest"
travel_grp_df['opp_rest_cats'] = 'Opponent: <BR>' + travel_grp_df['opp_rest_cats'] + "'<BR>Rest"
travel_grp_df['WIN%'] = travel_grp_df.win/travel_grp_df.games * 100

fig = px.treemap(
    travel_grp_df, path=['home_str', 'rest_cats', 'opp_rest_cats'], values='games', color='WIN%', color_continuous_midpoint=50, color_continuous_scale=px.colors.diverging.Portland
)
fig.show()
