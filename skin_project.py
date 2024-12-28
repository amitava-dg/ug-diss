#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 20:38:14 2024

@author: Amitava Dasgupta
"""

import meep as mp
import numpy as np
import matplotlib.pyplot as plt

cell = mp.Vector3(12,12,0.0)

geometry = [mp.Block(mp.Vector3(mp.inf,7.5,mp.inf),
                     center = mp.Vector3(0.0,-2.25),
                     material = mp.Medium(epsilon=1.0,index=1.0)),
            mp.Block(mp.Vector3(mp.inf,0.2,mp.inf),
                     center = mp.Vector3(0.0,1.6),
                     material = mp.Medium(epsilon=36.11,index=6.4)),
            mp.Block(mp.Vector3(mp.inf,3.3,mp.inf),
                     center = mp.Vector3(0.0,3.35),
                     material = mp.Medium(epsilon=4.21,index=2.5)),
            mp.Block(mp.Vector3(mp.inf,1.0,mp.inf),
                     center = mp.Vector3(0.0,5.5),
                     material = mp.Medium(epsilon=52.77,index=8.9))]

sources = [mp.Source(mp.ContinuousSource(frequency=0.068),
                     component=mp.Ez,
                     center=mp.Vector3(0.0,0.065))]

pml_layers = [mp.PML(1.0)]

resolution = 100

sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

sim.run(mp.at_beginning(mp.output_epsilon),
        mp.to_appended("ez", mp.at_every(0.1, mp.output_efield_z)),
        until=100)


ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
ez_data=np.square(ez_data)
plt.figure(figsize=(10,10))
plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='jet', alpha=1.0)
plt.show()

for i in range (1200):
    if(i<=740):
        ez_data[i,600]=ez_data[i,600]*1e-14*0.5/1.3
    elif(i<=760):
        ez_data[i,600]=ez_data[i,600]*6.61*0.5/1118.0
    else:
        ez_data[i,600]=ez_data[i,600]*0.48*0.5/999.0

plt.figure(figsize=(10,10))
plt.plot(np.log10(ez_data[500:1000,600]))
plt.show()