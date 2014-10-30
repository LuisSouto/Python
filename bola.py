# -*- coding: utf-8 -*-


import visual as vs
import numpy as np

L = float(raw_input('Introduce la dimensión del cubo: '))
r = float(raw_input('Introduce el radio de la bola: '))
v_o = float(raw_input('Introduce la velocidad inicial: '))
phi = float(raw_input('Introduce el ángulo azimutal inicual: '))
theta = float(raw_input('Introduce el ángulo cenital inicial: '))

while r>L:
   print 'La bola no puede ser mayor que el contorno en el que está encerrada.'
   r = float(raw_input('Introduce el radio de la bola: '))


cubo = vs.box(pos=(0,0,0),length=2*L,height=2*L,width=2*L,color=(0,1,0),opacity=0.2)
bola = vs.sphere(pos=(0,0,0),radius=r,color=(0,0,1))


v_x = v_o*np.sin(theta)*np.cos(phi)
v_y = v_o*np.sin(theta)*np.sin(phi)
v_z = v_o*np.cos(theta)

while 1:
    
    vs.rate(10)
    
    if abs(bola.x)+r>=L:
        v_x*=-1

    if abs(bola.y)+r>=L:
        v_y*=-1
        
    if abs(bola.z)+r>=L:
        v_z*=-1    
        
    bola.pos += v_x,v_y,v_z   