"""
Script to plot final models for slow convergence
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pyvista as pv

from matplotlib import rc
rc("pdf", fonttype=42)

import vtk_plot as vp

pv.start_xvfb()

# The following 8 models need to be plotted
# slow_cold_half 080122_rip_a
# slow_cold_half_qui 080122_rip_e
# slow_cold_full 080122_rip_b
# slow_cold_full_qui 080122_rip_f
# hot_fast_half 080122_rip_c
# hot_fast_half_qui 080122_rip_g
# hot_fast_full 080122_rip_d
# hot_fast_full_qui 080122_rip_h

# Make list of models with appropriate names
models = ['080122_rip_a','080122_rip_e','080122_rip_b','080122_rip_f',
          '080122_rip_c','080122_rip_g','080122_rip_d','080122_rip_h']

names = ['Model ' + str(x) for x in range(9,17)]

# Indicate time of final rift of reach model (post-cooling)

times = [16,36,32,52,7.3,27.3,14.5,34.5]
tstep_interval = 0.1

# Set up the figure

fig,axs = plt.subplots(4,2,dpi=300,figsize=(4,5))
bounds = [300,700,400,620]

colors=['#99CCCC','#996633','#990000','#339966']
cm = ListedColormap(colors)

# Set opacity for strain
opacity_strain = [0,0.7,0.7,0.7,0.7]
lim_strain = [0,5]
cm_strain = 'inferno'

# Do the loop to plot

for k,model in enumerate(models):
    
    ax = axs.flat[k]
    
    # Get the appropriate pvtu file
    base_dir = r'/mnt/f44f06b4-89ef-4d7c-a41d-6dbf331c8d4e/riftinversion_production/'
    suffix = r'/output_ri_rift/solution'
    pvtu_dir = base_dir + model + suffix
    
    # Figure out appropriate timesteps
    tstep_invert = int((times[k]+4)/tstep_interval)
    
    if model == '080122_rip_a':
        tstep_invert = 194
    if model =='080122_rip_e':
        tstep_invert = 395
    
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
    
fig.savefig('all_final_fast_tiny.pdf')

project_dir = '/home/dyvasey/hawksey/UCD Box/UC Davis/Manuscripts/RiftInversion_Geology/python_figs/all_final_fast_tiny.pdf'
fig.savefig(project_dir)      
    




