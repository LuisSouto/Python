# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 18:13:48 2015

@author: luis
"""
import random as rd
import visual as vs
import numpy as np
from scipy.stats import maxwell
import constantes_fisicas as cf

class Gas_Ideal(object):
    def __init__(self,L,n,T):
        self.L = L
        self.n = n
        self.T = T
        self.r = L*0.01
        self.contenedor()
        self.bolas = Gas_Ideal.crear_bolas(self)

    def contenedor(self):
        cubo = vs.box(pos=(0,0,0),length=self.L,height=self.L,width=self.L,color=(1,1,1),opacity=0.2)
        
    def crear_bolas(self):        
        m = 12*cf.u
        escala = np.sqrt(cf.k_B*self.T/m)
        bolas = []
        v = []
        for i in range(self.n):
    
          # Posición inicial
    
          pos = (rd.uniform(-1,1)*self.L/2,rd.uniform(-1,1)*self.L/2,rd.uniform(-1,1)*self.L/2)
    
          # Velocidad inicial
    
          cos_theta = rd.uniform(-1,1)
          phi = rd.uniform(0,2*np.pi)
          theta = np.arccos(cos_theta)
    
          x = maxwell.rvs(scale=escala)
          v = x*cf.m/cf.ms
          v_x = v*np.sin(theta)*np.cos(phi)
          v_y = v*np.sin(theta)*np.sin(phi)
          v_z = v*np.cos(theta)    
    
          bola = vs.sphere(pos=np.array(pos),radius=self.r,color=(0,0,1),v=np.array([v_x,v_y,v_z]))
    
          bolas.append(bola)
        return bolas
          
    def centro_de_masas(bola1,bola2):
        return 0.5*np.array([bola1.pos[0]+bola2.pos[0],bola1.pos[1]+bola2.pos[1],bola1.pos[2]+bola2.pos[2]]) 
          
    def velocidad_centro(self,bola1,bola2):
        return 0.5*np.array([bola1.v[0]+bola2.v[0],bola1.v[1]+bola2.v[1],bola1.v[2]+bola2.v[2]])      
          
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
        for i in range(self.n):
          if abs(self.bolas[i].x)+self.r>=self.L/2.:
            self.bolas[i].v[0]*=-1
          if abs(self.bolas[i].y)+self.r>=self.L/2.:
            self.bolas[i].v[1]*=-1
          if abs(self.bolas[i].z)+self.r>=self.L/2.:
            self.bolas[i].v[2]*=-1
           
    def update(self):
        for i in range(self.n):        
          x,y,z = self.bolas[i].pos
          vx,vy,vz = self.bolas[i].v
          if abs(x+vx)+self.r>self.L/2.:
            if x>0:
              self.bolas[i].x = self.L/2.-self.r
            else:
              self.bolas[i].x = self.r-self.L/2.
          else:
              self.bolas[i].x = x+vx
            
          if abs(y+vy)+self.r>self.L/2.:
              if y>0:
                self.bolas[i].y = self.L/2.-self.r
              else:
                self.bolas[i].y = self.r-self.L/2.
          else:
              self.bolas[i].y = y+vy
            
          if abs(z+vz)+self.r>self.L/2.:
              if z>0:
                self.bolas[i].z = self.L/2.-self.r
              else:
                self.bolas[i].z = self.r-self.L/2.
          else:
              self.bolas[i].z = z+vz  
              
    def analiza_choque_bolas(self):
        for i in range(gas_ideal.n):
          for j in range(gas_ideal.n):    
            if i!=j:      
              distancia_centros = np.sqrt((gas_ideal.bolas[i].x-gas_ideal.bolas[j].x)**2 + (gas_ideal.bolas[i].y-gas_ideal.bolas[j].y)**2 + (gas_ideal.bolas[i].z-gas_ideal.bolas[j].z)**2)      
              if distancia_centros<=(gas_ideal.bolas[i].radius+gas_ideal.bolas[j].radius):
                gas_ideal.choque_elastico(gas_ideal.bolas[i],gas_ideal.bolas[j])

gas_ideal = Gas_Ideal(10,30,100)              

# Mainloop


while 1:
    
    vs.rate(20)
    
    # Choque entre una bola  y la pared
    gas_ideal.choque_pared()
          
    # Choque entre dos bolas
    gas_ideal.analiza_choque_bolas()
       
    # Actualizar parámetro
    gas_ideal.update()   