# ========== (c) JP Hwang 2020-02-20  ==========

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

season_tot_df = pd.read_csv('srcdata/bballref_1819_season_tots_1000plus_mins.csv', index_col=0)

# ========== Import & set up plotly ==========
import plotly.express as px


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
                text="Twitter: @_jphwang",
                xref="paper",
                yref="paper",
                textangle=0
            ),
        ],
    )
    fig.update_traces(marker=dict(line=dict(width=1, color='Navy')),
                      selector=dict(mode='markers'))
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


# ========== PLOT A SIMPLE BAR CHART OF FANTASY POINTS ==========

fig = px.bar(season_tot_df, y='fan_ppg', x='name',
             labels={'fan_ppg': 'Fantasy points / game', 'name': 'Player'})
clean_chart_format(fig, namelocs=[0.9, 0.9])
fig.update_layout(font={'size': 10})
fig.show()

# ========== LOOK AT (OSTENSIBLY) SIMILAR FANTASY PLAYERS ==========
print(season_tot_df[season_tot_df['name'].isin(['Eric Bledsoe', 'Khris Middleton'])].fan_ppg)

# ========== LOAD PLAYER PER GAME DATA ==========
import pickle

with open('srcdata/bballref_1819_pl_box.pickle', 'rb') as f:
    pl_data_dict = pickle.load(f)


def add_fan_pts(in_df):
    in_df = in_df.assign(
        fan_pts=(
                (in_df.points_scored +
                 (in_df.offensive_rebounds + in_df.defensive_rebounds) * 1.2 +
                 in_df.assists * 1.5 + in_df['blocks'] * 2 + in_df.steals * 2 - in_df.turnovers)
        )
    )
    return in_df


# ========== COMPARE KHRIS MIDDLETON AND ERIC BLEDSOE ==========
temp_df_list = list()
temp_slugs = season_tot_df[season_tot_df['name'].isin(['Eric Bledsoe', 'Khris Middleton'])].slug.unique()
for pl_slug in temp_slugs:
    temp_df = pd.DataFrame(pl_data_dict[pl_slug])
    temp_df = add_fan_pts(temp_df)
    temp_df = temp_df.assign(player=season_tot_df[season_tot_df.slug == pl_slug]['name'].values[0])
    temp_df_list.append(temp_df)
comp_df = pd.concat(temp_df_list, axis=0)
comp_df.reset_index(inplace=True, drop=True)


# ========== VISUALIZE PER GAME DATA ==========
fig = px.bar(comp_df, y='fan_pts', color='player', facet_col='player', labels={'fan_pts': 'Fantasy Points', 'date': 'Date'})
clean_chart_format(fig, namelocs=[0.1, 0.9])
fig.update_layout(title='Fantasy performance comparison')
fig.show()

fig = px.histogram(
    comp_df, x='fan_pts', facet_row='player', color='player',
    labels={'fan_pts': 'Fantasy Points', 'count': 'Count'}, nbins=30)
clean_chart_format(fig, namelocs=[0.1, 0.9])
fig.update_layout(title='Fantasy performance comparison')
fig.show()


# ========== VISUALIZE DISTRIBUTIONS ==========
# Box plot
fig = px.box(comp_df, x='player', y='fan_pts', color='player', labels={'fan_pts': 'Fantasy Points', 'date': 'Date'})
clean_chart_format(fig, namelocs=[0.1, 0.9])
fig.update_layout(title='Fantasy performance comparison')
fig.show()

# Box plot w/ points
fig = px.box(comp_df, x='player', y='fan_pts', color='player', labels={'fan_pts': 'Fantasy Points', 'date': 'Date'}, points="all")
clean_chart_format(fig, namelocs=[0.1, 0.9])
fig.update_layout(title='Fantasy performance comparison')
fig.show()

# Box plot w/ points
fig = px.violin(comp_df, x='player', y='fan_pts', color='player', labels={'fan_pts': 'Fantasy Points', 'date': 'Date'}, points="all")
clean_chart_format(fig, namelocs=[0.5, 0.95])
fig.update_layout(title='Fantasy performance comparison')
fig.show()

# ========== COMPARE MORE PLAYERS ==========
top_pl_df_list = list()
temp_slugs = season_tot_df[(season_tot_df.fan_ppg > 35) & (season_tot_df.fan_ppg < 40)].slug.unique()
for pl_slug in temp_slugs:
    temp_df = pd.DataFrame(pl_data_dict[pl_slug])
    temp_df = add_fan_pts(temp_df)
    temp_df = temp_df.assign(player=season_tot_df[season_tot_df.slug == pl_slug]['name'].values[0])
    top_pl_df_list.append(temp_df)
top_pl_df = pd.concat(top_pl_df_list, axis=0)
top_pl_df.reset_index(inplace=True, drop=True)
# Box plot
fig = px.box(top_pl_df, x='player', y='fan_pts', labels={'fan_pts': 'Fantasy Points', 'date': 'Date'})
clean_chart_format(fig, namelocs=[0.9, 0.9])
fig.update_layout(title='Fantasy performance comparison - 35-40 Points/game', font=dict(size=10))
fig.show()
# Histogram plot
fig = px.histogram(top_pl_df, x='fan_pts', facet_col='player', facet_col_wrap=3,
                   labels={'fan_pts': 'Fantasy Points', 'date': 'Date'}, hover_name='player')
clean_chart_format(fig, namelocs=[0.9, 0.95])
fig.update_layout(title='Fantasy performance comparison - 35-40 Points/game', font=dict(size=10))
fig.show()

# ========== COMPARE EVEN MORE PLAYERS ==========
top_pl_df_list = list()
temp_slugs = season_tot_df[(season_tot_df.fan_ppg > 30) & (season_tot_df.fan_ppg < 40)].slug.unique()
for pl_slug in temp_slugs:
    temp_df = pd.DataFrame(pl_data_dict[pl_slug])
    temp_df = add_fan_pts(temp_df)
    temp_df = temp_df.assign(player=season_tot_df[season_tot_df.slug == pl_slug]['name'].values[0])
    top_pl_df_list.append(temp_df)
top_pl_df = pd.concat(top_pl_df_list, axis=0)
top_pl_df.reset_index(inplace=True, drop=True)
# Box plot
fig = px.box(top_pl_df, x='player', y='fan_pts', labels={'fan_pts': 'Fantasy Points', 'date': 'Date'})
clean_chart_format(fig, namelocs=[0.9, 0.9])
fig.update_layout(title='Fantasy performance comparison - top players', font=dict(size=10))
fig.show()

# ========== PLOT ALL PLAYERS BY CONSISTENCY ==========
# Find players with highest stdev / avg ratio:
pl_pts_list = list()
for pl_slug in season_tot_df.slug.values:
    temp_df = pd.DataFrame(pl_data_dict[pl_slug])
    temp_df = add_fan_pts(temp_df)
    fan_pts_mean = temp_df.fan_pts.mean()
    fan_pts_std = temp_df.fan_pts.std()
    temp_dict=dict(
        player=season_tot_df[season_tot_df.slug == pl_slug]['name'].values[0],
        fan_pts_mean=round(fan_pts_mean, 3),
        fan_pts_std=round(fan_pts_std, 3),
    )
    pl_pts_list.append(temp_dict)

pl_pts_df = pd.DataFrame(pl_pts_list)
pl_pts_df = pl_pts_df.assign(fan_pts_std_vs_mean=round(pl_pts_df.fan_pts_std/pl_pts_df.fan_pts_mean, 3))
fig = px.scatter(
    pl_pts_df, x='fan_pts_mean', y='fan_pts_std', color='fan_pts_std_vs_mean',
    # labels={'fan_pts_mean': 'Mean Points', 'fan_pts_std': 'Standard Deviation'},
    labels={'fan_pts_mean': 'Typical', 'fan_pts_std': 'Variability', 'fan_pts_std_vs_mean': 'Variability vs Typical'},
    hover_name='player')
clean_chart_format(fig, namelocs=[0.1, 0.9])
fig.update_layout(
    title='Fantasy performance - Variability vs Mean', font=dict(size=10),
    coloraxis_colorbar=dict(title=dict(text='Variability<BR>vs Typical'))
)

fig.show(config=dict(displayModeBar=False))

# ========== CORRELATIONS - Harden / CP3 ==========

temp_df_list = list()
temp_slugs = season_tot_df[season_tot_df['name'].isin(['James Harden', 'Chris Paul'])].slug.unique()
for pl_slug in temp_slugs:
    temp_df = pd.DataFrame(pl_data_dict[pl_slug])
    temp_df = add_fan_pts(temp_df)
    temp_df = temp_df.assign(player=season_tot_df[season_tot_df.slug == pl_slug]['name'].values[0])
    temp_df_list.append(temp_df)
comp_df = pd.concat(temp_df_list, axis=0)
comp_df.reset_index(inplace=True, drop=True)

dates_grp = comp_df.groupby('date').count()
dates_both_played = dates_grp[dates_grp['team'] == 2].index
# comb_dates_df = comp_df[comp_df.date.isin(dates_both_played)]
comb_dates_list = list()
for temp_date in dates_both_played:
    jh_points = comp_df[(comp_df.date == temp_date) & (comp_df.player == 'James Harden')].fan_pts.values[0]
    cp_points = comp_df[(comp_df.date == temp_date) & (comp_df.player == 'Chris Paul')].fan_pts.values[0]
    temp_dict = dict(
        date=temp_date,
        Harden=jh_points,
        Paul=cp_points,
        Sum=jh_points+cp_points,
    )
    comb_dates_list.append(temp_dict)
comb_dates_df = pd.DataFrame(comb_dates_list)

fig = px.scatter(comb_dates_df, x='Harden', y='Paul', color='Sum', range_color=[40, 125], range_y=[8, 55])
clean_chart_format(fig, namelocs=[0.1, 0.9])
fig.update_layout(title='Fantasy performance comparison')
fig.show()

# Replace CP3 with another player (Khris Middleton)
temp_df_list = list()
temp_slugs = season_tot_df[season_tot_df['name'].isin(['James Harden', 'Khris Middleton'])].slug.unique()
for pl_slug in temp_slugs:
    temp_df = pd.DataFrame(pl_data_dict[pl_slug])
    temp_df = add_fan_pts(temp_df)
    temp_df = temp_df.assign(player=season_tot_df[season_tot_df.slug == pl_slug]['name'].values[0])
    temp_df_list.append(temp_df)
comp_df = pd.concat(temp_df_list, axis=0)
comp_df.reset_index(inplace=True, drop=True)

dates_grp = comp_df.groupby('date').count()
dates_both_played = dates_grp[dates_grp['team'] == 2].index
comb_dates_list = list()
for temp_date in dates_both_played:
    jh_points = comp_df[(comp_df.date == temp_date) & (comp_df.player == 'James Harden')].fan_pts.values[0]
    km_points = comp_df[(comp_df.date == temp_date) & (comp_df.player == 'Khris Middleton')].fan_pts.values[0]
    temp_dict = dict(
        date=temp_date,
        Harden=jh_points,
        Middleton=km_points,
        Sum=jh_points+km_points,
    )
    comb_dates_list.append(temp_dict)
comb_dates_df = pd.DataFrame(comb_dates_list)

fig = px.scatter(comb_dates_df, x='Harden', y='Middleton', color='Sum', range_color=[40, 125], range_y=[8, 55])
clean_chart_format(fig, namelocs=[0.1, 0.9])
fig.update_layout(title='Fantasy performance comparison')
fig.show()
