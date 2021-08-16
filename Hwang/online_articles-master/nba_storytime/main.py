# ========== (c) JP Hwang 2020-03-05  ==========

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

desired_width = 320
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', desired_width)

# LOAD DATA
all_records_df = pd.read_csv('srcdata/2018_2019_season_records.csv', index_col=0)

# Get regular season games
records_df = all_records_df[pd.to_datetime(all_records_df.date) < pd.to_datetime('2019-04-12')]

# ========== PLOT SIMPLE TIME-SERIES DATA ==========
# PLOT TIME-SERIES DATA OVER GAMES
import plotly.express as px
fig = px.scatter(records_df, x='games', y='wins', color='team')
fig.show()

# As lines + marker
fig = px.scatter(records_df, x='games', y='wins', color='team')
fig.update_traces(mode='markers+lines')
fig.show()

# As lines only
fig = px.scatter(records_df, x='games', y='wins', color='team')
fig.update_traces(mode='lines')
fig.show()

# ========== IMPROVE READABILITY ==========
# Sort names
tm_names = [i for i in records_df.team.unique()]
tm_names.sort()
fig = px.scatter(records_df, x='games', y='wins', color='team', category_orders={'team': tm_names})
fig.update_traces(mode='markers+lines')
fig.show()

# Add the right colours
import pickle
with open('srcdata/teamcolor_dict.pickle', 'rb') as f:
    team_col_dict = pickle.load(f)
team_col_dict = {k.upper().replace(' ', '_'): v for k, v in team_col_dict.items()}
team_cols_list = [team_col_dict[tm] for tm in tm_names]
fig = px.scatter(records_df, x='games', y='wins', color='team', category_orders={'team': tm_names}, color_discrete_sequence=team_cols_list)
fig.update_traces(mode='markers+lines')
fig.show()

# Highlight one team only - Raptors
base_col = '#C0C0C0'
team_cols_list = list()
for i in range(len(tm_names)):
    tm = 'TORONTO_RAPTORS'
    if tm_names[i] == tm:
        team_cols_list.append(team_col_dict[tm])
    else:
        team_cols_list.append(base_col)
fig = px.scatter(records_df, x='games', y='wins', color='team', category_orders={'team': tm_names}, color_discrete_sequence=team_cols_list)
fig.update_traces(mode='markers+lines')
fig.show()

# Highlight Atlantic Division teams
base_col = '#C0C0C0'
hero_teams = ['TORONTO_RAPTORS', 'PHILADELPHIA_76ERS', 'BOSTON_CELTICS', 'BROOKLYN_NETS', 'NEW_YORK_KNICKS']
team_cols_list = list()
for i in range(len(tm_names)):
    if tm_names[i] in hero_teams:
        tm = tm_names[i]
        team_cols_list.append(team_col_dict[tm])
    else:
        team_cols_list.append(base_col)
fig = px.scatter(records_df, x='games', y='wins', color='team', category_orders={'team': tm_names}, color_discrete_sequence=team_cols_list)
fig.update_traces(mode='markers+lines')
fig.show()

# Highlight Atlantic Division teams - at the bottom
base_col = '#C0C0C0'
hero_teams = ['TORONTO_RAPTORS', 'PHILADELPHIA_76ERS', 'BOSTON_CELTICS', 'BROOKLYN_NETS', 'NEW_YORK_KNICKS']
tm_names = [i for i in records_df.team.unique() if i not in hero_teams]
tm_names.sort()
tm_names = tm_names + hero_teams
team_cols_list = list()
for i in range(len(tm_names)):
    if tm_names[i] in hero_teams:
        tm = tm_names[i]
        team_cols_list.append(team_col_dict[tm])
    else:
        team_cols_list.append(base_col)
fig = px.scatter(records_df, x='games', y='wins', color='team', category_orders={'team': tm_names}, color_discrete_sequence=team_cols_list)
fig.update_traces(mode='markers+lines')
fig.show()


# ========== FINAL TOUCHES ==========
# Separate Conferences, and add highlights for
hero_teams = [
    'TORONTO_RAPTORS', 'PHILADELPHIA_76ERS', 'BOSTON_CELTICS', 'BROOKLYN_NETS', 'NEW_YORK_KNICKS',
    'HOUSTON_ROCKETS', 'SAN_ANTONIO_SPURS', 'DALLAS_MAVERICKS', 'MEMPHIS_GRIZZLIES', 'NEW_ORLEANS_PELICANS'
]
tm_names = [i for i in records_df.team.unique() if i not in hero_teams]
tm_names.sort()
tm_names = tm_names + hero_teams
team_cols_list = list()
for i in range(len(tm_names)):
    if tm_names[i] in hero_teams:
        tm = tm_names[i]
        team_cols_list.append(team_col_dict[tm])
    else:
        team_cols_list.append(base_col)
fig = px.scatter(records_df, x='games', y='wins', color='team', category_orders={'team': tm_names},
                 color_discrete_sequence=team_cols_list, facet_col='conference')
fig.update_traces(mode='markers+lines')
fig.show()

# Try different templates
# See: https://plot.ly/python/templates/
fig = px.scatter(records_df, x='games', y='wins', color='team', category_orders={'team': tm_names},
                 color_discrete_sequence=team_cols_list, facet_col='conference', template="plotly_white")
fig.update_traces(mode='markers+lines')
fig.show()

# With more formatting applied
fig = px.scatter(records_df, x='games', y='wins', color='team', category_orders={'team': tm_names},
                 color_discrete_sequence=team_cols_list, facet_col='conference', template="ggplot2",
                 title='2018-19 NBA Regular season wins',
                 labels={'games': 'Games played', 'wins': 'Season Wins', 'team': 'Team'}
                 )
fig.for_each_annotation(lambda t: t.update(text=t.text.replace('conference=', 'Conference: ')))
fig.update_traces(mode='markers+lines')
fig.show()

