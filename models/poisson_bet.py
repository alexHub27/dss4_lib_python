import numpy as np 

def poiss_team(skills,nb_goals):
    if skills:
        return np.power(skills,nb_goals)*np.exp(-skills)/np.math.factorial(nb_goals)
    else:
        return None

def prob_draw(skills_h,skills_a):
    if skills_h and skills_a:
        return sum([poiss_team(skills_h,i)*poiss_team(skills_a,i) for i in range(10)])
    else:
        return None

def prob_home_win(skills_h,skills_a):
    pr = []
    if skills_h and skills_a:
        for scH in range(1,10):
            for scA in range(scH):
                pr.append(poiss_team(skills_h,scH)*poiss_team(skills_a,scA))
        return np.sum(pr)
    else:
        return None

def prob_away_win(skills_h,skills_a):
    if skills_h and skilss_a:
        return 1-prob_draw(skills_h,skills_a) - prob_home_win(skills_h,skills_a)
    else:
        return None

def prob_less(skills_h,skills_a,n=3):
    pr = []
    if skills_h and skills_a:
        for scH in range(n):
            for scA in range(n - scH):
                pr.append(poiss_team(skills_h,scH)*poiss_team(skills_a,scA))
        return np.sum(pr)
    else:
        return None    
    