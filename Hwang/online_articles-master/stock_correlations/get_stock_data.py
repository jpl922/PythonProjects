# ========== (c) JP Hwang 6/5/20  ==========

import logging

# ===== START LOGGER =====
logger = logging.getLogger(__name__)
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
root_logger.addHandler(sh)

import scipy.stats
import pandas as pd
import numpy as np
import requests
import os
import plotly.express as px
import sklearn
import datetime

desired_width = 320
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', desired_width)

# ========== LOAD TOKENS / SET CONSTANTS==========
if 'TIINGO_KEY' in os.environ:
    tiingo_token = os.environ['TIINGO_KEY']
else:
    with open('../tokens/tiingo_token.txt', 'r') as f:
        tiingo_token = f.read().strip()

# ========== LOAD S&P 500 CONSTITUENT DATA  ==========
const_df = pd.read_csv('stock_correlations/srcdata/s_p_500_constituents.csv')  # https://github.com/datasets/s-and-p-500-companies-financials
fin_df = pd.read_csv('stock_correlations/srcdata/s_p_500_constituents_fin.csv').sort_values('Market Cap', ascending=False).reset_index(drop=True)  # https://github.com/datasets/s-and-p-500-companies-financials

# ========== FUNCTION TO GET STOCK DATA ==========
def get_stock_data(tkn, sym='amzn', start_date='2020-01-01'):
    headers = {'Content-Type': 'application/json'}

    requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/" + sym + "/prices?startDate=" + start_date + "&token=" + tkn, headers=headers)
    if requestResponse.status_code == 200:
        logger.info(f'Success fetching {sym} data from {start_date} to today')
    else:
        logger.warning(f'Something looks wrong - status code {requestResponse.status_code}')

    return requestResponse


# ========== GET STOCK DATA ==========

symbols_ser = ['AAPL', 'MSFT', 'JNJ', 'WMT', 'TSM', 'XOM']  # For testing

def dl_stock_df(symbols_in, start_date='2015-01-01'):
    # TODO - add error handling
    ticker_datas = []
    for sym in symbols_in:
        temp_data = get_stock_data(tiingo_token, sym=sym, start_date=start_date).json()
        temp_df = pd.DataFrame(temp_data)
        temp_df['sym'] = sym
        ticker_datas.append(temp_df)

    # Concatenate stock data
    return pd.concat(ticker_datas)


total_ticker_df = dl_stock_df(symbols_ser)

# Sanity check data
fig = px.scatter(total_ticker_df,
                 x='date', y='close', color='sym', template='plotly_white', title='Sample Stock Price Graphs',
                 facet_col='sym', facet_col_wrap=3
                 )
fig.update_yaxes(matches=None, showticklabels=False)  # If we want to simply view curve 'shapes'
fig.update_traces(mode='lines')
fig.show()

# ========== GENERATE ROLLING AVG DATA ==========
# TODO - add this later on / optional module

# ========== COMPARE ONE CURVE VS ANOTHER ==========
# Build a correlation (and p-value) matrix
def build_corr_matrix(df_in):
    symbols_in = df_in.sym.unique()
    r_array_out = np.zeros([len(symbols_in), len(symbols_in)])
    p_array_out = np.zeros([len(symbols_in), len(symbols_in)])
    for i in range(len(symbols_in)):
        for j in range(len(symbols_in)):
            ser_i = df_in[df_in.sym == symbols_in[i]]['close'].values
            ser_j = df_in[df_in.sym == symbols_in[j]]['close'].values
            if len(ser_i) != len(ser_j):
                logger.info(f'lengths for {symbols_in[i]}, row {i} and {symbols_in[j]}, row {j} do not match!')
                r_array_out[i, j] = -2
                p_array_out[i, j] = -2
            else:
                r_ij, p_ij = scipy.stats.pearsonr(ser_i, ser_j)
                r_array_out[i, j] = r_ij
                p_array_out[i, j] = p_ij
    return r_array_out, p_array_out

r_array, p_array = build_corr_matrix(symbols_ser)


fig = px.imshow(r_array, x=symbols_ser, y=symbols_ser,
                color_continuous_scale=px.colors.sequential.Bluyl, color_continuous_midpoint=0,
                )
fig.update_xaxes(side="top")
fig.show()


full_symbols = list(fin_df[:50].Symbol)
total_ticker_df = dl_stock_df(full_symbols)

# Some data rows have incomplete data - filtering these out
grpby_cnts = total_ticker_df.groupby('sym')['date'].count()
incomp_data = grpby_cnts[grpby_cnts < grpby_cnts.max()]
filt_df = total_ticker_df[-total_ticker_df.sym.isin(incomp_data.index)]

# Filter out stocks that go through a split TODO - adjust them for the split
split_stocks = filt_df[filt_df.splitFactor > 1].sym.unique()
filt_df = filt_df[-filt_df.sym.isin(split_stocks)]

# Plot data
r_array, p_array = build_corr_matrix(filt_df)
fig = px.imshow(r_array, x=filt_df.sym.unique(), y=filt_df.sym.unique(),
                color_continuous_scale=px.colors.sequential.Bluyl, color_continuous_midpoint=0,
                )
fig.update_xaxes(side="top")
fig.show()

# Cluster data
model = sklearn.cluster.SpectralBiclustering(n_clusters=3, method='log', random_state=0)
model.fit(r_array)

r_array_srt = r_array[np.argsort(model.row_labels_)]
r_array_srt = r_array_srt[:, np.argsort(model.column_labels_)]
syms_srt = filt_df.sym.unique()[np.argsort(model.row_labels_)]

fig = px.imshow(r_array_srt, x=syms_srt, y=syms_srt,
                color_continuous_scale=px.colors.sequential.Bluyl, color_continuous_midpoint=0,
                )
fig.update_xaxes(side="top")
fig.show()

# See sample charts of correlated stocks
sim_charts = np.argsort(r_array[0])[-6:]
sim_syms = [filt_df.sym.unique()[i] for i in sim_charts]
sim_df = filt_df[filt_df.sym.isin(sim_syms)]
fig = px.scatter(sim_df,
                 x='date', y='close', color='sym', template='plotly_white', title='Sample Stock Price Graphs',
                 facet_col='sym', facet_col_wrap=3
                 )
fig.update_yaxes(matches=None, showticklabels=False)  # If we want to simply view curve 'shapes'
fig.update_traces(mode='lines')
fig.show()

# See sample charts of uncorrelated stocks
dissim_charts = np.argsort(r_array[0])[:5]
dissim_syms = [filt_df.sym.unique()[0]] + [filt_df.sym.unique()[i] for i in dissim_charts]
dissim_df = filt_df[filt_df.sym.isin(dissim_syms)]
fig = px.scatter(dissim_df,
                 x='date', y='close', color='sym', template='plotly_white', title='Sample Stock Price Graphs',
                 facet_col='sym', facet_col_wrap=3
                 )
fig.update_yaxes(matches=None, showticklabels=False)  # If we want to simply view curve 'shapes'
fig.update_traces(mode='lines')
fig.show()

# For filtering data by date:

# filt_df = filt_df[(filt_df.date < str(datetime.fromisoformat('2016-01-01')))]
# filt_df = filt_df[(filt_df.date < str(datetime.fromisoformat('2016-01-01'))) & (filt_df.date >= str(datetime.fromisoformat('2015-01-01')))]
