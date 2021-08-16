# ========== (c) JP Hwang 2020-02-15  ==========

import logging

# ===== START LOGGER =====
logger = logging.getLogger(__name__)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
root_logger.addHandler(sh)

# ===== Load & Inspect Data =====
import plotly.express as px
gap_df = px.data.gapminder()
gap_df = gap_df.assign(gdp=gap_df['pop'] * gap_df['gdpPercap'])

# ===== Visualising single year data only =====
year_df = gap_df[gap_df.year == max(gap_df.year)]
cont_df = year_df.groupby('continent').agg({'gdp': 'sum'})
cont_df.reset_index(inplace=True)

# Pie chart
fig = px.pie(cont_df, values='gdp', names='continent')
fig.show()
# Bar chart
fig = px.bar(cont_df, x='continent', y='gdp')
fig.show()
# Horizontal bar chart - stacked
fig = px.bar(cont_df, color='continent', x='gdp', orientation='h')
fig.show()
# Bubble chart
fig = px.scatter(cont_df.assign(dataType='GDP'), color='continent', x='continent', y='dataType', size='gdp', size_max=50)
fig.show()

# ===== Visualising multiple years' data =====
mul_yrs_df = gap_df[gap_df.year > 1985]
mul_yr_cont_df = mul_yrs_df.groupby(['continent', 'year']).agg({'gdp': 'sum'})
mul_yr_cont_df.reset_index(inplace=True)

# Bar chart
mul_yr_cont_df = mul_yr_cont_df.assign(yrstr=mul_yr_cont_df.year.astype(str))

fig = px.bar(mul_yr_cont_df, color='continent', y='gdp', x='yrstr', barmode='group')
fig.show()
# Horizontal bar chart - stacked
fig = px.bar(mul_yr_cont_df, color='continent', x='gdp', orientation='h', y='yrstr')
fig.show()
# Bubble chart
fig = px.scatter(mul_yr_cont_df, y='continent', x='yrstr', color='continent', size='gdp', size_max=50)
fig.show()

# Different groupings
fig = px.bar(mul_yr_cont_df, color='continent', y='gdp', x='yrstr', barmode='group')
fig.show()
fig = px.bar(mul_yr_cont_df, color='yrstr', y='gdp', x='continent', barmode='group')
fig.show()

# Horizontal subplots
fig = px.bar(mul_yr_cont_df, color='continent', facet_col='continent', x='gdp', orientation='h', facet_row='yrstr')
fig.update_yaxes(showticklabels=False)
fig.show()

# ===== Visualising larger data sets =====
gap_cont_df = gap_df.groupby(['continent', 'year']).agg({'gdp': 'sum'})
gap_cont_df.reset_index(inplace=True)
gap_cont_df = gap_cont_df.assign(yrstr=gap_cont_df.year.astype(str))


# Bar chart
fig = px.bar(gap_cont_df, color='continent', y='gdp', x='yrstr', barmode='group')
fig.show()
# Horizontal bar chart - stacked
fig = px.bar(gap_cont_df, color='continent', x='gdp', orientation='h', y='yrstr')
fig.show()
# Bubble chart
fig = px.scatter(gap_cont_df, y='continent', x='yrstr', color='continent', size='gdp', size_max=50)
fig.show()

# Horizontal subplots
fig = px.bar(
    gap_cont_df, color='continent', facet_col='continent', x='gdp', orientation='h', facet_row='yrstr'
)
# fig.for_each_shape(lambda t: t.update(name=t.name.replace("yrstr=", "")))
fig.for_each_annotation(lambda t: t.update(text=t.text.replace("yrstr=", "")))
fig.for_each_annotation(lambda t: t.update(text=t.text.replace("continent=", "")))
fig.update_yaxes(showticklabels=False)
fig.show()


# ===== Visualising larger data sets =====
countries_df = gap_df[
     (gap_df.country.str.startswith('A'))
]
countries_df['yrstr'] = countries_df['year'].astype(str)
# Bar chart
fig = px.bar(countries_df, color='country', y='gdp', x='yrstr', barmode='group')
fig.show()
# Horizontal bar chart - stacked
fig = px.bar(countries_df, color='country', x='gdp', orientation='h', y='yrstr')
fig.show()
# Bubble chart
fig = px.scatter(countries_df, y='country', x='yrstr', color='country', size='gdp', size_max=50)
fig.show()
# Horizontal subplots
fig = px.bar(
    countries_df, color='country', facet_col='country', x='gdp', orientation='h', facet_row='yrstr'
)
# fig.for_each_shape(lambda t: t.update(name=t.name.replace("yrstr=", "")))
fig.for_each_annotation(lambda t: t.update(text=t.text.replace("yrstr=", "")))
fig.for_each_annotation(lambda t: t.update(text=t.text.replace("continent=", "")))
fig.update_yaxes(showticklabels=False)
fig.show()


# ===== Visualising larger data sets =====
def clean_chart_format(fig):

    import plotly.graph_objects as go

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        annotations=[
            go.layout.Annotation(
                x=0.9,
                y=0.02,
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

import pandas as pd
team_summary_df = pd.read_csv('viz_proportions/srcdata/raptors_18_19_shots_summary_2mins.csv', index_col=0)

# Bar chart
fig = px.bar(team_summary_df, color='player', y='shots_freq', x='min_end', barmode='group')
fig.show()
# Horizontal bar chart - stacked
fig = px.bar(team_summary_df, color='player', x='shots_freq', orientation='h', y='min_end')
fig.show()

# Bubble chart
fig = px.scatter(
    team_summary_df, y='player', x='min_end', color='pl_pps', size='shots_freq', size_max=15,
    color_continuous_scale = px.colors.sequential.GnBu,
    range_color=[90, 120],
    range_x=[0, 49],
)
clean_chart_format()
leaders_title = "Leaders in portion of team's shots taken (2018-19 NBA Season)"
fig.update_layout(title=leaders_title, height=500, width=1000)
fig.update_coloraxes(colorbar=dict(title='Player<BR>points/100'))
fig.update_traces(marker=dict(sizeref=2. * 30 / (22 ** 2)))
fig.update_yaxes(title="Player")
fig.update_xaxes(title='Minute', tickvals=list(range(0, 54, 6)))
fig.show()
