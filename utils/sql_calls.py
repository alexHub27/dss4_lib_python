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


def footbet_lstm_elo(club_id,match_dt):
    """ return a (10,9) Matrix """
    return """ select club_rank,adv_rank,club_proba 
                     ,club_point_home_win,club_point_home_draw,club_point_home_defeat
                     ,club_point_away_win,club_point_away_draw,club_point_away_defeat
from
(select 
       case when home_id = '{0}' 
            then (cast(home_rank as numeric)-1000)/60 
            else (cast(away_rank as numeric)-1000)/60 
        end as club_rank
      ,case when home_id = '{0}' 
            then (cast(away_rank as numeric)-1000)/60 
            else (cast(home_rank as numeric)-1000)/60 
        end as adv_rank
      ,case when home_id = '{0}' 
            then (cast(proba_home as numeric) - 0.5)/0.1 
            else (cast(proba_away as numeric) - 0.5)/0.1
        end as club_proba
        
      ,case when (home_id = '{0}' and home_goal>away_goal) then (cast(point_home as numeric)-2)/8 else 0 end as club_point_home_win
      ,case when (home_id = '{0}' and home_goal=away_goal) then (cast(point_home as numeric)-2)/8 else 0 end as club_point_home_draw
      ,case when (home_id = '{0}' and home_goal<away_goal) then (cast(point_home as numeric)-2)/8 else 0 end as club_point_home_defeat
   
      ,case when (away_id = '{0}' and home_goal<away_goal) then (cast(point_home as numeric)-2)/8 else 0 end as club_point_away_win
      ,case when (away_id = '{0}' and home_goal=away_goal) then (cast(point_home as numeric)-2)/8 else 0 end as club_point_away_draw
      ,case when (away_id = '{0}' and home_goal>away_goal) then (cast(point_home as numeric)-2)/8 else 0 end as club_point_away_defeat
      
      ,row_number() over(order by match_dt desc) as rk
      ,match_dt
    
from "FOOTBET_elo_rank"
where (home_id = '{0}' or away_id = '{0}') and match_dt < '{1}' )tmp
where rk <= 10
order by match_dt desc """.format(club_id,match_dt)

def footbet_lstm_elo_simple(club_id):
    return """select case when home_id = '{0}' then 1 else 0 end as home_flag
      ,case when home_id = '{0}' then proba_home else proba_away end as proba_club
      ,case when home_id = '{0}' then point_home else point_away end as point_club
      ,case when (home_id = '{0}' and home_goal > away_goal) or (away_id = '{$club_id}' and home_goal < away_goal) 
            then 1 
            else 0
        end as target
      ,match_dt
from "FOOTBET_elo_rank"
where home_id = '{0}' or away_id = '{0}' 
order by match_dt""".format(club_id)


