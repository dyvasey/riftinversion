"""
Script to plot final models for slow convergence
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pyvista as pv

from matplotlib import rc
rc("pdf", fonttype=42)

pv.start_xvfb()

import vtk_plot as vp

# The following 8 models need to be plotted
# slow_cold_half 063022_rip_c
# slow_cold_half_qui 071822_rip_b
# slow_cold_full 070422_rip_e
# slow_cold_full_qui 072022_rip_a
# hot_fast_half 070422_rip_c
# hot_fast_half_qui 071322_rip
# hot_fast_full 070622_rip_a
# hot_fast_full_qui 072022_rip_b

# Make list of models with appropriate names
models = ['063022_rip_c','071822_rip_b','070422_rip_e','072022_rip_a',
          '070422_rip_c','071322_rip','070622_rip_a','072022_rip_b']

names = ['Model ' + str(x) for x in range(1,9)]

# Indicate time of final rift of reach model (post-cooling)

times = [16,36,32,52,7.3,27.3,14.5,34.5]
tstep_interval = 0.1

# Set up the figure

fig,axs = plt.subplots(4,2,dpi=300,figsize=(4,5))
bounds = [300,700,400,620]

colors=['#66CCEE','#BBBBBB','#EE6677','#228833']
cm = ListedColormap(colors)

# Set opacity for strain
opacity_strain = [0,0.8,0.8,0.8,0.8]
lim_strain = [0,5]
cm_strain = 'inferno_r'

# Do the loop to plot

for k,model in enumerate(models):
    
    ax = axs.flat[k]
    
    # Get the appropriate pvtu file
    base_dir = r'/mnt/f44f06b4-89ef-4d7c-a41d-6dbf331c8d4e/riftinversion_production/'
    suffix = r'/output_ri_rift/solution'
    pvtu_dir = base_dir + model + suffix
    
    # Figure out appropriate timesteps
    tstep_invert = int((times[k]+20)/tstep_interval)
    
    # Pull the file locations
    file = vp.get_pvtu(pvtu_dir,tstep_invert)
    
    # Plot

    vp.plot2D(file,'comp_field',bounds=bounds,ax=ax,
              cmap=cm,contours=False)

    vp.plot2D(file,'noninitial_plastic_strain',bounds=bounds,ax=ax,
              cmap=cm_strain,opacity=opacity_strain,clim=lim_strain)
    
    #ax.set_title(names[k] + ': '+ str(times[k]+20) + ' Myr',fontsize=8)
    ax.tick_params(axis='both',labelsize=6)
    ax.set_xticks([300,700])
    ax.set_xticklabels(['3','7'])
    ax.set_yticks([400,600])
    ax.set_yticklabels(['4','6'])

#axs[3,0].set_xlabel('X Position (km)',fontsize=6)
#axs[3,1].set_xlabel('X Position (km)',fontsize=6)
#axs[0,0].set_ylabel('Y Position (km)',fontsize=6)
#axs[1,0].set_ylabel('Y Position (km)',fontsize=6)
#axs[2,0].set_ylabel('Y Position (km)',fontsize=6)
#axs[3,0].set_ylabel('Y Position (km)',fontsize=6)
    
fig.savefig('all_final_slow_tiny.pdf')

project_dir = '/home/dyvasey/hawksey/UCD Box/UC Davis/Manuscripts/RiftInversion_Geology/python_figs/all_final_slow_tiny.pdf'
fig.savefig(project_dir)    
    




