import dataiku as dk 

def footbet_lstm_advanced(club_id,match_dt):
    """ Return a (10,6) Matrix"""
    return """ select home_away_flag,club_point,home_rank,away_rank,home_goal,away_goal
    from
    (select
           case when club_id = home_id then 1 else 0 end as home_away_flag
          ,home_rank,away_rank
          ,case when (club_id = home_id and home_goal > away_goal) or (club_id = away_id and home_goal < away_goal) then 3
                when home_goal = away_goal then 1
                else 0
            end as club_point
          ,home_goal,away_goal
          ,match_dt
          ,row_number() over(order by match_dt desc) as rk 

    from "DATAIMPORT_foot_games_p"

    where club_id = '{0}' and match_dt < '{1}') tmp
    where rk <=10
     """.format(club_id,match_dt) 

def footbet_lstm_simple(club_id,match_dt):
    """ Return a (10,6) Matrix"""
    return """select home_win,home_draw,home_defeat,away_win,away_draw,away_defeat 
from
(select
      case when club_id = home_id and home_goal > away_goal then 1 else 0 end as home_win
      ,case when club_id = home_id and home_goal = away_goal then 1 else 0 end as home_draw
      ,case when club_id = home_id and home_goal < away_goal then 1 else 0 end as home_defeat
 
      ,case when club_id = away_id and home_goal < away_goal then 1 else 0 end as away_win
      ,case when club_id = away_id and home_goal = away_goal then 1 else 0 end as away_draw
      ,case when club_id = away_id and home_goal > away_goal then 1 else 0 end as away_defeat

      ,row_number() over(order by match_dt desc) as rk 
    
from "DATAIMPORT_foot_games_p"

where club_id = '{0}' and match_dt < '{1}') tmp
where rk <=10
""".format(club_id,match_dt)

def footbet_lstm_simple2(club_id,match_dt):
    """ Return a (10,6) Matrix"""
    return """select home_win,home_draw,home_defeat,away_win,away_draw,away_defeat
from
(select club_id,match_dt,home_goal,away_goal
      ,home_rank,away_rank
      ,case when club_id = home_id and home_goal > away_goal then home_goal-away_goal else 0 end as home_win
      ,case when club_id = home_id and home_goal = away_goal then 1 else 0 end as home_draw
      ,case when club_id = home_id and home_goal < away_goal then away_goal-home_goal else 0 end as home_defeat
 
      ,case when club_id = away_id and home_goal < away_goal then away_goal-home_goal else 0 end as away_win
      ,case when club_id = away_id and home_goal = away_goal then 1 else 0 end as away_draw
      ,case when club_id = away_id and home_goal > away_goal then home_goal-away_goal else 0 end as away_defeat

      ,row_number() over(order by match_dt desc) as rk 
    
from "DATAIMPORT_foot_games_p"

where club_id = '{0}' and match_dt < '{1}') tmp
where rk <=10
order by match_dt
""".format(club_id,match_dt)

def footbet_lstm_simple3(club_id,match_dt):
    """ Return a (10,7) Matrix"""
    return """select home_rank/20,away_rank/20,home_win,home_draw,home_defeat,away_win,away_draw,away_defeat
from
(select club_id,match_dt,home_goal,away_goal
      ,home_rank,away_rank
      ,case when club_id = home_id and home_goal > away_goal then home_goal-away_goal else 0 end as home_win
      ,case when club_id = home_id and home_goal = away_goal then 1 else 0 end as home_draw
      ,case when club_id = home_id and home_goal < away_goal then away_goal-home_goal else 0 end as home_defeat
 
      ,case when club_id = away_id and home_goal < away_goal then away_goal-home_goal else 0 end as away_win
      ,case when club_id = away_id and home_goal = away_goal then 1 else 0 end as away_draw
      ,case when club_id = away_id and home_goal > away_goal then home_goal-away_goal else 0 end as away_defeat

      ,row_number() over(order by match_dt desc) as rk 
    
from "DATAIMPORT_foot_games_p"

where club_id = '{0}' and match_dt < '{1}') tmp
where rk <=10
order by match_dt
""".format(club_id,match_dt)


