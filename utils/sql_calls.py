import dataiku as dk 


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
    """ Return a (15,9) Matrix"""
    return """select home_rank/20.0,away_rank/20.0,home_win/1.0,home_draw/1.0,home_defeat/1.0,away_win/1.0,away_draw/1.0,away_defeat/1.0
from
(select club_id,match_dt,home_goal,away_goal
      ,home_rank,away_rank,match_day
      ,case when club_id = home_id and home_goal > away_goal then home_goal-away_goal else 0 end as home_win
      ,case when club_id = home_id and home_goal = away_goal then 1 else 0 end as home_draw
      ,case when club_id = home_id and home_goal < away_goal then away_goal-home_goal else 0 end as home_defeat
 
      ,case when club_id = away_id and home_goal < away_goal then away_goal-home_goal else 0 end as away_win
      ,case when club_id = away_id and home_goal = away_goal then 1 else 0 end as away_draw
      ,case when club_id = away_id and home_goal > away_goal then home_goal-away_goal else 0 end as away_defeat

      ,row_number() over(order by match_dt desc) as rk 
    
from "DATAIMPORT_foot_games_p"

where club_id = '{0}' and match_dt < '{1}' and home_rank is not null and away_rank is not null ) tmp
where rk <=15
order by match_dt
""".format(club_id,match_dt)


def footbet_lstm_elo_simple(club_id):
    return """select case when home_id = '{0}' then 1 else 0 end as home_flag
      ,case when home_id = '{0}' then proba_home else proba_away end as proba_club
      ,case when home_id = '{0}' then point_home else point_away end as point_club
      ,case when (home_id = '{0}' and home_goal > away_goal) or (away_id = '{0}' and home_goal < away_goal) 
            then 1 
            else 0
        end as target
      ,match_dt
from "FOOTBET_elo_rank"
where home_id = '{0}' or away_id = '{0}' 
order by match_dt""".format(club_id)


