import dataiku as dk 

def footbet_lstm_attack_form_test(club_id,match_dt,dataNm):
    return """ select home_flag,club_defence_skills,adv_attack_skills
      ,case when lag(target) over(partition by club_id,compet_id order by match_day) is null
            then 0 
            else lag(target) over(partition by club_id,compet_id order by match_day)
        end as prev_scored
from
(select club_id,compet_id,match_dt,home_flag,club_defence_skills,adv_attack_skills
      ,case when club_goal_against = 0 then 0
            when club_goal_against = 1 then 1
            when (club_goal_against = 2 or club_goal_against = 3) then 2
            else 3
        end as target
from
(select case when home_id = '{0}' then home_id else away_id end as club_id 
      ,case when home_id = '{0}' then 1 else 0 end as home_flag
      ,case when home_id = '{0}' then home_defence_skills else away_defence_skills end as club_defence_skills
      ,case when home_id = '{0}' then away_attack_skills else home_attack_skills end as adv_attack_skills
      ,case when home_id = '{0}' then away_goal else home_goal end as club_goal_against
      ,compet_id,match_day,match_dt
      ,row_number() over(order by match_dt) as rk 
from (select compet_id,match_dt,match_day,home_id,away_id
            ,case when home_attack_skills is null then 0 else home_attack_skills end as home_attack_skills
            ,case when away_attack_skills is null then 0 else away_attack_skills end as away_attack_skills
            ,case when home_defence_skills is null then 0 else home_defence_skills end as home_defence_skills
            ,case when away_defence_skills is null then 0 else away_defence_skills end as away_defence_skills
            
            ,case when home_goal is null then 0 else home_goal end as home_goal
            ,case when away_goal is null then 0 else away_goal end as away_goal 
            
            from "FOOTBET_{}")tmp
where home_id = '{0}'  and m2atch_dt <= '{1}')tmp
where rk < '${wG}')tmp
order by compet_id,match_day
""".format(club_id,match_dt,dataNm)
        
def footbet_lstm_goal_defence_test(club_id,dataNm):
    return """select home_flag,club_defence_skills,adv_attack_skills
      ,case when lag(target) over(partition by club_id,compet_id order by match_day) is null
            then 0 
            else lag(target) over(partition by club_id,compet_id order by match_day)
        end as prev
      ,target
from
(select club_id,compet_id,match_day,home_flag,club_defence_skills,adv_attack_skills
      ,case when club_goal_against = 0 then 0
            when club_goal_against = 1 then 1
            when (club_goal_against = 2 or club_goal_against = 3) then 2
            else 3
        end as target
from
(select case when home_id = '{0}' then home_id else away_id end as club_id 
      ,case when home_id = '{0}' then 1 else 0 end as home_flag
      ,case when home_id = '{0}' then home_defence_skills else away_defence_skills end as club_defence_skills
      ,case when home_id = '{0}' then away_attack_skills else home_attack_skills end as adv_attack_skills
      ,case when home_id = '{0}' then away_goal else home_goal end as club_goal_against
      ,compet_id,match_day
from (select compet_id,match_day,home_id,away_id
            ,case when home_attack_skills is null then 0 else home_attack_skills end as home_attack_skills
            ,case when away_attack_skills is null then 0 else away_attack_skills end as away_attack_skills
            ,case when home_defence_skills is null then 0 else home_defence_skills end as home_defence_skills
            ,case when away_defence_skills is null then 0 else away_defence_skills end as away_defence_skills
            
            ,case when home_goal is null then 0 else home_goal end as home_goal
            ,case when away_goal is null then 0 else away_goal end as away_goal 
            from "FOOTBET_{1}")tmp
where home_id = '{0}' or away_id = '{0}')tmp)tmp
order by compet_id,match_day""".format(club_id,dataNm)

def footbet_lstm_goal_attack_test(club_id,dataNm):
    return """select home_flag,club_attack_skills,adv_defence_skills
      ,case when lag(target) over(partition by club_id,compet_id order by match_day) is null
            then 0 
            else lag(target) over(partition by club_id,compet_id order by match_day)
        end as prev
      ,target
from
(select club_id,compet_id,match_day,home_flag,club_attack_skills,adv_defence_skills
      ,case when club_goals =0  then 0
            when club_goals = 1 then 1
            when (club_goals = 2 or club_goals = 3) then 2
            else 3
        end as target
from
(select case when home_id = '{0}' then home_id else away_id end as club_id 
      ,case when home_id = '{0}' then 1 else 0 end as home_flag
      ,case when home_id = '{0}' then home_attack_skills else away_attack_skills end as club_attack_skills
      ,case when home_id = '{0}' then away_defence_skills else home_defence_skills end as adv_defence_skills
      ,case when home_id = '{0}' then home_goal else away_goal end as club_goals
      ,compet_id,match_day
from (select compet_id,match_day,home_id,away_id
            ,case when home_attack_skills is null then 0 else home_attack_skills end as home_attack_skills
            ,case when away_attack_skills is null then 0 else away_attack_skills end as away_attack_skills
            ,case when home_defence_skills is null then 0 else home_defence_skills end as home_defence_skills
            ,case when away_defence_skills is null then 0 else away_defence_skills end as away_defence_skills
            
            ,case when home_goal is null then 0 else home_goal end as home_goal
            ,case when away_goal is null then 0 else away_goal end as away_goal 
            from "FOOTBET_{1}")tmp
where home_id = '{0}' or away_id = '{0}')tmp)tmp
order by compet_id,match_day""".format(club_id,dataNm)

def footbet_lstm_elo_global_test(club_id,dataNm):
    return """select
       case when l.home_id = '{0}' 
            then 1
            else 0 
            end as flag_home 
      ,case when l.home_id = '{0}'
            then (cast(l.home_rank as numeric) -1000)/60
            else (cast(l.away_rank as numeric) -1000)/60
            end as rank_club
      ,case when l.home_id = '{0}'
            then (cast(l.away_rank as numeric) -1000)/60
            else (cast(l.home_rank as numeric) -1000)/60
            end as rank_adv
      ,case when l.home_id = '{0}' 
            then l.proba_home 
            else l.proba_away 
            end as proba_club
      ,case when l.home_id = '{0}' 
            then l.point_home 
            else l.point_away 
            end as point_club

      ,case when (l.home_id = '{0}' and l.home_goal>l.away_goal) or (l.away_id = '{0}' and l.home_goal<=l.away_goal) then 1
            else 0 end as target

from "FOOTBET_{1}" l
/*inner join "FOOTBET_foot_games_flat" r
on cast(l.match_id as text) = cast(r.match_id as text)*/
where l.home_id = '{0}' or l.away_id = '{0}' 
order by l.match_dt""".format(club_id,dataNm)

def footbet_lstm_elo_global(club_id,dataNm):
    return """select
       case when l.home_id = '{0}' 
            then 1
            else 0 
            end as flag_home 
      ,case when l.home_id = '{0}'
            then (cast(l.home_rank as numeric) -1000)/60
            else (cast(l.away_rank as numeric) -1000)/60
            end as rank_club
      ,case when l.home_id = '{0}'
            then (cast(l.away_rank as numeric) -1000)/60
            else (cast(l.home_rank as numeric) -1000)/60
            end as rank_adv
      ,case when l.home_id = '{0}' 
            then l.proba_home 
            else l.proba_away 
            end as proba_club
      ,case when l.home_id = '{0}' 
            then l.point_home 
            else l.point_away 
            end as point_club

      ,case when (l.home_id = '{0}' and l.home_goal>l.away_goal) or (l.away_id = '{0}' and l.home_goal<=l.away_goal) then 1
            else 0 end as target

from "FOOTBET_{1}" l
where home_id = '{0}' or away_id = '{0}'
order by match_dt""".format(club_id,dataNm)

def footbet_lstm_elo_form_global(club_id,match_dt,w,dataNm='elo_rank_club_test'):
    """ Supposed to be used as a batch generator for Model pre trained. Those models will then give features we will use in another
        concatenated Dense model."""
    return """ select home_flag,rank_club,rank_adv,proba_club,case when rk = 1 then 0 else cast(point_club as numeric) end as point_club
from
(select case when home_id = '{0}' then 1 else 0 end as home_flag
      ,case when home_id = '{0}'
            then (cast(home_rank as numeric) -1000)/60
            else (cast(away_rank as numeric) -1000)/60
            end as rank_club
      ,case when home_id = '{0}'
            then (cast(away_rank as numeric) -1000)/60
            else (cast(home_rank as numeric) -1000)/60
            end as rank_adv
      ,case when home_id = '{0}' then proba_home else proba_away end as proba_club
      ,case when home_id = '{0}' then point_home else point_away end as point_club
      ,row_number() over(order by match_dt desc) as rk
      ,match_dt
from "FOOTBET_{3}"
where (home_id = '{0}' or away_id = '{0}') and match_dt <= '{1}') tmp
where rk <= {2}
order by match_dt
""".format(club_id,match_dt,w,dataNm)

def footbet_lstm_elo_flag(home_flag,club_id,dataNm):
    return """ select 
         case when '{1}'='home_id' then (cast(home_rank as numeric)-1000)/60
              else (cast(away_rank as numeric)-1000)/60
              end as rank_club
        ,case when '{1}'='home_id' then (cast(away_rank as numeric)-1000)/60
              else (cast(home_rank as numeric)-1000)/60
              end as rank_adv
        ,proba_home,point_home
        ,case when ('{1}'='home_id' and home_goal > away_goal) or ('{1}'='away_id' and home_goal <= away_goal) 
              then 1 
              else 0 
              end as target
        from "FOOTBET_{2}"
        where {1} = '{0}' 
        order by match_dt""".format(club_id,home_flag,dataNm)

def footbet_lstm_elo_form_flag(home_flag,club_id,match_dt,w,dataNm='elo_rank_club_test'):
    """ Supposed to be used as a batch generator for Model pre trained. Those models will then give features we will use in another
        concatenated Dense model."""
    return """ select rank_club,rank_adv,proba_club,case when rk = 1 then 0 else cast(point_club as numeric) end as point_club
from
(select 
       case when '{1}'='home_id' then (cast(home_rank as numeric)-1000)/60
            else (cast(away_rank as numeric)-1000)/60
            end as rank_club
      ,case when '{1}'='home_id' then (cast(away_rank as numeric)-1000)/60
            else (cast(home_rank as numeric)-1000)/60
            end as rank_adv
      ,proba_home as proba_club
      ,point_home as point_club
      ,row_number() over(order by match_dt desc) as rk
      ,match_dt
from "FOOTBET_{4}"
where {0} = '{1}' and match_dt <= '{2}') tmp
where rk <= {3}
order by match_dt
""".format(home_flag,club_id,match_dt,w,dataNm)

########################


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




