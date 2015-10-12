# -*- coding: utf-8 -*-
"""
Created on Mon Nov  3 22:56:27 2014

@author: luis
"""

# -*- coding: utf-8 -*-



import visual as vs
import numpy as np
import random as rd
from scipy.stats import maxwell
import constantes_fisicas as cf


L = float(raw_input('Introduce la dimensión del cubo: '))
r = L/100
n = int(raw_input('Introduce el número de partículas: '))
T = float(raw_input('Introduce la temperatura del recipiente en grados Kelvin: '))*cf.K
m = 12*cf.u
escala = 100*np.sqrt(m/(cf.k_B*T))

while T<0:
    print 'En escala Kelvin no existen temperaturas negativas.'
    T = float(raw_input('Introduce la temperatura del recipiente en grados Kelvin: '))



# Creación de los elementos a interaccionar entre sí

cubo = vs.box(pos=(0,0,0),length=2*L,height=2*L,width=2*L,color=(1,1,1),opacity=0.2)

bolas = []
v = []

for i in range(n):
    
    # Posición inicial
    
    pos = (rd.uniform(-1,1)*L/2,rd.uniform(-1,1)*L/2,rd.uniform(-1,1)*L/2)
    
    # Velocidad inicial
    
    cos_theta = rd.uniform(-1,1)
    phi = rd.uniform(0,2*np.pi)
    theta = np.arccos(cos_theta)
    
    f_inv_cdf = rd.uniform(0,1)
    x = maxwell.ppf(f_inv_cdf)
    v = x/escala
    
    v_x = v*np.sin(theta)*np.cos(phi)
    v_y = v*np.sin(theta)*np.sin(phi)
    v_z = v*np.cos(theta)    
    
    bola = vs.sphere(pos=np.array(pos),radius=r,color=(0,0,1),v=np.array([v_x,v_y,v_z]))
    
    bolas.append(bola)
    


# Funciones a utilizar

def centro_de_masas(bola1,bola2):
    
    # Coordenada x
     
     x = (bola1.pos[0]+bola2.pos[0])/2
     
    # Coordenada y
     
     y = (bola1.pos[1]+bola2.pos[1])/2     
     
    # Coordenada z
     
     z = (bola1.pos[2]+bola2.pos[2])/2     
     
     return np.array([x,y,z])


def velocidad_centro(bola1,bola2):
    
    # Componente x
    
     v_x = (bola1.v[0]+bola2.v[0])/2
     
    # Componente y
    
     v_y = (bola1.v[1]+bola2.v[1])/2  
     
    # Componente z
    
     v_z = (bola1.v[2]+bola2.v[2])/2 
     
     return np.array([v_x,v_y,v_z])
    
def choque_elastico(bola1,bola2):

  # Velocidad en el sistema del centro de masas antes del choque

    v_c = velocidad_centro(bola1,bola2)
    v_1 = bola1.v - v_c
    v_2 = bola2.v - v_c


  # Velocidad en el sistema del centro de masas después del choque

    v_1 *= -1
    v_2 *= -1
    
    bola1.v = v_1  + v_c
    bola2.v = v_2 + v_c

    


# Mainloop

while 1:
    
    
    
    vs.rate(20)
    
    # Choque entre una bola  y la pared
    
    for i in range(n):
          
      if abs(bolas[i].x)+r>=L:
          bolas[i].v[0]*=-1
    
      if abs(bolas[i].y)+r>=L:
          bolas[i].v[1]*=-1
          
      if abs(bolas[i].z)+r>=L:
          bolas[i].v[2]*=-1
          
    
    # Choque entre dos bolas
    
    for i in range(n):
        for j in range(n):
            
          if i!=j:  
            
            distancia_centros = np.sqrt((bolas[i].x-bolas[j].x)**2 + (bolas[i].y-bolas[j].y)**2 + (bolas[i].z-bolas[j].z)**2)
          
            if distancia_centros<=(bolas[i].radius+bolas[j].radius):
               choque_elastico(bolas[i],bolas[j])
       
    # Actualizar parámetros   
    
    for i in range(n):
        
        x,y,z = bolas[i].pos
        vx,vy,vz = bolas[i].v
        
        if abs(x+vx)+r>L:
            if x>0:
                bolas[i].x = L-r
            else:
                bolas[i].x = r-L
        else:
            bolas[i].x = x+vx
            
        if abs(y+vy)+r>L:
            if y>0:
                bolas[i].y = L-r
            else:
                bolas[i].y = r-L
        else:
            bolas[i].y = y+vy
            
        if abs(z+vz)+r>L:
            if z>0:
                bolas[i].z = L-r
            else:
                bolas[i].z = r-L
        else:
            bolas[i].z = z+vz    
    
    