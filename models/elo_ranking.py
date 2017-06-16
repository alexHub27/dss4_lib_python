import numpy as np


class Club(object):
    def __init__(self,club_id,rank=1000,scored=0):
        self.club_id = club_id
        self.rank = rank
        self.scored = scored
        self.new_rank = 0
        self.perf = 0
        
    
class Game(object):
    def __init__(self,match_id,level,clubH,clubA,scH,scA):
        self.match_id = match_id
        self.level = level
        self.clubH = clubH
        self.clubH.scored = scH
        self.clubA = clubA
        self.clubA.scored = scA
        self.proba = 0
        self.home_k = 15
        self.away_k = 15
        self.avg = self.clubH.scored - self.clubA.scored
        self.H = 0
        self.A = 0
        self.pointH = 0
        self.pointA = 0
        self.probaH = 0
        self.probaA = 0
        
    def get_res_game(self):
        if self.clubH.scored > self.clubA.scored:
            self.clubH.perf = 1
            self.clubA.perf = 0
        elif self.clubH.scored == self.clubA.scored:
            self.clubH.perf = 0.5
            self.clubA.perf = 0.5
        else:
            self.clubH.perf = 0
            self.clubA.perf = 1 
        return 1
    
    def get_proba(self):
        self.probaH = 1.0/(1+np.power(10,(self.clubA.rank - (self.clubH.rank))/400.0))  
        self.probaA = 1.0 - self.probaH
        return 1
    
    def get_point(self):
        self.get_proba()

        self.pointH = self.level * self.fct() *(self.clubH.perf - self.probaH) #self.H
        self.pointA = self.level * self.fct() *(self.clubA.perf - self.probaA) #self.A
        return 1
    
    def fct(self):
        """ Weighting the result so that the defeat is not lienar (8-0 or 6-0 is roughly the same : you got destroyed) """
        if self.avg==0 or np.abs(self.avg) == 1:
            return 1
        elif np.abs(self.avg) == 2:
            return 3/2.0
        else :
            return (11+np.abs(self.avg))/8.0