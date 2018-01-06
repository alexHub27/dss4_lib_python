import numpy as np
import pandas as pd
import datetime as dt
from statsmodels.tsa.stattools import adfuller,coint,add_constant
from quandlb.spread import get_Z,get_ma,get_rstd

def get_bbsc(dicTr,Zlen,per=21):
    startDate,endDate = get_startDate(dicTr['entry_date'],15),get_end_signal(dicTr['entry_date'],dicTr['half_life'],fact=5,nbdays=100)
    
    Z = get_Z(df_data=dfs,ticker_X=dicTr['stock_x'],ticker_Y=dicTr['stock_y']
              ,beta=dicTr['beta'],endDate=endDate,startDate=startDate)
    
    mdMa = get_ma(Z,per)
    rstd = get_rstd(Z,per)
    zsc = (Z - mdMa)/rstd
    return zsc[-Zlen-1:-1]

def stop_coint(radf):
    if radf>0.01:
        return True
    else: 
        return None
    
  
    
# Describing trade
def describe_trade(dicRow):
    if dicRow['pos']>0 :
        pos = 'long'
    else:
        pos = 'short'
    mes= "{0} open {1} in {2} at {3} ended {4} at {5} for {6} : {7} \nsig: {8} - {9} zsc : {10} - {11}".format(dt.datetime.strftime(startDate,"%Y-%m-%d"),pos
                                                                     ,dicRow['spreadnm'],round(dicRow['last_price'],2)
                                                                     ,dt.datetime.strftime(dicRow["exitday"],"%Y-%m-%d")
                                                                     ,round(dicRow['exit_price'],2),round(pnl,2),reason
                                                                     ,round(dicRow['fs_nmacd'],2),round(dicRow['exit_fs_nmacd'],2)
                                                                     ,round(dicRow['last_zsc'],2),round(dicRow['exit_zsc'],2))
    return mes

def get_startDate(entryDate,weekBack=15):
    return entryDate - dt.timedelta(days=weekBack*7)

def get_radf(startDate,endDate,tickX,tickY,beta,dfs):
    startDateAdf = startDate - dt.timedelta(days=2800)
    zAdf = get_Z(ticker_X=tickX,ticker_Y=tickY,beta=beta,startDate=startDateAdf,endDate=endDate,df_data=dfs)
    w = zAdf.shape[0] - Z.shape[0]
    rAdf = np.array([adfuller(zAdf[i+1-w:i+1],autolag=None,regression='c')[1] for i in range(w,zAdf.shape[0])])
    assert (len(rAdf)==len(Z))
    return rAdf

def get_nmacd(dicTr,Zlen,f=5,s=63):
    startDate = get_startDate(dicTr['entry_date'],30)
    
    Z = get_Z(df_data=dfs,ticker_X=dicTr['stock_x'],ticker_Y=dicTr['stock_y']
              ,beta=dicTr['beta'],endDate=dicTr['max_date'],startDate=startDate)
    
    Z = (Z-dicTr['const'])/dicTr['stdv']
    faMa,slMa = get_ma(Z,f),get_ma(Z,s)
    rstd = get_rstd(Z,s)  
    zsc = (faMa - slMa)/rstd
    return zsc[-Zlen-1:-1]

def get_bbsc(dicTr,Zlen,p):
    startDate = get_startDate(dicTr['entry_date'],30)
    
    Z = get_Z(df_data=dfs,ticker_X=dicTr['stock_x'],ticker_Y=dicTr['stock_y']
              ,beta=dicTr['beta'],endDate=dicTr['max_date'],startDate=startDate)
    
    Z = (Z-dicTr['const'])/dicTr['stdv']
    ma,rstd = get_ma(Z,p),get_rstd(Z,p)
    bbsc = (Z - ma)/rstd
    return bbsc[-Zlen-1:-1]

def exit_bb(pos,z,r=0.5,ex='TP'):
    if (ex=='TP' and pos==1 and z>r) or (ex=='TP' and pos == -1 and z<-r) or (ex=='TL' and pos==1 and z<-r) or (ex=='TL' and pos==-1 and z>r):
        return True
    else :
        return None
    
def stop_bb(pos,zi,p,r=1,ex='TP'):
    assert (r>=0),("r:{0} must be positive".format(r))
    if (ex=='TP' and pos==1 and (p-zi)>r) or (ex=='TP' and pos==-1 and (zi-p)>r) or (ex=='TL' and pos==1 and (zi-p)>r) or (ex=='TL' and pos==-1 and (p-zi)>r):
        return True
    else:
        return None