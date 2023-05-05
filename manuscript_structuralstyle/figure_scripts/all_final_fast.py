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

fig,axs = plt.subplots(4,2,dpi=300,figsize=(7,9.5))
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
    tstep_invert = int((times[k]+4)/tstep_interval)
    
    if model == '080122_rip_a':
        tstep_invert = 194
    if model =='080122_rip_e':
        tstep_invert = 395
    
    # Pull the file locations
    file = vp.get_pvtu(pvtu_dir,tstep_invert)
    
    # Plot

    vp.plot2D(file,'comp_field',bounds=bounds,ax=ax,
              cmap=cm,contours=True)

    vp.plot2D(file,'noninitial_plastic_strain',bounds=bounds,ax=ax,
              cmap=cm_strain,opacity=opacity_strain,clim=lim_strain)
    
    ax.set_title(names[k] + ': '+ str(tstep_invert/10) + ' Myr',fontsize=8)
    ax.tick_params(axis='both',labelsize=6)

axs[3,0].set_xlabel('X Position (km)',fontsize=6)
axs[3,1].set_xlabel('X Position (km)',fontsize=6)
axs[0,0].set_ylabel('Y Position (km)',fontsize=6)
axs[1,0].set_ylabel('Y Position (km)',fontsize=6)
axs[2,0].set_ylabel('Y Position (km)',fontsize=6)
axs[3,0].set_ylabel('Y Position (km)',fontsize=6)

# Set colormap for colorbar
orig_cmap = plt.get_cmap(cm_strain)
orig_colors = orig_cmap(np.arange(orig_cmap.N))
cutoff= int(orig_cmap.N/5)

alpha = np.concatenate((np.linspace(0,0.8,cutoff), np.ones(orig_cmap.N-cutoff)*0.8))

orig_colors[:,-1] = alpha

new_cmap = ListedColormap(orig_colors)


cax = vp.add_colorbar(fig,vmin=lim_strain[0],vmax=lim_strain[1],cmap=new_cmap,
                    location=[0.2,0.05,0.2,0.01])

cax.tick_params(axis='both',labelsize=6)
cax.set_title('Plastic Strain',fontsize=6,pad=1)  
cax.set_xticks([0,5])

colors_barorder = [colors[0],colors[3],colors[2],colors[1]]
cm_bar = ListedColormap(colors_barorder)

cax2 = vp.add_colorbar(fig,cmap=cm_bar,
                location=[0.6,0.03,0.025,0.045],ticks=[0.125,0.375,0.625,0.875],
                orientation='vertical')

cax2.tick_params(labelsize=6)

cax2.set_yticklabels(['Asthenosphere','Mantle Lithosphere','Lower Crust','Upper Crust'])

plt.subplots_adjust(bottom=0.1)
    
fig.savefig('all_final_fast.pdf')
fig.savefig('all_final_fast.jpg')

project_dir = '/home/dyvasey/hawksey/UCD Box/UC Davis/Manuscripts/RiftInversion_Geology/python_figs/all_final_fast.jpg'
fig.savefig(project_dir)   
    




