"""
Compare two models from command line. Requires 4 arguments: directory1, time1, directory2, time2
timestep, and output image
"""
import sys
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pyvista as pv

from riftinversion import vtk_plot as vp

pv.start_xvfb()

directory1 = sys.argv[1]
time1 = float(sys.argv[2])

directory2 = sys.argv[3]
time2 = float(sys.argv[4])

model_step = float(sys.argv[5])

step1 = int(time1/model_step)
step2 = int(time2/model_step)

file1 = vp.get_pvtu(directory1,step1)
file2 = vp.get_pvtu(directory2,step2)

colors=['#99CCCC','#996633','#990000','#339966']
cm = ListedColormap(colors)

opaque_cm = 'inferno_r'
opaque_cm_rev = 'inferno'

lim_strain = [0,5]

lim_strainrate = [1e-20,1e-14]

lim_viscosity = [1e19,1e25]

bar=True

time_str1 = str(round(step1/2,1)).zfill(5).replace('.','-')
time_str2 = str(round(step2/2,1)).zfill(5).replace('.','-')
    
fig,axs = plt.subplots(2,2,dpi=300,figsize=(8.5,11))

axs = axs.flatten()

bounds = [250,750,450,620]

axs[0].set_title('Model 1: '+ str(time1) +' Ma',loc='left')
axs[1].set_title('Model 2: '+ str(time2)  +' Ma',loc='left')

axs[2].set_title('Plastic Strain',loc='center')

vp.plot2D(file1,'comp_field',bounds=bounds,ax=axs[0],
            cmap=cm,colorbar=False)

vp.plot2D(file2,'comp_field',bounds=bounds,ax=axs[1],
            cmap=cm,colorbar=False)

vp.plot2D(file1,'plastic_strain',bounds=bounds,ax=axs[2],
            cmap=opaque_cm,colorbar=bar,clim=lim_strain)

vp.plot2D(file2,'plastic_strain',bounds=bounds,ax=axs[3],
            cmap=opaque_cm,colorbar=bar,clim=lim_strain)

plt.tight_layout()

fig.savefig(sys.argv[6])
