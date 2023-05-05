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

fig,axs = plt.subplots(4,2,dpi=300,figsize=(7,9.5))
bounds = [300,700,400,620]

#colors=['#99CCCC','#996633','#990000','#339966']
# Colors go in order of asthen, upper crust, lower crust, mantle lith
colors=['#66CCEE','#BBBBBB','#EE6677','#228833']
cm = ListedColormap(colors)

# Set opacity for strain
#opacity_strain = [0,1,1,1,1,1,1,1,1,1]
opacity_strain = [0,0.8,0.8,0.8,0.8]
#opacity_strain = [0,0.7,0.7,0.7,0.7]
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
              cmap=cm,contours=True)

    vp.plot2D(file,'noninitial_plastic_strain',bounds=bounds,ax=ax,
              cmap=cm_strain,opacity=opacity_strain,clim=lim_strain)
    
    ax.set_title(names[k] + ': '+ str(times[k]+20) + ' Myr',fontsize=8)
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
    
fig.savefig('all_final_slow.pdf')
fig.savefig('all_final_slow.jpg')

project_dir = '/home/dyvasey/hawksey/UCD Box/UC Davis/Manuscripts/RiftInversion_Geology/python_figs/all_final_slow.jpg'
fig.savefig(project_dir)    
    




