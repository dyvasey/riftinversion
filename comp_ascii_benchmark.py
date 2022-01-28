#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Benchmark to ensure consistent generation of randomized plastic strain fields
"""
import matplotlib.pyplot as plt
import numpy as np
import ripropagate

params_400_100 = ripropagate.comp_ascii(y=400,seed=25,thicknesses=[20,20,60],plot=False)

params_400_120 = ripropagate.comp_ascii(y=400,seed=25,thicknesses=[20,20,80],plot=False)

params_600_100 = ripropagate.comp_ascii(y=600,seed=25,thicknesses=[20,20,60],plot=False)

fig,axs = plt.subplots(3,dpi=300,sharex=True)

grids = [params_400_100,params_400_120,params_600_100]

liths = [100,120,100]
depths = [400,400,600]

for k,ax in enumerate(axs):
    
    params = grids[k]
    xx = params[0]
    yy = params[1]
    ep = params[2]
    
    xmin = xx.min() + 350e3
    xmax = xx.max() - 350e3
    ymin = yy.max() - 80e3
    ymax = yy.max()
    
    ax.set_aspect('equal')
    ax.set_xlim(xmin/1.e3,xmax/1.e3)
    ax.set_ylim(ymin/1.e3,ymax/1.e3)
    ax.set_xlabel('Horizontal Position (km)')
    ax.set_ylabel('Height (km)')
    ctf = ax.contourf(xx[:,:]/1.e3,yy[:,:]/1.e3,ep[:,:],vmin=0.8)
    
    ax.set_title('Lith Thick: ' + str(liths[k]) + '  Depth: ' + str(depths[k]))

plt.tight_layout()

fig.savefig('strain_seeding_benchmark.jpg')
