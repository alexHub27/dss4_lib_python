import datetime as dt 
import numpy as np
import pandas as pd 
from statsmodels.tsa.stattools import adfuller,coint,add_constant
from statsmodels.api import OLS

def get_Z(ticker_X,ticker_Y,beta,timeStamp,df_data):
    start = timeStamp - dt.timedelta(days=252*7.5)
    df_data = df_data.loc[(df_data.index>start)&(df_data.index<timeStamp)][[ticker_X,ticker_Y]]
    return df_data[ticker_Y].values - np.float(beta) * df_data[ticker_X].values


def get_half_life(Z):
    z_lag = np.roll(Z,1)
    z_lag[0] = 0
    z_ret = Z - z_lag

    # adds intercept terms to X for regression
    z_lag2 = add_constant(z_lag)
    model = OLS(z_ret,z_lag2)
    res = model.fit()

    return int(-log(2)/res.params[1])