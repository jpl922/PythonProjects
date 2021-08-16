# ========== (c) JP Hwang 2020-02-04  ==========

import logging

# ===== START LOGGER =====
logger = logging.getLogger(__name__)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
root_logger.addHandler(sh)


import pickle
import pandas as pd
import numpy as np
import basketball_assists.viz as viz

shots_df = pd.read_csv('srcdata/2018_19_NBA_shot_logs.csv', index_col=0)
out_dir = 'outputs'

# ==================== RECAP =================================
# ========== PLOT LEAGUE WIDE SHOT CHART - ACCURACY ==========
# ============================================================
with open('srcdata/league_hexbin_stats.pickle', 'rb') as f:
    league_hexbin_stats = pickle.load(f)

min_samples=0.0005
filt_league_hexbin_stats = viz.filt_hexbins(league_hexbin_stats, min_samples)
max_freq = 0.002
freq_by_hex = np.array([min(max_freq, i) for i in filt_league_hexbin_stats['freq_by_hex']])

xlocs = filt_league_hexbin_stats['xlocs']
ylocs = filt_league_hexbin_stats['ylocs']
accs_by_hex = filt_league_hexbin_stats['accs_by_hex']

colorscale = 'YlOrRd'
marker_cmin = 0.1
marker_cmax = 0.6
title_txt = "NBA shot chart, '18-'19<BR>(league average)"
hexbin_text = ['<i>Accuracy: </i>' + str(round(accs_by_hex[i]*100, 1)) + '%<BR>'
               for i in range(len(freq_by_hex))]
ticktexts = [str(marker_cmin*100)+'%-', "", str(marker_cmax*100)+'%+']

fig = viz.plot_shot_hexbins_plotly(
    xlocs, ylocs, freq_by_hex, accs_by_hex,
    marker_cmin, marker_cmax, colorscale=colorscale,
    title_txt=title_txt, hexbin_text=hexbin_text, ticktexts=ticktexts)

# ==================== MAPPING ASSIST RATES ==================
# ========== PLOT LEAGUE WIDE SHOT CHART - ASSISTS ===========
# ============================================================
with open('srcdata/league_hexbin_stats.pickle', 'rb') as f:
    league_hexbin_stats = pickle.load(f)

min_samples=0.0005
filt_league_hexbin_stats = viz.filt_hexbins(league_hexbin_stats, min_samples)
max_freq = 0.002
freq_by_hex = np.array([min(max_freq, i) for i in filt_league_hexbin_stats['freq_by_hex']])

xlocs = filt_league_hexbin_stats['xlocs']
ylocs = filt_league_hexbin_stats['ylocs']
asts_by_hex = filt_league_hexbin_stats['ass_perc_by_hex']

colorscale = 'YlOrRd'
marker_cmin = 0.3
marker_cmax = 1
title_txt = "NBA shot chart, '18-'19<BR>(league average)"
hexbin_text = ['<i>Assist rate: </i>' + str(round(asts_by_hex[i]*100, 1)) + '%<BR>'
               for i in range(len(freq_by_hex))]
ticktexts = [str(marker_cmin*100)+'%-', "", str(marker_cmax*100)+'%+']

fig = viz.plot_shot_hexbins_plotly(
    xlocs, ylocs, freq_by_hex, asts_by_hex,
    marker_cmin, marker_cmax, colorscale=colorscale,
    title_txt=title_txt, legend_title='Assist rate',
    hexbin_text=hexbin_text, ticktexts=ticktexts)

# ================== ACCURACY Vs ASSIST RATES ================
# ====== HOW WELL IS ACCURACY CORRELATED TO ASSIST RATE ======
# ============================================================

per100_df = pd.read_csv('srcdata/2018_2019_per100_stats.csv', index_col=0)
per100_df['FG%'] = per100_df['FG%'] * 100

import plotly.express as px
fig = px.scatter(
    per100_df, x='AST', y='FG%', size='PTS', size_max=13, color_continuous_scale='rdylbu_r',
    color='PTS', hover_name='Team', trendline="ols")
fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
fig.update_layout(width=800, height=600)
fig.data[1].marker.color = 'grey'  # set trendline color
fig.show()


# ========== ANALYSE ACCURACY vs ASSIST RATE FOR SHOT DISTANCES ==========
# get hexbin data for each team, put into dataframe
zone_names = shots_df.shot_zone.unique()
zone_names.sort()
summary_data_list = list()
for teamname in shots_df.team.unique():
    team_df = shots_df[shots_df.team == teamname]
    shots_made = team_df.groupby('shot_zone').sum()['shot_made']
    shots_taken = team_df.groupby('shot_zone').count()['shot_made']
    shots_pcts = round(shots_made / shots_taken * 100, 1)  # Get shot acc % per zone
    assists = team_df.groupby('shot_zone').count()['assist']
    assist_pcts = round(assists / shots_made * 100, 1)  # Get assist rate per zone
    for zone_name in zone_names:
        temp_dict = dict()
        temp_dict['shots_pct'] = shots_pcts[zone_name]
        temp_dict['assist_pct'] = assist_pcts[zone_name]
        temp_dict['shots_taken'] = shots_taken[zone_name]
        temp_dict['teamname'] = teamname
        temp_dict['zone_name'] = zone_name
        summary_data_list.append(temp_dict)
flat_summary_df = pd.DataFrame(summary_data_list)

# Plot data
fig = px.scatter(flat_summary_df, x='assist_pct', y='shots_pct', color='zone_name', hover_name='teamname')
fig.update_traces(marker=dict(size=10, opacity=0.7, line=dict(width=1, color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
fig.update_layout(height=500, width=1000)
fig.show()

# Separate plots into subplots
fig = px.scatter(flat_summary_df, x='assist_pct', y='shots_pct',
                 facet_col='zone_name', facet_col_wrap=3,
                 color='teamname', size_max=14,
                 size='shots_taken', hover_name='teamname')

fig.update_yaxes(matches=None, showticklabels=True)
fig.update_xaxes(matches=None, showticklabels=True)
fig.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
fig.update_layout(height=800, width=900)
fig.show()

# ================== CORRELATION BY SHOT CHARTS ================
# ====== VISUALISING SHOT ACC / AST CORRELATION ON COURT =======
# ==============================================================

from copy import deepcopy
teamname = 'GSW'

with open('srcdata/' + teamname + '_hexbin_stats.pickle', 'rb') as f:
    team_hexbin_stats = pickle.load(f)

rel_hexbin_stats = deepcopy(team_hexbin_stats)
base_hexbin_stats = deepcopy(league_hexbin_stats)

rel_hexbin_stats['accs_by_hex'] = rel_hexbin_stats['accs_by_hex'] - base_hexbin_stats['accs_by_hex']
rel_hexbin_stats['ass_perc_by_hex'] = rel_hexbin_stats['ass_perc_by_hex'] - base_hexbin_stats['ass_perc_by_hex']
rel_hexbin_stats = viz.filt_hexbins(rel_hexbin_stats, min_threshold=0.0005)

xlocs = rel_hexbin_stats['xlocs']
ylocs = rel_hexbin_stats['ylocs']
freq_by_hex = np.array([min(max_freq, i) for i in rel_hexbin_stats['freq_by_hex']])


accs_by_hex = rel_hexbin_stats['accs_by_hex']
colorscale = 'RdYlBu_r'
marker_cmin = -0.1
marker_cmax = 0.1
title_txt = teamname + ":<BR>Shot chart, '18-'19<BR>(vs NBA average)"
hexbin_text = [
        '<i>Accuracy: </i>' + str(round(accs_by_hex[i]*100, 1)) + '%<BR>'
        + 'vs NBA average' for i in range(len(freq_by_hex))
]
ticktexts = ["Worse", "Average", "Better"]

fig = viz.plot_shot_hexbins_plotly(
    xlocs, ylocs, freq_by_hex, accs_by_hex,
    marker_cmin, marker_cmax, colorscale=colorscale,
    title_txt=title_txt, hexbin_text=hexbin_text, ticktexts=ticktexts)


asts_by_hex = rel_hexbin_stats['ass_perc_by_hex']
colorscale = 'RdYlBu_r'
marker_cmin = -0.1
marker_cmax = 0.1
title_txt = teamname + ":<BR>Shot chart, '18-'19<BR>(vs NBA average)"
hexbin_text = [
        '<i>Assists: </i>' + str(round(asts_by_hex[i]*100, 1)) + '%<BR>'
        + 'vs NBA average' for i in range(len(freq_by_hex))
]
ticktexts = ["Worse", "Average", "Better"]

fig = viz.plot_shot_hexbins_plotly(
    xlocs, ylocs, freq_by_hex, asts_by_hex,
    marker_cmin, marker_cmax, colorscale=colorscale, legend_title='Assist rate',
    title_txt=title_txt, hexbin_text=hexbin_text, ticktexts=ticktexts)

# ========== Plot TEAM parallel category chart ==========
teamname = 'TOR'
team_df = shots_df[shots_df.team == teamname]

# Simple ParCat plot
fig = px.parallel_categories(team_df[team_df.shot_made == 1], dimensions=['player', 'shot_zone', 'assist'],
                color_continuous_scale=px.colors.sequential.Inferno,
                labels={'player':'Shooter', 'shot_zone':'Shot location', 'assist':'Assist (if any)'})
fig.show()

# Refined PatCat plot - for a player
player = 'Kawhi Leonard'
player_df = shots_df[shots_df.player == player]
colorscale = [[0, 'dimgray'], [1, 'crimson']]
title_txt = player + ' Shots - 2018/2019 NBA Season (colored: assisted)'
fig = viz.plot_parcat_chart(player_df, title_txt, colorscale)
fig.show()

# Refined PatCat plot - for a team
teamname = 'HOU'
team_df = shots_df[shots_df.team == teamname]
colorscale = [[0, 'dimgray'], [1, 'crimson']]
title_txt = teamname + ' Shots - 2018/2019 NBA Season (colored: assisted)'
fig = viz.plot_parcat_chart(team_df, title_txt, colorscale)
fig.show()

