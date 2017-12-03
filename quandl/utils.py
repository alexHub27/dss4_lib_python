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


def get_df_data(df_data,tickerLst,endDate,startDate=None):
    if not startDate : 
        startDate = endDate - dt.timedelta(days=365*7.5)
    return df_data.loc[(df_data.index>startDate)&(df_data.index<endDate)][tickerLst]

def get_end_signal(timeStamp,halfLife,fact=5):
    return timeStamp + dt.timedelta(days=fact*halfLife)

