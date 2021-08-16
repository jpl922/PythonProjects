# ========== (c) JP Hwang 2020-02-03  ==========

import logging

# ===== START LOGGER =====
logger = logging.getLogger(__name__)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
root_logger.addHandler(sh)

# ================================================
# ========== DATA CLEANING / PROCESSING ==========
# ================================================

# ===== LOAD RAW DATA =====
import pandas as pd
player_data_df = pd.read_csv('srcdata/player_data.csv')
season_stats_df = pd.read_csv('srcdata/Seasons_Stats.csv', index_col=0)

print(player_data_df.head())
print(player_data_df.info())
print(player_data_df.describe())

# ===== CLEAN DATA =====
# Clean player heights
player_data_df.height.fillna("0-0", inplace=True)
player_data_df.weight.fillna(0, inplace=True)
player_data_df = player_data_df.assign(height_metric=player_data_df.height.str[:1].astype(int) * 30.48 + player_data_df.height.str[2:].astype(int) * 30.48 / 12)
player_data_df = player_data_df.assign(weight_metric=player_data_df.weight * 0.453592)

# Filter season dataset by minutes played & year
season_stats_df = season_stats_df[(season_stats_df.MP > 1000) & (season_stats_df.Year > 1980)]

# Drop players' partial seasons (leave the total)
for temp_tuple in season_stats_df[season_stats_df.Tm == 'TOT'].itertuples():
    part_seasons = season_stats_df[
        (season_stats_df.Player == temp_tuple.Player) & (season_stats_df.Year == temp_tuple.Year) & (season_stats_df.Tm != 'TOT')
    ]
    if len(part_seasons) > 0:
        logger.info(f'Deleting {len(part_seasons)} partial seasons for {temp_tuple.Player} in {temp_tuple.Year}')
        season_stats_df = season_stats_df.drop(part_seasons.index)

# Assign height/weight data
season_stats_df = season_stats_df.assign(height=0)
season_stats_df = season_stats_df.assign(weight=0)

for itertup in season_stats_df.itertuples():
    pname = itertup.Player
    if pname[-1] == '*':
        pname = pname[:-1]
    player_data = player_data_df[player_data_df.name == pname]
    if len(player_data) > 0:
        season_stats_df.loc[itertup.Index, 'height'] = player_data.height_metric.values[0]
        season_stats_df.loc[itertup.Index, 'weight'] = player_data.weight_metric.values[0]
    else:
        player_data = player_data_df[
            (player_data_df.name.str.startswith(pname))
            & (player_data_df.year_start <= itertup.Year)
            & (player_data_df.year_end >= itertup.Year)
        ]
        if len(player_data) > 1:
            logger.warning(f'MULTIPLE NAMES FOUND STARTING WITH {pname}')
        logger.info(f'Populating player data for {pname} in {itertup.Year} with {player_data.name}')
        season_stats_df.loc[itertup.Index, 'height'] = player_data.height_metric.values[0]
        season_stats_df.loc[itertup.Index, 'weight'] = player_data.weight_metric.values[0]

# Clean up the rest of the data & reset the index
season_stats_df.GS = season_stats_df.GS.fillna(0)
season_stats_df['3P%'] = season_stats_df['3P%'].fillna(0)
season_stats_df = season_stats_df.assign(pos_simple=season_stats_df.Pos.str[:2])
season_stats_df.pos_simple = season_stats_df.pos_simple.str.replace('-', '')
season_stats_df = season_stats_df.drop(['blanl', 'blank2'], axis=1)
season_stats_df = season_stats_df.reset_index(drop=True)

season_stats_df.to_csv('srcdata/Seasons_Stats_proc.csv')

# ===================================
# ========== DATA ANALYSIS ==========
# ===================================

# ===== LOAD PROCESSED DATA =====
proc_stats_df = pd.read_csv('srcdata/Seasons_Stats_proc.csv', index_col=0)

# ===== PRELIMINARY LOOK AT DATA =====
# Add BMI column & get an overview
proc_stats_df = proc_stats_df.assign(bmi=proc_stats_df.weight / ((proc_stats_df.height/100) ** 2))

import plotly.express as px
fig = px.scatter(
    proc_stats_df, x='height', y='bmi',
    color='pos_simple', category_orders=dict(pos_simple=['PG', 'SG', 'SF', 'PF', 'C']),
    marginal_x="histogram", marginal_y="histogram", hover_name='Player')
fig.show()

# ===== CREATE BINS =====
import numpy as np

ht_limits = [0, 190, 200, 210, np.inf]
ht_labels = [str(i) + '_' + str(ht_limits[i]) + ' to ' + str(ht_limits[i+1]) for i in range(len(ht_limits)-1)]
proc_stats_df = proc_stats_df.assign(
    height_bins=pd.cut(proc_stats_df.height, bins=ht_limits, labels=ht_labels, right=False)
)

bmi_limits = [0, 22.5, 24, 25.5, np.inf]
bmi_labels = [str(i) + '_' + str(bmi_limits[i]) + ' to ' + str(bmi_limits[i+1]) for i in range(len(bmi_limits)-1)]
proc_stats_df = proc_stats_df.assign(
    bmi_bins=pd.cut(proc_stats_df.bmi, bins=bmi_limits, labels=bmi_labels, right=False)
)

# ===== CAREER LENGTHS =====
ht_n_seasons = proc_stats_df.groupby('height_bins').count()['Year']
ht_n_unique_pl = proc_stats_df.groupby('height_bins').nunique('Player')['Player']
print(ht_n_seasons / ht_n_unique_pl)

bmi_n_seasons = proc_stats_df.groupby('bmi_bins').count()['Year']
bmi_n_unique_pl = proc_stats_df.groupby('bmi_bins').nunique('Player')['Player']
print(bmi_n_seasons / bmi_n_unique_pl)

# ===== HEIGHT / BMI vs PER =====
# As scatter plots
fig = px.scatter(
    proc_stats_df, x='height', y='PER', hover_name='Player'
    , color='Year', color_continuous_scale=px.colors.sequential.Teal,
)
fig.show()

fig = px.scatter(
    proc_stats_df, x='bmi', y='PER', hover_name='Player'
    , color='Year', color_continuous_scale=px.colors.carto.Burg,
)
fig.show()

# In box plots
fig = px.box(
    proc_stats_df, x='height_bins', y='PER', color='bmi_bins', hover_name='Player'
    , category_orders=dict(height_bins=ht_labels, bmi_bins=bmi_labels)
)
fig.show()

# ===== POSITION PLAYED / BMI vs PER =====
fig = px.histogram(
    proc_stats_df, x='pos_simple', facet_row='bmi_bins', facet_col='height_bins', color='pos_simple'
    , category_orders=dict(height_bins=ht_labels, bmi_bins=bmi_labels, pos_simple=['PG', 'SG', 'SF', 'PF', 'C']))
fig.show()

# ===== AGE BRACKET / BMI vs PER =====
age_limits = [0, 23, 25, 27, 29, 31, np.inf]
age_labels = [str(i) + '_' + str(age_limits[i]) + ' to ' + str(age_limits[i+1]) for i in range(len(age_limits)-1)]
proc_stats_df = proc_stats_df.assign(
    age_bins=pd.cut(proc_stats_df.Age, bins=age_limits, labels=age_labels, right=False)
)
fig = px.box(
    proc_stats_df, x='age_bins', y='PER', color='height_bins', hover_name='Player'
    , category_orders=dict(height_bins=ht_labels, age_bins=age_labels)
)
fig.show()

fig = px.box(
    proc_stats_df, x='age_bins', y='PER', color='bmi_bins', hover_name='Player'
    , category_orders=dict(bmi_bins=bmi_labels, age_bins=age_labels)
)
fig.show()

# Now with position subplots
fig = px.box(
    proc_stats_df, x='age_bins', y='PER', color='bmi_bins', hover_name='Player', facet_row='pos_simple'
    , category_orders=dict(bmi_bins=bmi_labels, age_bins=age_labels, pos_simple=['PG', 'SG', 'SF', 'PF', 'C'])
)
fig.update_layout(width=800, height=1200)
fig.show()

fig = px.box(
    proc_stats_df, x='height_bins', y='PER', color='age_bins', hover_name='Player'
    , category_orders=dict(height_bins=ht_labels, age_bins=age_labels)
)
fig.show()

# ===== MODERN BASKETBALL / BMI vs PER =====
yr_limits = [0, 1995, 2007, np.inf]
yr_labels = [str(i) + '_' + str(yr_limits[i]) + ' to ' + str(yr_limits[i+1]) for i in range(len(yr_limits)-1)]
proc_stats_df = proc_stats_df.assign(
    year_bins=pd.cut(proc_stats_df.Year, bins=yr_limits, labels=yr_labels, right=False)
)
fig = px.box(
    proc_stats_df, x='height_bins', y='PER', color='age_bins', hover_name='Player', facet_row='year_bins'
    , category_orders=dict(height_bins=ht_labels, age_bins=age_labels, year_bins=yr_labels)
)
fig.show()
