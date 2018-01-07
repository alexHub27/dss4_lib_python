import dataiku as dk
import numpy as np
import pandas as pd
import datetime as dt

def get_tickerDic(dfNm="sp500_ticker"):
    df_sym= dk.Dataset(dfNm).get_dataframe()
    return {tck:df_sym["GICS Sector"].values[idx] for idx,tck in enumerate(df_sym["Ticker symbol"].values)} 


def get_tickerVol(dfv,entryDate,tickerDic,tshd=1):
    d_ =  dfv.loc[dfv.Date==str(entryDate).split('T')[0]].values[0,1:]
    tickerVol = dict((tick,d_[idx]) for idx,tick in enumerate(list(dfv.columns)[1:]) if d_[idx]<tshd)
    return dict((k,tickerDic[k]) for k in tickerVol) 
       
def get_price_dataframe(dfNm="wiki_sp500_daily_2007"):
    dfs = dk.Dataset(dfNm).get_dataframe()
    dfs["Date"] = pd.to_datetime(dfs.Date.values)
    dfs.index = dfs.Date
    return dfs 

def get_days_tuple2(dateIndex,schLst,tickerDic,startDate=None,endDate=None,w=2000):
    if type(startDate) == str:
        startDate= dt.datetime.strptime(startDate,"%Y-%m-%d")
    if type(endDate) == str:
        endDate = dt.datetime.strptime(endDate,"%Y-%m-%d")
        
    if not startDate or startDate-dt.timedelta(days=w)<min(dateIndex):
        startDate = min(dateIndex)
    if not endDate or endDate>max(dateIndex):
        endDate = max(dateIndex)
    
    t = [(d,d+dt.timedelta(days=w),schLst,tickerDic) for d in dateIndex 
         if d>=startDate-dt.timedelta(days=w) and d+dt.timedelta(days=w)<=endDate ]
    print "Period of study: {0} to {1} - {2} trading days".format(t[0][1],t[-1][1],len(t))
    return t

def get_days_tuple_vol(dateIndex,schLst,tickerDic,dfv,startDate=None,endDate=None,w=2000,tshd=1):
    if type(startDate) == str:
        startDate= dt.datetime.strptime(startDate,"%Y-%m-%d")
    if type(endDate) == str:
        endDate = dt.datetime.strptime(endDate,"%Y-%m-%d")
        
    if not startDate or startDate-dt.timedelta(days=w)<min(dateIndex):
        startDate = min(dateIndex)
    if not endDate or endDate>max(dateIndex):
        endDate = max(dateIndex)
    
    t = [(d,d+dt.timedelta(days=w),schLst,get_tickerVol(dfv,d,tickerDic,tshd)) for d in dateIndex 
         if d>=startDate-dt.timedelta(days=w) and d+dt.timedelta(days=w)<=endDate ]
    print "Period of study: {0} to {1} - {2} trading days".format(t[0][1],t[-1][1],len(t))
    return t

def get_df_data(df_data,tickerLst,endDate,startDate=None):
    if not startDate : 
        startDate = endDate - dt.timedelta(days=365*7.5)
    up = dt.datetime.strptime(dt.datetime.strftime(startDate,'%Y-%m-%d 23:59:00'),'%Y-%m-%d %H:%M:%S')
    down = dt.datetime.strptime(dt.datetime.strftime(startDate,'%Y-%m-%d 00:01:00'),'%Y-%m-%d %H:%M:%S')
    return df_data.loc[(df_data.index>=down)&(df_data.index<=up)][tickerLst]

def get_end_signal(timeStamp,halfLife,fact=3,nbdays=100):
    hl= timeStamp + dt.timedelta(days=fact*halfLife)
    if nbdays:
        maxS = get_max_signal(timeStamp,nbdays=nbdays)
        return min(hl,maxS)
    else:
        return hl

def get_max_signal(entry_date,nbdays=100):
    return entry_date+dt.timedelta(days=nbdays)

