import dataiku as dk
from utils.sql_calls import footbet_lstm_elo_global,footbet_lstm_elo_flag,footbet_lstm_simple2
                           ,footbet_lstm_elo_form_flag,footbet_lstm_elo_form_global

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

def get_club_histo_elo_global(club_id,dataNm):
    executor = dk.core.sql.SQLExecutor2(dataset=dk.Dataset(dataNm))
    mess = footbet_lstm_elo_global(club_id,dataNm)
    return executor.query_to_df(mess)

def get_club_histo_elo_flag(home_flag,club_id,dataNm):
    executor = dk.core.sql.SQLExecutor2(dataset=dk.Dataset(dataNm))
    mess = footbet_lstm_elo_flag(home_flag,club_id,dataNm)
    return executor.query_to_df(mess)

def get_club_histo_elo_form_flag(home_flag,club_id,match_dt,w,dataNm='elo_rank_club_test'):
    executor = dk.core.sql.SQLExecutor2(dataset=dk.Dataset(dataNm))
    mess = footbet_lstm_elo_form_flag(home_flag,club_id,match_dt,w,dataNm)
    return executor.query_to_df(mess)

def get_club_histo_elo_form_global(club_id,match_dt,w,dataNm='elo_rank_club_test'):
    executor = dk.core.sql.SQLExecutor2(dataset=dk.Dataset(dataNm))
    mess = footbet_lstm_elo_form_global(club_id,match_dt,w,dataNm)
    return executor.query_to_df(mess)

#########################

def get_club_histo_simple2(club_id,match_dt,data):
    executor = dk.core.sql.SQLExecutor2(dataset=data)
    mess = footbet_lstm_simple2(club_id,match_dt)
    return executor.query_to_df(mess)

