# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 14:00:33 2015

@author: luis
"""
from gas_ideal import Gas_Ideal
from Physics import Units
import visual as vs
import numpy as np

L = 10*Units.nm
n = 50
T = 100

class Gas_Ideal_P(Gas_Ideal):
    def __init__(self,L,n,T,contenedor,m=12*Units.amu):
        super(Gas_Ideal_P,self).__init__(L,n,T,contenedor)
        self.m_wall = self.m*5000
        self.x = 0
        
    def choque_pared(self):
        P = 0*Units.Pa
        self.x = 0
        for i in range(self.n_graph):  
          if np.mod(i,10)==0:
            j = i/10
            if abs(self.bolas_visual[j].x-self.cubo.pos[0])+self.r>=self.cubo.length/2.:
              self.bolas_visual[j].v[0]*=-1
            if abs(self.bolas_visual[j].y)+self.r>=self.cubo.width/2.:
              self.bolas_visual[j].v[1]*=-1
            if abs(self.bolas_visual[j].z)+self.r>=self.cubo.height/2.:
              self.bolas_visual[j].v[2]*=-1    
          if abs(self.bolas_grafica[i].x-self.cubo.pos[0])+self.r>=self.cubo.length/2.:
            self.bolas_grafica[i].v[0]*=-1
            self.x+=abs(self.bolas_grafica[i].p[0])*self.dt/self.m_wall
            P+= abs(self.bolas_grafica[i].p[0])/(self.cubo.width*self.cubo.height*self.dt)*Units.Pa
          if abs(self.bolas_grafica[i].y)+self.r>=self.cubo.width/2.:
            self.bolas_grafica[i].v[1]*=-1
            P+= abs(self.bolas_grafica[i].p[1])/(self.cubo.length*self.cubo.height*self.dt)*Units.Pa
          if abs(self.bolas_grafica[i].z)+self.r>=self.cubo.height/2.:
            self.bolas_grafica[i].v[2]*=-1
            P+= abs(self.bolas_grafica[i].p[2])/(self.cubo.length*self.cubo.width*self.dt)*Units.Pa
        self.P.append(P/3) 
        
    def move_wall(self,x):
        self.cubo.length+=x
        self.cubo.pos[0]+=x/2
    
    def update(self):
        super(Gas_Ideal_P,self).update()
        self.move_wall(self.x)  
              
    def update_balls_position(self):
        self.counter+=1
        self.t+=self.dt
        for i in range(self.n_graph):        
          x,y,z = self.bolas_grafica[i].x,self.bolas_grafica[i].y,self.bolas_grafica[i].z
          vx,vy,vz = self.bolas_grafica[i].v
          if abs(x+vx*self.dt-self.cubo.pos[0])+self.r>self.cubo.length/2.:
            if x-self.cubo.pos[0]>0:
              self.bolas_grafica[i].x = self.cubo.length/2.-self.r+self.cubo.pos[0]
            else:
              self.bolas_grafica[i].x = self.r-self.cubo.length/2.+self.cubo.pos[0]
          else:
              self.bolas_grafica[i].x = x+vx*self.dt
            
          if abs(y+vy*self.dt)+self.r>self.cubo.height/2.:
              if y>0:
                self.bolas_grafica[i].y = self.cubo.height/2.-self.r
              else:
                self.bolas_grafica[i].y = self.r-self.cubo.height/2.
          else:
              self.bolas_grafica[i].y = y+vy*self.dt
          
          if abs(z+vz*self.dt)+self.r>self.cubo.width/2.:
              if z>0:
                self.bolas_grafica[i].z = self.cubo.width/2.-self.r
              else:
                self.bolas_grafica[i].z = self.r-self.cubo.width/2.
          else:
              self.bolas_grafica[i].z = z+vz*self.dt  
          if np.mod(i,self.n_graph/self.n_vis)==0:
              j = i/10
              if abs(x+vx*self.dt-self.cubo.pos[0])+self.r>self.cubo.length/2.:
                if x-self.cubo.pos[0]>0:
                  self.bolas_visual[j].x = self.cubo.length/2.-self.r+self.cubo.pos[0]
                else:
                  self.bolas_visual[j].x = self.r-self.cubo.length/2.+self.cubo.pos[0]
              else:
                self.bolas_visual[j].x = x+vx*self.dt
          
              if abs(y+vy*self.dt)+self.r>self.cubo.height/2.:
                if y>0:
                  self.bolas_visual[j].y = self.cubo.height/2.-self.r
                else:
                  self.bolas_visual[j].y = self.r-self.cubo.height/2.
              else:
                self.bolas_visual[j].y = y+vy*self.dt
           
              if abs(z+vz*self.dt)+self.r>self.cubo.width/2.:
                if z>0:
                  self.bolas_visual[j].z = self.cubo.width/2.-self.r
                else:
                  self.bolas_visual[j].z = self.r-self.cubo.width/2.
              else:
                self.bolas_visual[j].z = z+vz*self.dt
                
                
        
 
if __name__=='__main__':
    
  box1 = vs.box(pos=(0,0,0),length=0.5*L,height=L,width=L,color=(1,0,0),opacity=0.2)
  gas1 = Gas_Ideal_P(L,n,T,box1)

  while 1:
    vs.rate(30)
    
    gas1.update()

