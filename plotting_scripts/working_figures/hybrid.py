"""
Script to plot hybrid models for Geology manuscript
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pyvista as pv

from matplotlib import rc
rc("pdf", fonttype=42)

import vtk_plot as vp

# Summary of models:

# 1 cm/yr convergence
# slow_cold_half 063022_rip_c
# slow_cold_half_qui 071822_rip_b
# slow_cold_full 070422_rip_e
# slow_cold_full_qui 072022_rip_a
# hot_fast_half 070422_rip_c
# hot_fast_half_qui 071322_rip
# hot_fast_full 070622_rip_a
# hot_fast_full_qui 072022_rip_b

models = ['071822_rip_b','072022_rip_a',
          '071322_rip']

# Indicate times for each model
times_start = [36,52,27.3]
times_final = [x+20 for x in times_start]
tstep_interval = 0.1

# Set up the figure

fig,axs = plt.subplots(3,dpi=300,figsize=(3,5))
bounds = [300,700,400,620]

colors=['#99CCCC','#996633','#990000','#339966']
cm = ListedColormap(colors)

# Set opacity for strain
opacity_strain = [0,0.7,0.7,0.7,0.7]
lim_strain = [0,5]
cm_strain = 'inferno'

for k,model in enumerate(models):
    
    # Get the appropriate pvtu file
    base_dir = r'/mnt/f44f06b4-89ef-4d7c-a41d-6dbf331c8d4e/riftinversion_production/'
    suffix = r'/output_ri_rift/solution'
    
    pvtu_dir = base_dir + model + suffix
    
    # Figure out appropriate timesteps
    tstep_final = int(times_final[k]/tstep_interval)
    
    # Pull the file locations
    file = vp.get_pvtu(pvtu_dir,tstep_final)
    
    # Plot
    ax = axs[k]
    
    vp.plot2D(file,'comp_field',bounds=bounds,ax=ax,
              cmap=cm,contours=True)
    
    
    vp.plot2D(file,'noninitial_plastic_strain',bounds=bounds,ax=ax,
              cmap=cm_strain,opacity=opacity_strain,clim=lim_strain)
    
    ax.tick_params(axis='both',labelsize=6)
    
    ax.set_xlabel('X Position (km)',fontsize=6)
    ax.set_ylabel('Y Position (km)',fontsize=6)
    
plt.tight_layout() 
    
fig.savefig('hybrid.pdf')

project_dir = (
    '/home/dyvasey/hawksey/UCD Box/UC Davis/Manuscripts/RiftInversion_Geology/python_figs/hybrid.pdf'
    )
fig.savefig(project_dir)    
