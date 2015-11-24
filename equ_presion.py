# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 18:42:30 2015

@author: luis
"""

from piston_movil import Gas_Ideal_P
from Physics import Units
import visual as vs

L = 10*Units.nm
n = 30
T = 100

class Gas_Ideal_P2(Gas_Ideal_P):

      
    
    def move_wall(self,x):
        self.cubo.length+=x
        self.cubo.pos[0]-=x/2
        
        
def common_wall(gas1,gas2):
    gas1.move_wall(-gas2.x)
    gas2.move_wall(-gas1.x)
    
box1 = vs.box(pos=(0,0,0),length=0.1*L,height=L,width=L,color=(1,0,0),opacity=0.2)
gas1 = Gas_Ideal_P(L,n,T,box1)
box2 = vs.box(pos=(L/2,0,0),length=0.9*L,height=L,width=L,color=(0,0,1),opacity=0.2)
gas2 = Gas_Ideal_P2(L,n,T,box2)    


while 1:
    vs.rate(30)
    
    gas1.update()
    gas2.update()
    common_wall(gas1,gas2)        