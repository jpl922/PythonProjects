# ========== (c) JP Hwang 2020-03-30  ==========

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

# ========== LOAD DATA ==========
messy_df = pd.read_csv('srcdata/demo_messy.csv', index_col=0)
tidy_df = pd.read_csv('srcdata/demo_tidy.csv', index_col=0)

# ========== FILTER FOR COUNTRIES ==========
countries_list = ['China', 'Germany', 'New Zealand', 'South Africa', 'United States']
messy_df_sm = messy_df[messy_df['Country Name'].isin(countries_list)]
tidy_df_sm = tidy_df[tidy_df['Country Name'].isin(countries_list)]

# ========== FILTER FOR YEARS ==========
year_list = ['1995', '2000', '2005', '2010']
var_list = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']
messy_df_sm2 = messy_df[var_list + year_list]

year_list = ['1995', '2000', '2005', '2010']
tidy_df_sm2 = tidy_df[tidy_df['year'].isin(year_list)]

# ========== GET AVERAGE DATA ==========
all_years = ['1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972',
             '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985',
             '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998',
             '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011',
             '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
messy_df_obs = messy_df[all_years]
messy_avg = np.sum(messy_df_obs.sum()) / sum(sum(messy_df_obs.notna().values))

print(tidy_df['hosp_per_1000'].mean())

# ========== CREATE TIDY DATA ==========

# With pandas .melt
tidy_df = messy_df.melt(var_list, [str(i) for i in list(range(1960, 2020))], 'year', 'hosp_per_1000')

# With loops
data_list = list()
for i, row in messy_df.iterrows():
    for yr in [str(i) for i in list(range(1960, 2020))]:
        temp_dict = {k: row[k] for k in var_list}
        temp_dict['year'] = yr
        temp_dict['hosp_per_1000'] = row[yr]
        data_list.append(temp_dict)
tidy_df_2 = pd.DataFrame(data_list)

# ========== SIMPLE DATAVIZ ==========
import plotly.express as px
fig = px.scatter(tidy_df_sm, y='hosp_per_1000', x='year', color='Country Name', template='plotly_white')
fig.show()

fig = px.bar(tidy_df_sm, y='hosp_per_1000', x='year', color='Country Name', template='plotly_white', barmode='group')
fig.show()
