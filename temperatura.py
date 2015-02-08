# -*- coding: utf-8 -*-
"""
Created on Mon Nov  3 22:56:27 2014

@author: luis
"""

# -*- coding: utf-8 -*-


import visual as vs
import numpy as np

L = float(raw_input('Introduce la dimensión del cubo: '))
r = L/50
n = int(raw_input('Introduce el número de partículas: '))
T = float(raw_input('Introduce la temperatura del recipiente en grados Kelvin: '))

while T<0:
    print 'En escala Kelvin no existen temperaturas negativas.'
    T = float(raw_input('Introduce la temperatura del recipiente en grados Kelvin: '))


v = np.sqrt(T) # Faltan constantes

# Creación de los elementos a interaccionar entre sí

cubo = vs.box(pos=(0,0,0),length=2*L,height=2*L,width=2*L,color=(0,1,0),opacity=0.2)

bolas = []

for i in range(n):
    
    # Posición inicial
    
    pos = (np.random.random()*L/2,np.random.random()*L/2,np.random.random()*L/2)
    
    # Velocidad inicial
    
    theta = np.random.random()*2*np.pi
    phi = np.random.random()*2*np.pi
    
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
    
def choque_elastico2(bola1,bola2):

  # Velocidad en el sistema del centro de masas antes del choque

    v_1 = bola1.v - velocidad_centro(bola1,bola2)
    v_2 = bola2.v - velocidad_centro(bola1,bola2)    


  # Velocidad en el sistema del centro de masas después del choque

    v_1 *= -1
    v_2 *= -1
    
    bola1.v = v_1  + velocidad_centro(bola1,bola2)
    bola2.v = v_2 + velocidad_centro(bola1,bola2)
    
    
    
def choque_elastico(bola1,bola2):

    
        # Parámetros dejados al azar
    
        phi_1 = np.random.random()*2*np.pi
        theta_1 = np.random.random()*2*np.pi
        
        phi_2 = np.random.random()*2*np.pi
        theta_2 = np.random.random()*2*np.pi
        
        # Velocidades de las bolas antes del choque
        
        v_1 = np.sqrt(bola1.v[0]**2+bola1.v[1]**2+bola1.v[2]**2)
        v_2 = np.sqrt(bola2.v[0]**2+bola2.v[1]**2+bola2.v[2]**2)
        
        # Dirección de las velocidades después del choque        
        
        v_1x = v_1*np.sin(theta_1)*np.cos(phi_1)   
        v_1y = v_1*np.sin(theta_1)*np.sin(phi_1)
        v_1z = v_1*np.cos(theta_1)
        
        v_2x = v_2*np.sin(theta_2)*np.cos(phi_2)   
        v_2y = v_2*np.sin(theta_2)*np.sin(phi_2)
        v_2z = v_2*np.cos(theta_2)
        
        bola1.v = [v_1x,v_1y,v_1z]
        bola2.v = [v_2x,v_2y,v_2z]



# Mainloop

while 1:
    
    
    
    vs.rate(20)
    
    # Choque entre una bola  y la pared
    
    for i in range(n):

      if abs(bolas[i].x)+r>L:
          if bolas[i].x>0:
              bolas[i].x = L-r
          else:
              bolas[i].x = -L+r
              

      if abs(bolas[i].y)+r>L:
          if bolas[i].y>0:
              bolas[i].y = L-r
          else:
              bolas[i].y = -L+r
              
        
      if abs(bolas[i].z)+r>L:
          if bolas[i].z>0:
              bolas[i].z = L-r
          else:
              bolas[i].z = -L+r
               
          
      if abs(bolas[i].x)+r==L:
          bolas[i].v[0]*=-1
    
      if abs(bolas[i].y)+r==L:
          bolas[i].v[1]*=-1
          
      if abs(bolas[i].z)+r==L:
          bolas[i].v[2]*=-1
          
    
    # Choque entre dos bolas
    
    for i in range(n):
        for j in range(n):
            
          if i!=j:  
            
            distancia_centros = np.sqrt((bolas[i].x-bolas[j].x)**2 + (bolas[i].y-bolas[j].y)**2 + (bolas[i].z-bolas[j].z)**2)
          
            if distancia_centros<=(bolas[i].radius+bolas[j].radius):
               choque_elastico2(bolas[i],bolas[j])
       
    # Actualizar parámetros   
    
    for i in range(n):
        bolas[i].pos += (bolas[i].v[0]/5,bolas[i].v[1]/5,bolas[i].v[2]/5)
    
    