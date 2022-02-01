#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Benchmark to ensure consistent generation of randomized plastic strain fields
"""
import matplotlib.pyplot as plt
import numpy as np
import ripropagate

seed=35
mantle_liths = [60,60,40,80]
depths = [400,600,400,1000]

grids = []
for k, lith in enumerate(mantle_liths):
    params = ripropagate.comp_ascii(depth=depths[k],seed=seed,thicknesses=[20,20,lith],plot=False)
    grids.append(params)

nplots = len(grids)

fig,axs = plt.subplots(nplots,dpi=300,sharex=True)

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
    #ax.set_xlabel('Horizontal Position (km)')
    #ax.set_ylabel('Height (km)')
    ctf = ax.contourf(xx[:,:]/1.e3,yy[:,:]/1.e3,ep[:,:],vmin=0.8)
    
    ax.set_title('Mantle Lith Thick: ' + str(mantle_liths[k]) + '  Depth: ' + str(depths[k]))

plt.tight_layout()

fig.savefig('strain_seeding_benchmark.jpg')
