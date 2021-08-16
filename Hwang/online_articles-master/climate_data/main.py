# ========== (c) JP Hwang 2020-01-28  ==========

import logging

# ===== START LOGGER =====
logger = logging.getLogger(__name__)


root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
root_logger.addHandler(sh)

# ==================================================
# ========== LOAD PREPROESSED DATA ==========
# ==================================================

import pandas as pd
flat_avg_df = pd.read_csv('climate_data/srcdata/flat_avg_data.csv', index_col=0)

# ==================================================
# ========== SIMPLE BAR GRAPH ==========
# ==================================================

import plotly.express as px
simple_df = flat_avg_df[(flat_avg_df.site_name == 'ALBANY AIRPORT') & (flat_avg_df.datatype == 'tmax')]
fig = px.bar(simple_df, x='year', y='rel_avg_temp_C', color='rel_avg_temp_C')
fig.show()

# ==================================================
# ========== SIMPLE SUBPLOTS ==========
# ==================================================

site_names = flat_avg_df.site_name.unique()
short_df = flat_avg_df[flat_avg_df.site_name.isin(site_names[:5])]
fig = px.bar(short_df, x='year', y='rel_avg_temp_C', color='rel_avg_temp_C', facet_row='site_name', facet_col='datatype')
fig.show()

# ==================================================
# ========== SUBPLOT BARS - V1 ==========
# ==================================================
from plotly.subplots import make_subplots
import plotly.graph_objects as go

site_names = flat_avg_df.site_name.unique()[:4]
year_list = [yr for yr in flat_avg_df.year.unique() if yr in flat_avg_df.year.unique()]
year_list.sort()

fig = make_subplots(rows=2, cols=2)

for i in range(4):
    site_name = site_names[i]
    temp_vals = list()
    for yr in year_list:
        filt_val = flat_avg_df[
            (flat_avg_df.site_name == site_name)
            & (flat_avg_df.datatype == 'tmax')
            & (flat_avg_df.year == yr)
        ]
        if len(filt_val) > 0:
            temp_val = filt_val.rel_avg_temp_C.values[0]
        else:
            logger.info(f'Filling value for {site_name} in {yr} to be 0')
            temp_val = 0
        temp_vals.append(temp_val)
    fig.add_trace(
        go.Bar(
            x=year_list,
            y=temp_vals,
        ),
        row=(i // 2) + 1, col=((i % 2) + 1),
    )

fig.update_layout(barmode='relative', height=500, width=700)
fig.show(config={'displayModeBar': False})

# ==================================================
# ========== SUBPLOT BARS - V2 ==========
# ==================================================
site_names = flat_avg_df.site_name.unique()[:4]
year_list = [yr for yr in flat_avg_df.year.unique() if yr in flat_avg_df.year.unique()]
year_list.sort()

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=site_names
)

for i in range(4):
    site_name = site_names[i]
    temp_vals = list()
    for yr in year_list:
        filt_val = flat_avg_df[
            (flat_avg_df.site_name == site_name)
            & (flat_avg_df.datatype == 'tmax')
            & (flat_avg_df.year == yr)
        ]
        if len(filt_val) > 0:
            temp_val = filt_val.rel_avg_temp_C.values[0]
        else:
            logger.info(f'Filling value for {site_name} in {yr} to be 0')
            temp_val = 0
        temp_vals.append(temp_val)
    fig.add_trace(
        go.Bar(
            x=year_list,
            y=temp_vals,
            marker=dict(color=temp_vals, colorscale='RdYlBu_r'),
            name=site_names[i]
        ),
        row=(i // 2) + 1, col=((i % 2) + 1),
    )

fig.update_layout(
    barmode='relative', height=500, width=700,
    showlegend=False,
)
fig.update_yaxes(tickvals=[-2, 0, 2], range=[-2.5, 2.5], fixedrange=True)
fig.update_xaxes(fixedrange=True)
fig.show(config={'displayModeBar': False})

# ==================================================
# ========== SUBPLOT BARS - V3 ==========
# ==================================================

subplot_rows = 5
subplot_cols = 4
tot_subplots = subplot_rows * subplot_cols

names_by_obs = list(
    flat_avg_df.groupby('site_name')['avg_temp_C'].count().sort_values(ascending=False).index)
site_names = names_by_obs[:tot_subplots]
year_list = [yr for yr in flat_avg_df.year.unique() if yr in flat_avg_df.year.unique()]
year_list.sort()

fig = make_subplots(
    rows=subplot_rows, cols=subplot_cols,
    shared_xaxes=True, shared_yaxes=True,
    horizontal_spacing=0.03, vertical_spacing=0.03,
    subplot_titles=site_names
)

for i in range(tot_subplots):
    site_name = site_names[i]
    temp_vals = list()
    for yr in year_list:
        filt_val = flat_avg_df[
            (flat_avg_df.site_name == site_name)
            & (flat_avg_df.datatype == 'tmax')
            & (flat_avg_df.year == yr)
        ]
        if len(filt_val) > 0:
            temp_val = filt_val.rel_avg_temp_C.values[0]
        else:
            logger.info(f'Filling value for {site_name} in {yr} to be 0')
            temp_val = 0
        temp_vals.append(temp_val)
    fig.add_trace(
        go.Bar(
            x=year_list,
            y=temp_vals,
            marker=dict(color=temp_vals, colorscale='RdYlBu_r'),
            name=site_names[i]
        ),
        row=(i // subplot_cols) + 1, col=((i % subplot_cols) + 1),
    )

fig.update_layout(
    barmode='relative', height=120 * subplot_rows, width=230 * subplot_cols,
    showlegend=False,
    font=dict(
        family="Arial, Tahoma, Helvetica",
        size=10,
        color="#404040"
    ),
)
fig.update_yaxes(tickvals=[-2, 0, 2], range=[-3, 3], fixedrange=True)
fig.update_xaxes(fixedrange=True)

# To update the title font:
for i in fig['layout']['annotations']:
    i['font'] = dict(size=10, color='#404040')
# Alternatively, use:
fig.update_annotations(patch=dict(font=dict(size=10, color='#404040')))

fig.show(config={'displayModeBar': False})

# ==================================================
# ========== SUBPLOT BARS ==========
# ==================================================

subplot_rows = 5
subplot_cols = 4
tot_subplots = subplot_rows * subplot_cols

years_back = 50
year_list = [yr for yr in flat_avg_df.year.unique() if yr in flat_avg_df.year.unique()]
year_list.sort()
filt_year_list = year_list[-years_back:]

# Get a list of observatories with most counts (and therefore unlikely to be missing data)
names_by_obs = list(
    flat_avg_df[flat_avg_df.year > 2020-years_back].groupby('site_name')['avg_temp_C'].count().sort_values(ascending=False).index)

used_sites = names_by_obs[:tot_subplots]

fig = make_subplots(
    rows=subplot_rows, cols=subplot_cols,
    shared_xaxes=True, shared_yaxes=True,
    horizontal_spacing=0.03, vertical_spacing=0.03,
    subplot_titles=used_sites
)

for i in range(subplot_rows * subplot_cols):
    site_name = used_sites[i]
    temp_vals = list()
    for yr in filt_year_list:
        filt_val = flat_avg_df[
            (flat_avg_df.site_name == site_name)
            & (flat_avg_df.datatype == 'tmax')
            & (flat_avg_df.year == yr)
        ]
        if len(filt_val) > 0:
            temp_val = filt_val.rel_avg_temp_C.values[0]
        else:
            logger.info(f'Filling value for {site_name} in {yr} to be 0')
            temp_val = 0
        temp_vals.append(temp_val)
    fig.add_trace(
        go.Bar(
            x=filt_year_list,
            y=temp_vals,
            marker=dict(color=temp_vals, colorscale='RdYlBu_r'),
            name=used_sites[i]
        ),
        row=(i // subplot_cols) + 1, col=((i % subplot_cols) + 1),
    )

fig.update_layout(
    barmode='relative', height=120 * subplot_rows, width=230 * subplot_cols,
    showlegend=False,
    font=dict(
        family="Arial, Tahoma, Helvetica",
        size=10,
        color="#404040"
    ),
)
fig.update_yaxes(tickvals=[-2, 0, 2], range=[-3, 3], fixedrange=True, visible=False)
fig.update_xaxes(fixedrange=True)

for i in fig['layout']['annotations']:
    i['font'] = dict(size=10, color='#404040')

fig.show(config={'displayModeBar': False})

# ==================================================
# ========== EXPRESS STACKED BARS V1 ==========
# ==================================================

fig = px.bar(flat_avg_df, x='year', y='rel_avg_temp_C', color='rel_avg_temp_C')
fig.show()

# ==================================================
# ========== EXPRESS STACKED BARS V1.5 ==========
# ==================================================

fig = px.bar(
    flat_avg_df,
    x='year', y='rel_avg_temp_C', color='rel_avg_temp_C',
    color_continuous_scale=px.colors.diverging.RdYlBu_r,
    color_continuous_midpoint=0,
    facet_row="datatype",
    hover_name='site_name',
    hover_data=flat_avg_df.columns
)
fig.update_layout(
    plot_bgcolor="white",
)
fig.show(config={'displayModeBar': False})

# ==================================================
# ========== SIMPLE STACKED BARS, NORMALISED ==========
# ==================================================
# Here, we normalise for effects of different numbers of sample sizes

flat_avg_df = flat_avg_df.assign(norm_rel_avg_temp_C=flat_avg_df.rel_avg_temp_C)
for i, row in flat_avg_df.iterrows():
    norm_count = len(flat_avg_df[
                         (flat_avg_df.year == row.year)
                         & (flat_avg_df.datatype == row.datatype)
                     ])
    flat_avg_df.loc[i, 'norm_rel_avg_temp_C'] = flat_avg_df.loc[i, 'rel_avg_temp_C'] / norm_count

fig = px.bar(
    flat_avg_df,
    x='year', y='norm_rel_avg_temp_C', color='rel_avg_temp_C',
    color_continuous_scale=px.colors.diverging.RdYlBu_r,
    color_continuous_midpoint=0,
    facet_row="datatype",
    hover_name='site_name',
    hover_data=flat_avg_df.columns
)
fig.update_layout(
    plot_bgcolor="white",
)
fig.show(config={'displayModeBar': False})

# ==================================================
# ========== SIMPLE STACKED BARS, NORMALISED ==========
# ==================================================
# Here, we normalise for effects of different numbers of sample sizes

fig = px.bar(
    flat_avg_df,
    x='year', y='norm_rel_avg_temp_C', color='rel_avg_temp_C',
    color_continuous_scale=px.colors.diverging.RdYlBu_r,
    color_continuous_midpoint=0,
    facet_row="datatype",
    hover_name='site_name',
    hover_data=['site_name', 'year', 'avg_temp_C', 'datatype']
)
fig.update_yaxes(title_text='Annual temp variation (vs typical, deg C)')
fig.update_layout(
    plot_bgcolor="white",
    title='Temperature trends in Australia since 1910',
    font=dict(
        family="Arial, Tahoma, Helvetica",
        size=12,
        color="#606060"
    ),
    coloraxis_colorbar=dict(
        title=dict(
            text='Relative<br>temperature<br>(at each<br>station)',
            side='bottom'),
        thicknessmode="pixels", thickness=15,
        outlinewidth=2,
        outlinecolor='#909090',
        lenmode="pixels", len=300,
        yanchor="middle", y=0.5,
    ),
    width=1000,
    height=700,
    annotations=[
        go.layout.Annotation(
            x=0.9,
            y=0.05,
            showarrow=False,
            text="Twitter: @_jphwang",
            xref="paper",
            yref="paper",
            textangle=0
        ),
    ],
)
fig.show(config={'displayModeBar': False})
