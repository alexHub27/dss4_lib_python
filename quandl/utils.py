import dataiku as dk
import numpy as np
import pandas as pd
import datetime as dt

def get_tickerDic(dfNm="sp500_ticker"):
    df_sym= dk.Dataset(dfNm).get_dataframe()
    sectors = np.unique(df_sym["GICS Sector"].values)
    return {tck:df_sym["GICS Sector"].values[idx] for idx,tck in enumerate(df_sym["Ticker symbol"].values)} 

def get_price_dataframe(dfNm="wiki_sp500_daily_2007"):
    dfs = dk.Dataset(dfNm).get_dataframe()
    dfs["Date"] = pd.to_datetime(dfs.Date.values)
    dfs.index = dfs.Date
    return dfs 

def get_Z(ticker_X,ticker_Y,beta,timeStamp,df_data):
    start = timeStamp - dt.timedelta(days=252*7.5)
    df_data = df_data.loc[(df_data.index>start)&(df_data.index<timeStamp)][[ticker_X,ticker_Y]]
    return df_data[ticker_Y].values - beta * df_data[ticker_X].values


def get_half_life(Z):
    
    z_array = get_z(stockX,stockY,beta,df_is)

    z_lag = np.roll(Z,1)
    z_lag[0] = 0
    z_ret = Z - z_lag

    # adds intercept terms to X for regression
    z_lag2 = add_constant(z_lag)
    model = OLS(z_ret,z_lag2)
    res = model.fit()

    return int(-log(2)/res.params[1])