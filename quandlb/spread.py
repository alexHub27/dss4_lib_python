import numpy as np
import pandas as pd 
from statsmodels.tsa.stattools import adfuller,coint,add_constant
from statsmodels.api import OLS

from quandlb.utils import get_df_data


def get_Z(df_data,ticker_X,ticker_Y,beta,endDate,startDate=None):
    df_data = get_df_data(df_data=df_data,tickerLst=[ticker_X,ticker_Y],endDate=endDate,startDate=startDate)
    return df_data[ticker_Y].values - np.float(beta) * df_data[ticker_X].values

def get_z(stock_X,stock_Y,beta,df_is):
    return df_is[stock_Y]- np.float(beta)*df_is[stock_X]

def std_z(stock_X,stock_Y,beta,df_is):
    # called in get_df_coint
    return np.std(get_z(stock_X,stock_Y,beta,df_is))

def get_half_life(Z):
    z_lag = np.roll(Z,1)
    z_lag[0] = 0
    z_ret = Z - z_lag

    # adds intercept terms to X for regression
    z_lag2 = add_constant(z_lag)
    model = OLS(z_ret,z_lag2).fit()

    return int(-np.log(2)/model.params[1])

def get_half_life_from_scratch(stockX,stockY,beta,df_is):
    # called in get_df_coint
    z_array = get_z(stockX,stockY,beta,df_is)

    z_lag = np.roll(z_array,1)
    z_lag[0] = 0
    z_ret = z_array - z_lag

    # adds intercept terms to X for regression
    z_lag2 = add_constant(z_lag)
    model = OLS(z_ret,z_lag2)
    res = model.fit()

    return int(-np.log(2)/res.params[1])

def get_ma(Z,tr):
    cZ,ma = np.cumsum(Z),np.zeros(Z.shape)
    ma[tr:] = (cZ[tr:]-cZ[:-tr])/float(tr)
    return ma

def get_rstd(Z,tr):
    rstd = np.zeros(Z.shape)
    rstd[tr:] = [np.std(Z[i-tr:i]) for i in range(tr,Z.shape[0]+1)]
    return rstd

def get_std(X,Y,beta,dfs,w):
    z = get_z(X,Y,beta,dfs)
    return np.std(z[-w:])