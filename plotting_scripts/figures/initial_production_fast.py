"""
Script to plot initial rift inversion production results (July 2022)
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pyvista as pv

import vtk_plot as vp

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

names = ['Slow/Cold Half-Breakup','Slow/Cold Half-Breakup w/ Cooling',
         'Slow/Cold Full-Breakup','Slow/Cold Full-Breakup w/ Cooling',
         'Hot/Fast Half-Breakup','Hot/Fast  Half-Breakup w/ Cooling',
         'Hot/Fast  Full-Breakup','Hot/Fast Full-Breakup w/ Cooling']

# Indicate time of final rift of reach model (post-cooling)

times = [16,36,32,52,7.3,27.3,14.5,34.5]
tstep_interval = 0.1

# Set up the figure

fig,axs = plt.subplots(8,3,dpi=300,figsize=(11,17))
bounds = [300,700,400,620]

colors=['#99CCCC','#996633','#990000','#339966']
cm = ListedColormap(colors)

# Set opacity for strain
opacity_strain = [0,0.7,0.7,0.7,0.7]
lim_strain = [0,5]
cm_strain = 'Purples'

# Do the loop to plot

for k,model in enumerate(models):
    
    # Get the appropriate pvtu file
    base_dir = r'/mnt/f44f06b4-89ef-4d7c-a41d-6dbf331c8d4e/riftinversion_production/'
    suffix = r'/output_ri_rift/solution'
    pvtu_dir = base_dir + models[k] + suffix
    
    # Get meshes with rift-side information
    #side_dir = r'~/git/gdmate/processing/figs/'
    #side_dir_rift = side_dir + models[k] + '/' +models[k] + '_0.vtu'
    #side_dir_invert = side_dir + models[k] + '/' +models[k] + '_10.vtu'
    
    #if model=='071322_rip':
    #    side_dir_invert = side_dir + models[k] + '/' +models[k] + '_9.vtu'
    
    # Figure out appropriate timesteps
    tstep_initial = 0
    tstep_rift = int(times[k]/tstep_interval)
    tstep_invert = int((times[k]+4)/tstep_interval)
    
    if model == '080122_rip_a':
        tstep_invert = 194
    if model =='080122_rip_e':
        tstep_invert = 395
    
    tsteps = np.array([tstep_initial,tstep_rift,tstep_invert])
    
    # Pull the file locations
    files = vp.get_pvtu(pvtu_dir,tsteps)
    
    # Plot
    for column in range(3):
        vp.plot2D(files[column],'comp_field',bounds=bounds,ax=axs[k,column],
                  cmap=cm,contours=True)

        
    #vp.plot2D(side_dir_rift,'rift_side',bounds=bounds,ax=axs[k,1])
    #vp.plot2D(side_dir_invert,'rift_side',bounds=bounds,ax=axs[k,2])
    
    for column in range(3):
        vp.plot2D(files[column],'noninitial_plastic_strain',bounds=bounds,ax=axs[k,column],
                  cmap=cm_strain,opacity=opacity_strain,clim=lim_strain)
    
    axs[k,0].set_title(names[k]+ ' - Fast')
    axs[k,1].set_title('Rift: '+ str(times[k]) + ' Myr')
    axs[k,2].set_title('Inversion: '+ str(tstep_invert*tstep_interval) + ' Myr')
        
plt.tight_layout()
    
    
fig.savefig('initial_production_fast.pdf')
    




