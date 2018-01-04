

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