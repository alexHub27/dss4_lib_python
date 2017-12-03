import dataiku as dk
import numpy as np
import pandas as pd
import datetime as dt
import 

def get_tickerDic(dfNm="sp500_ticker"):
    df_sym= dk.Dataset(dfNm).get_dataframe()
    sectors = np.unique(df_sym["GICS Sector"].values)
    return {tck:df_sym["GICS Sector"].values[idx] for idx,tck in enumerate(df_sym["Ticker symbol"].values)} 

def get_price_dataframe(dfNm="wiki_sp500_daily_2007"):
    dfs = dk.Dataset(dfNm).get_dataframe()
    dfs["Date"] = pd.to_datetime(dfs.Date.values)
    dfs.index = dfs.Date
    return dfs 

