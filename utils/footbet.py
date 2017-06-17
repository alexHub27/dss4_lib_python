import dataiku as dk
from utils.sql_calls import footbet_lstm_simple,footbet_lstm_simple2,footbet_lstm_advanced

def get_target(home_goal,away_goal):
    if home_goal> away_goal:
        return [1,0,0]
    elif home_goal == away_goal:
        return [0,1,0]
    else:
        return [0,0,1]
    
def get_target_bin(home_goal,away_goal):
    if home_goal> away_goal:
        return [1,0]
    else:
        return [0,1]
    
    
def get_club_histo_simple(club_id,match_dt,data):
    executor = dk.core.sql.SQLExecutor2(dataset=data)
    mess = footbet_lstm_simple2(club_id,match_dt)
    return executor.query_to_df(mess)

def get_club_histo_advanced(club_id,match_dt,data):
    executor = dk.core.sql.SQLExecutor2(dataset=data)
    mess = footbet_lstm_advanced(club_id,match_dt)
    return executor.query_to_df(mess)