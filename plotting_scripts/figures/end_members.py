"""
Script to plot end=member models for Geology manuscript
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

# Make list of models with appropriate names
models = ['063022_rip_c',
          '070422_rip_c','070422_rip_e']

names = ['Model 1 - Style AU','Model 5 - Style DT','Model 3 - Style PF']

# Indicate times for each model
times_start = [16,7.3,32]
times_intermed = [x+10 for x in times_start]
times_final = [x+20 for x in times_start]
tstep_interval = 0.1

# Set up the figure

fig,axs = plt.subplots(3,3,dpi=300,figsize=(7,5))
bounds = [300,700,400,620]

colors=['#66CCEE','#BBBBBB','#EE6677','#228833']
cm = ListedColormap(colors)

# Set opacity for strain
opacity_strain = [0,0.8,0.8,0.8,0.8]
lim_strain = [0,5]
cm_strain = 'inferno_r'


# Do the loop to plot

for k,model in enumerate(models):
    
    # Get the appropriate pvtu file
    base_dir = r'/mnt/f44f06b4-89ef-4d7c-a41d-6dbf331c8d4e/riftinversion_production/'
    suffix = r'/output_ri_rift/solution'
    
    pvtu_dir = base_dir + model + suffix
    
    # Figure out appropriate timesteps
    tstep_rift = int(times_start[k]/tstep_interval)
    tstep_intermed = int(times_intermed[k]/tstep_interval)
    tstep_final = int(times_final[k]/tstep_interval)
    
    tsteps = np.array([tstep_rift,tstep_intermed,tstep_final])
    
    # Pull the file locations
    files = vp.get_pvtu(pvtu_dir,tsteps)
    
    # Plot
    
    for column in range(3):
        ax = axs[k,column]
        ax.tick_params(axis='both',labelsize=6)
        
        vp.plot2D(files[column],'comp_field',bounds=bounds,ax=ax,
                  cmap=cm,contours=True)
    
        vp.plot2D(files[column],'noninitial_plastic_strain',bounds=bounds,ax=ax,
                  cmap=cm_strain,opacity=opacity_strain,clim=lim_strain)
    
    axs[k,0].set_title(names[k] + ': ' + str(tstep_rift/10) + ' Myr',
                       fontsize=8)
    axs[k,1].set_title(str(tstep_intermed/10) + ' Myr',
                       fontsize=8)
    axs[k,2].set_title(str(tstep_final/10) + ' Myr',
                       fontsize=8)
    
    
axs[2,0].set_xlabel('X Position (km)',fontsize=6)
axs[2,1].set_xlabel('X Position (km)',fontsize=6)
axs[2,2].set_xlabel('X Position (km)',fontsize=6)

axs[0,0].set_ylabel('Y Position (km)',fontsize=6)
axs[1,0].set_ylabel('Y Position (km)',fontsize=6)
axs[2,0].set_ylabel('Y Position (km)',fontsize=6)
     
plt.tight_layout() 
    
fig.savefig('end_members.pdf')

project_dir = '/home/dyvasey/hawksey/UCD Box/UC Davis/Manuscripts/RiftInversion_Geology/python_figs/end_members.pdf'

fig.savefig(project_dir)    




