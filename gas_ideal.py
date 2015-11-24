# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 18:13:48 2015

@author: luis
"""
import random as rd
import visual as vs
import visual.graph as vs_graph
import numpy as np
from scipy.stats import maxwell
from Physics import Constants
from Physics import Units


class Bola(object):

    def __init__(self,pos,v,m):
      self.x = pos[0]
      self.y = pos[1]
      self.z = pos[2]
      self.pos = self.calculate_pos()
      self.v = v
      self.m = m
      self.p = self.calculate_momentum()
      
    def calculate_momentum(self):
        return self.m*self.v

    def calculate_pos(self):
        return np.array([self.x,self.y,self.z])
        
class Gas_Ideal(object):
    
    def __init__(self,L,n,T,contenedor,m=12*Units.amu):
        self.L = L*Units.m
        self.n_vis = n
        self.n_graph = 10*n
        self.T = T*Units.K
        self.m = m*Units.kg
        self.r = self.L*0.01
        self.cubo = contenedor
        self.bolas_visual,self.bolas_grafica = self.crear_bolas()
        self.dt = 0.1*self.L*np.sqrt(np.pi*self.m/(8*Constants.kBJ*self.T))
        self.P = []
        self.t = 0
        self.counter = 0
        self.graph = vs_graph.gdots()
        self.p_ideal_graph = vs_graph.gcurve(color=vs_graph.color.blue)

    def crear_bolas(self): 
        
        escala = np.sqrt(Constants.kBJ*self.T/self.m)
        bolas_grafica = []
        bolas_visual = []
        v = []
        for i in range(self.n_graph):
          # Posición inicial
          pos = (rd.uniform(-1,1)*self.cubo.length/2+self.cubo.pos[0],rd.uniform(-1,1)*self.cubo.height/2+self.cubo.pos[1],rd.uniform(-1,1)*self.cubo.width/2+self.cubo.pos[2])
          # Velocidad inicial
          cos_theta = rd.uniform(-1,1)
          phi = rd.uniform(0,2*np.pi)
          theta = np.arccos(cos_theta)
    
          v = maxwell.rvs(scale=escala)*Units.m/Units.s
          v_x = v*np.sin(theta)*np.cos(phi)
          v_y = v*np.sin(theta)*np.sin(phi)
          v_z = v*np.cos(theta)
          bola_grafica = Bola(pos=np.array(pos),v=np.array([v_x,v_y,v_z]),m=self.m)
          bolas_grafica.append(bola_grafica)
          if np.mod(i,self.n_graph/self.n_vis)==0:     
            bola_visual = vs.sphere(pos=np.array(pos),radius=self.r,color=(0,1,0),v=np.array([v_x,v_y,v_z]))
            bolas_visual.append(bola_visual)
        return bolas_visual,bolas_grafica
          
    def centro_de_masas(bola1,bola2):
        return 0.5*np.array([bola1.pos[0]+bola2.pos[0],bola1.pos[1]+bola2.pos[1],bola1.pos[2]+bola2.pos[2]]) 
          
    def velocidad_centro(self,bola1,bola2):
        return 0.5*np.array([bola1.v[0]+bola2.v[0],bola1.v[1]+bola2.v[1],bola1.v[2]+bola2.v[2]])      
          
    def calculate_volume(self):
        return self.cubo.length*self.cubo.width*self.cubo.height
        
    def presion_ideal(self):
        return self.n_vis*Constants.kBJ*self.T/(self.calculate_volume())
          
    def choque_elastico(self,bola1,bola2):
      # Velocidad en el sistema del centro de masas antes del choque
        v_c = self.velocidad_centro(bola1,bola2)
        v_1 = bola1.v - v_c
        v_2 = bola2.v - v_c
        # Velocidad en el sistema del centro de masas después del choque
        v_1 *= -1
        v_2 *= -1
        bola1.v = v_1  + v_c
        bola2.v = v_2 + v_c   
          
    def choque_pared(self):
        P = 0*Units.Pa
        for i in range(self.n_graph):
          if abs(self.bolas_grafica[i].x)+self.r>=self.cubo.length/2.:
            self.bolas_grafica[i].v[0]*=-1
            P+= abs(self.bolas_grafica[i].p[0])/(self.cubo.width*self.cubo.height)
          if abs(self.bolas_grafica[i].y)+self.r>=self.cubo.height/2.:
            self.bolas_grafica[i].v[1]*=-1
            P+= abs(self.bolas_grafica[i].p[1])/(self.cubo.length*self.cubo.width)
          if abs(self.bolas_grafica[i].z)+self.r>=self.cubo.width/2.:
            self.bolas_grafica[i].v[2]*=-1
            P+= abs(self.bolas_grafica[i].p[2])/(self.cubo.length*self.cubo.height)
          if np.mod(i,10)==0:
              j = i/10
              if abs(self.bolas_visual[j].x)+self.r>=self.cubo.length/2.:
                self.bolas_visual[j].v[0]*=-1
              if abs(self.bolas_visual[j].y)+self.r>=self.cubo.height/2.:
                self.bolas_visual[j].v[1]*=-1
              if abs(self.bolas_visual[j].z)+self.r>=self.cubo.width/2.:
                self.bolas_visual[j].v[2]*=-1
        self.P.append(P/(3*self.dt))      
            
    def update_balls_position(self):
        self.counter+=1
        self.t+=self.dt
        for i in range(self.n_graph):        
          x,y,z = self.bolas_grafica[i].x,self.bolas_grafica[i].y,self.bolas_grafica[i].z
          vx,vy,vz = self.bolas_grafica[i].v
          if abs(x+vx*self.dt)+self.r>self.cubo.length/2.:
            if x>0:
              self.bolas_grafica[i].x = self.cubo.length/2.-self.r
            else:
              self.bolas_grafica[i].x = self.r-self.cubo.length/2.
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
              if abs(x+vx*self.dt)+self.r>self.cubo.length/2.:
                if x>0:
                  self.bolas_visual[j].x = self.cubo.length/2.-self.r
                else:
                  self.bolas_visual[j].x = self.r-self.cubo.length/2.
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
              
    def update_graph(self):     
      if np.mod(self.counter,10)==0:
        P = sum(self.P[self.counter-10:self.counter])/10
        self.graph.plot(pos=(self.t,P/10))     
        self.p_ideal_graph.plot(pos=(self.t,self.presion_ideal()))
        
    def analiza_choque_bolas(self):
        for i in range(self.n_graph):
          for j in range(self.n_graph):    
            if i!=j:      
              distancia_centros = np.sqrt((gas_ideal.bolas[i].x-gas_ideal.bolas[j].x)**2 + (gas_ideal.bolas[i].y-gas_ideal.bolas[j].y)**2 + (gas_ideal.bolas[i].z-gas_ideal.bolas[j].z)**2)      
              if distancia_centros<=(gas_ideal.bolas[i].radius+gas_ideal.bolas[j].radius):
                gas_ideal.choque_elastico(gas_ideal.bolas[i],gas_ideal.bolas[j]) 
                
    def update(self): 
      # Choque entre una bola  y la pared
      self.choque_pared()
      
      # Actualizar parámetro
      self.update_balls_position() 
      
      self.update_graph()
         
      

        

   


if __name__=='__main__':  
   
   L,n,T = 10*Units.nm,50,100
   contenedor = vs.box(pos=(0,0,0),length=7*L,width=2*L,height=5*L,color=(1,0,0),opacity=0.2)
   gas_ideal = Gas_Ideal(L,n,T,contenedor)   

   # Mainloop

   while 1:
    
    vs.rate(50)
    gas_ideal.update()   