import dataiku as dk
from utils.sql_calls import footbet_lstm_elo_simple,footbet_lstm_simple2,footbet_lstm_elo_home

def get_target(home_goal,away_goal):
    if home_goal> away_goal:
        return [1,0,0]
    elif home_goal == away_goal:
        return [0,1,0]
    else:
        return [0,0,1]
    
def get_target_bin(home_goal,away_goal):
    if home_goal> away_goal:
        return 1
    else:
        return 0

def get_club_histo_elo(club_id,data):
    executor = dk.core.sql.SQLExecutor2(dataset=data)
    mess = footbet_lstm_elo_simple(club_id)
    return executor.query_to_df(mess)

def get_club_histo_simple2(club_id,match_dt,data):
    executor = dk.core.sql.SQLExecutor2(dataset=data)
    mess = footbet_lstm_simple2(club_id,match_dt)
    return executor.query_to_df(mess)

def get_club_histo_elo_home(club_id,match_dt,home_flag,data):
    executor = dk.core.sql.SQLExecutor2(dataset=data)
    mess = footbet_lstm_elo_home(club_id,home_flag,match_dt)
    return executor.query_to_df(mess)

