import pandas as pd
import numpy as np

from statsmodels.tsa.stattools import adfuller,coint,add_constant
from statsmodels.api import OLS

from quandl.stats import coint_alex,adfuller_alex
import datetime as dt

from quandl.spread import get_half_life_from_scratch,get_z,std_z

def get_corrLst(df_is,tickerDic):
    #  called in main
    corrList = []
    for idx,tickX in enumerate(df_is.columns):
        for j in range(idx+1,len(df_is.columns)):
            tickY = df_is.columns[j]
            if tickerDic[tickX] == tickerDic[tickY]:
                corr = np.corrcoef(df_is[tickX].values,df_is[tickY].values)[0,1]
                dist = np.sum(np.power(df_is[tickX].values-df_is[tickY].values,2))
                if corr >0.9:
                    corrList.append([tickX,tickY,corr,dist])

    print "There are {0} pairs strongly correlated.".format(len(corrList))
    return corrList

def get_cointLst(corrList,df_is):
    # called in main
    # Test cointegration the test has to be perform on both side of the spread
    cointLst = []
    for pair in corrList:
        X1,X2 = df_is[pair[0]].values,df_is[pair[1]].values 

        x1 = add_constant(X1) 
        x2 =add_constant(X2)
        r1 = OLS(X2,x1).fit() 
        r2 = OLS(X1,x2).fit()

        adf1= adfuller(r1.resid)[1] 
        if adf1<0.01 : 
            adf2 = adfuller(r2.resid)[1]
            if adf2<0.01 and adf1 < adf2: # Test for strong cointegration in both side only.
                cointLst.append(["{0}_{1}".format(pair[0],pair[1])]+pair+[adf1]+list(r1.params))
            elif adf2<0.01:
                cointLst.append(["{0}_{1}".format(pair[1],pair[0])]+[pair[1],pair[0],pair[2],pair[3],adf2]+list(r2.params))
                            
    print "There are {0} pairs strongly cointegrated.".format(len(cointLst))
    return cointLst

def get_cointLst2(corrList,df_is):
    # called in main
    # Test cointegration the test has to be perform on both side of the spread
    cointLst = []
    for pair in corrList:
        X1,X2 = df_is[pair[0]].values,df_is[pair[1]].values 

        adf1,pval1,params1 = adfuller_alex(X2,X1)

        if pval1<0.01 : 
            adf2,pval2,params2 = adfuller_alex(X1,X2)
            if pval2<0.01 and pval1 < pval2: # Test for strong cointegration in both side only.
                cointLst.append(["{0}_{1}".format(pair[0],pair[1])]+pair+[pval1]+list(params1))
            elif pval2<0.01:
                cointLst.append(["{0}_{1}".format(pair[1],pair[0])]+[pair[1],pair[0],pair[2],pair[3],pval2]+list(params2))
                            
    print "There are {0} pairs strongly cointegrated.".format(len(cointLst))
    return cointLst

def get_df_coint(cointLst,tickerDic,df_is):
    # called in main
    # Make df_coint
    df_coint = pd.DataFrame(np.array(cointLst),columns=["spreadNm","stock_X","stock_Y","coefcorr","dist"
                                                        ,"adf","const","beta"])
    # Computing half life
    df_coint["half_life"] = [get_half_life_from_scratch(tck,df_coint.stock_X.values[idx],df_coint.beta.values[idx],df_is) 
                             for idx,tck in enumerate(df_coint.stock_X.values)]
    df_coint = df_coint.loc[df_coint["half_life"]>0]
    
    df_coint["sector"] = [tickerDic[tck] for tck in df_coint.stock_X.values]
    
    
    # Compute the mean and the std per pairs
    df_coint["stdv"] = [std_z(X,df_coint.stock_Y.values[idx],df_coint.beta.values[idx],df_is) 
                       for idx,X in enumerate(df_coint.stock_X.values)]
    df_coint["lastPrice"] = [get_z(X,df_coint.stock_Y.values[idx],df_coint.beta.values[idx],df_is)[-1] 
                             for idx,X in enumerate(df_coint.stock_X.values)]
    df_coint["last_Zscore"] = [(lp - np.float(df_coint.const.values[idx]))/np.float(df_coint.stdv.values[idx])
                               for idx,lp in enumerate(df_coint.lastPrice.values)]
    
    print "Df_shape : ",df_coint.shape
    return df_coint


def get_risk_mngt(df_coint,sector=None,maxPair=None,maxPerSector=10,maxStd=10,maxHalfLife=60,absZ=1):
    # called in main
    
    # Risk management policy: Sectors
    if sector:
        df_coint["RN"] = df_coint.sort_values(['adf']).groupby(['sector']).cumcount()+1
        df_coint = df_coint.loc[df_coint["RN"]<=maxPerSector][df_coint.columns[:-1]]
    else:
        pass
    
    # Risk management policy + Signals: Limit the risk of the spread (length on hold and vol of spread)
    q = 'half_life <= {0} and stdv <= {1} and (last_Zscore < -{2} or last_Zscore > {2})'.format(maxHalfLife,maxStd,absZ)
    df_trade = df_coint.query(q)

    # Risk management policy: Taking only the strongest pairs
    if maxPair:
        df_trade = df_trade.sort_values(["adf","half_life"]).head(maxPair)
                        
    print "There is {0} signals compliant with risk policy.".format(df_trade.shape[0])
    return df_trade

def money_mngt(df_tradeToday,endDate):
    # called in main
    df_tradeToday["timeStamp"] = [endDate for i in range(df_tradeToday.shape[0])]
    df_tradeToday["entryPrice"] = [lp for lp in df_tradeToday.lastPrice.values]
    df_tradeToday["typeOrder"] = [1 if z<0 else -1 for z in df_tradeToday.last_Zscore.values]
    df_tradeToday["pnl"] = df_tradeToday["lastPrice"] - df_tradeToday["entryPrice"]
    
    print "df_tradeToday: ",df_tradeToday.shape
    return df_tradeToday
