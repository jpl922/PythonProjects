# ========== (c) JP Hwang 2020-02-11  ==========

import logging

# ===== START LOGGER =====
logger = logging.getLogger(__name__)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
root_logger.addHandler(sh)


def get_zones(x, y, excl_angle=False):

    def append_name_by_angle(temp_angle):

        if excl_angle:
            temp_text = ''
        else:
            if temp_angle < 60 and temp_angle > -90:
                temp_text = '_right'
            elif temp_angle > 120 or temp_angle < -90:
                temp_text = '_middle'
            else:
                temp_text = '_left'
        return temp_text

    import math

    zones_list = list()
    for i in range(len(x)):

        temp_angle = math.atan2(y[i], x[i]) / math.pi * 180
        temp_dist = ((x[i] ** 2 + y[i] ** 2) ** 0.5) / 10

        if temp_dist > 30:
            zone = '7 - 30+ ft'
        elif (x[i] < -220 or x[i] > 220) and y[i] < 90:
            zone = '4 - Corner 3s'
            zone += append_name_by_angle(temp_angle)
        elif temp_dist > 27:
            zone = '6 - Long 3s'
            zone += append_name_by_angle(temp_angle)
        elif temp_dist > 23.75:
            zone = '5 - Short 3 (<27 ft)'
            zone += append_name_by_angle(temp_angle)
        elif temp_dist > 14:
            zone = '3 - Long 2 (14+ ft)'
            zone += append_name_by_angle(temp_angle)
        elif temp_dist > 4:
            zone = '2 - Short 2 (4-14 ft)'
            zone += append_name_by_angle(temp_angle)
        else:
            zone = '1 - Within 4 ft'

        zones_list.append(zone)

    return zones_list


import pandas as pd
import numpy as np
import plotly.express as px

# ======================================
# ===== LOAD DATA AND PREPARE DATA =====
# ======================================

shots_df = pd.read_csv('srcdata/2018_19_NBA_shot_logs.csv', index_col=0)
shots_df = shots_df.assign(shot_zone=get_zones(list(shots_df['original_x']), list(shots_df['original_y']), excl_angle=True))
out_dir = 'outputs'

# Create a total elapsed time column
shots_df = shots_df[shots_df.period <= 4]
shots_df = shots_df.assign(tot_time=(shots_df.period-1)*np.timedelta64(60*12, 's') + pd.to_timedelta(shots_df.elapsed, unit='s'))
shots_df = shots_df.assign(score_diff=abs(shots_df.home_score-shots_df.away_score))

# =========================================
# ===== DETERMINE WHERE TO SLICE DATA =====
# =========================================
# ===== How do stats change in these periods =====
# Data for the league
league_shots_taken = shots_df.groupby('shot_zone').count()['shot_made']
league_shots_freq = league_shots_taken/sum(league_shots_taken)
league_shots_made = shots_df.groupby('shot_zone').sum()['shot_made']
league_shots_acc = league_shots_made / league_shots_taken

zone_names = shots_df.shot_zone.unique()
zone_names.sort()
summary_data_list = list()
for time_thresh in [12, 10, 8, 6, 4, 2]:
    for score_thresh in [2, 4, 6, 8, 10]:
        filt_shots_df = shots_df[
            (shots_df.tot_time > np.timedelta64(60*(48-time_thresh), 's'))
            & (shots_df.score_diff <= score_thresh)
        ]
        filt_shots_taken = filt_shots_df.groupby('shot_zone').count()['shot_made']
        filt_shots_freq = filt_shots_taken/sum(filt_shots_taken)
        filt_shots_made = filt_shots_df.groupby('shot_zone').sum()['shot_made']
        filt_shots_acc = filt_shots_made / filt_shots_taken
        for zone_name in zone_names:
            temp_dict = dict(
                zone_name=zone_name,
                score_thresh='Score within ' + str(score_thresh),
                time_thresh='<' + str(time_thresh),
                filt_shots_taken=filt_shots_taken[zone_name],
                rel_shots_freq=100 * (filt_shots_freq[zone_name] - league_shots_freq[zone_name]),
                filt_shots_freq=100 * filt_shots_freq[zone_name],
                rel_shots_acc=100 * (filt_shots_acc[zone_name] - league_shots_acc[zone_name]),
                filt_shots_acc=100 * filt_shots_acc[zone_name]
            )
            summary_data_list.append(temp_dict)
summary_df = pd.DataFrame(summary_data_list)

# Look at shot frequency
fig = px.scatter(
    summary_df, x='score_thresh', y='rel_shots_freq', color='time_thresh', size='filt_shots_freq',
    facet_col='zone_name', hover_data=['filt_shots_taken'])
fig.show()

# Flipping x-axis:
fig = px.scatter(
    summary_df, x='time_thresh', y='rel_shots_freq', color='score_thresh', size='filt_shots_freq',
    facet_col='zone_name', hover_data=['filt_shots_taken'])
fig.show()

# Look at shot sccuracy
fig = px.scatter(
    summary_df, x='time_thresh', y='rel_shots_acc', color='score_thresh', size='filt_shots_freq',
    facet_col='zone_name', hover_data=['filt_shots_taken'])
fig.show()

# ===== HISTOGRAMS OF SCORE DIFFERENCES =====
fig = px.histogram(shots_df, x='score_diff', nbins=30, histnorm='probability density', range_y=[0, 0.09])
fig.update_layout(
    title_text='Score differences in an NBA game (in regulation time)',
    paper_bgcolor="white",
    plot_bgcolor="white",
    xaxis_title_text='Score difference', # xaxis label
    yaxis_title_text='Probability', # yaxis label
    bargap=0.2,  # gap between bars of adjacent location coordinates
)
fig.show()

for time_thresh in [6, 4, 2]:
    fig = px.histogram(
        shots_df[(shots_df.tot_time > np.timedelta64(60*(48-time_thresh), 's'))],
        x='score_diff', nbins=30, histnorm='probability density', range_y=[0, 0.09])
    fig.update_traces(marker=dict(color=px.colors.sequential.Sunset[time_thresh]))
    fig.update_layout(
        title_text='Score differences in the last ' + str(time_thresh) + ' minutes (in regulation time)',
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis_title_text='Score difference', # xaxis label
        yaxis_title_text='Probability', # yaxis label
        bargap=0.2,  # gap between bars of adjacent location coordinates
    )
    fig.show()

# ============================================
# ===== EVALUATE CRUNCH TIME DIFFERENCES =====
# ============================================
shots_df = shots_df.assign(
    crunchtime=(shots_df.tot_time > np.timedelta64(60*(48-6), 's'))
               & (shots_df.score_diff <= 2))

# ===== Compare crunch time vs non-crunch time datasets =====
crunch_data_list = list()
for crunch_bool in [True, False]:
    filt_shots_df = shots_df[shots_df.crunchtime == crunch_bool]
    filt_shots_taken = filt_shots_df.groupby('shot_zone').count()['shot_made']
    filt_shots_freq = filt_shots_taken/sum(filt_shots_taken)
    filt_shots_made = filt_shots_df.groupby('shot_zone').sum()['shot_made']
    filt_shots_acc = filt_shots_made / filt_shots_taken
    for zone_name in zone_names:
        temp_dict = dict(
            zone_name=zone_name,
            crunch_bool='Crunchtime: ' + str(crunch_bool),
            time_thresh='<' + str(time_thresh),
            filt_shots_taken=filt_shots_taken[zone_name],
            rel_shots_freq=100 * (filt_shots_freq[zone_name] - league_shots_freq[zone_name]),
            filt_shots_freq=100 * filt_shots_freq[zone_name],
            rel_shots_acc=100 * (filt_shots_acc[zone_name] - league_shots_acc[zone_name]),
            filt_shots_acc=100 * filt_shots_acc[zone_name]
        )
        crunch_data_list.append(temp_dict)
crunch_df = pd.DataFrame(crunch_data_list)

# Look at shot frequency
bgcolor = "#ffffff"
fig = px.scatter(
    crunch_df, x='zone_name', y='filt_shots_freq', color='crunch_bool', size='filt_shots_freq',
    hover_data=['filt_shots_taken'], color_continuous_scale=px.colors.diverging.RdYlBu_r)
fig.update_layout(
    paper_bgcolor=bgcolor,
    plot_bgcolor=bgcolor,
)
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
fig.update_traces(mode='lines+markers')
fig.show()

# Relative shot frequency
fig = px.scatter(
    crunch_df, x='zone_name', y='rel_shots_freq', color='crunch_bool', size='filt_shots_freq',
    hover_data=['filt_shots_taken'], color_continuous_scale=px.colors.diverging.RdYlBu_r)
fig.update_layout(
    paper_bgcolor=bgcolor,
    plot_bgcolor=bgcolor,
)
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
fig.update_traces(mode='lines+markers')
fig.show()

# Shot accuracy
fig = px.scatter(
    crunch_df, x='zone_name', y='filt_shots_acc', color='crunch_bool', size='filt_shots_freq',
    hover_data=['filt_shots_taken'], color_continuous_scale=px.colors.diverging.RdYlBu_r)
fig.update_layout(
    paper_bgcolor=bgcolor,
    plot_bgcolor=bgcolor,
)
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
fig.update_traces(mode='lines+markers')
fig.show()

# ===== Generate a shot chart =====
import pickle
from basketball_crunchtime import viz
from copy import deepcopy

with open('srcdata/league_hexbin_stats.pickle', 'rb') as f:
    league_hexbin_stats = pickle.load(f)
with open('srcdata/crunch_hexbin_stats.pickle', 'rb') as f:
    crunch_hexbin_stats = pickle.load(f)

max_freq = 0.002
min_samples = 0.0005

rel_hexbin_stats = deepcopy(crunch_hexbin_stats)
base_hexbin_stats = deepcopy(league_hexbin_stats)

rel_hexbin_stats['accs_by_hex'] = rel_hexbin_stats['accs_by_hex'] - base_hexbin_stats['accs_by_hex']
rel_hexbin_stats['ass_perc_by_hex'] = rel_hexbin_stats['ass_perc_by_hex'] - base_hexbin_stats['ass_perc_by_hex']
rel_hexbin_stats = viz.filt_hexbins(rel_hexbin_stats, min_threshold=min_samples)

xlocs = rel_hexbin_stats['xlocs']
ylocs = rel_hexbin_stats['ylocs']
freq_by_hex = np.array([min(max_freq, i) for i in rel_hexbin_stats['freq_by_hex']])
accs_by_hex = rel_hexbin_stats['accs_by_hex']

colorscale = 'RdYlBu_r'
marker_cmin = -0.1
marker_cmax = 0.1
title_txt = "NBA<BR>Shot chart, '18-'19<BR>(Crunchtime vs average)"
hexbin_text = [
        '<i>Accuracy: </i>' + str(round(accs_by_hex[i]*100, 1)) + '%<BR>'
        + 'vs NBA average' for i in range(len(freq_by_hex))
]
ticktexts = ["Worse", "Average", "Better"]

fig = viz.plot_shot_hexbins_plotly(
    xlocs, ylocs, freq_by_hex, accs_by_hex,
    marker_cmin, marker_cmax, colorscale=colorscale,
    title_txt=title_txt, legend_title='Accuracy',
    hexbin_text=hexbin_text, ticktexts=ticktexts)

