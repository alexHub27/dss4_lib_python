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