"""
Script to plot initial conditions of models for Geology manuscript
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
models_stan = ['063022_rip_c','070422_rip_e',
          '070422_rip_c','070622_rip_a']

models_cool = ['071822_rip_b','072022_rip_a','071322_rip','072022_rip_b']

titles = ['Slow, Cold Halfway','Slow, Cold Full Breakup','Hot, Fast Halfway',
          'Hot, Fast Full Breakup']

# Indicate time of final rift of reach model (post-cooling)

times_stan = [16,32,7.3,14.5]
times_cool = [x+20 for x in times_stan]
tstep_interval = 0.1

# Set up the figure

fig,axs = plt.subplots(2,2,dpi=300,figsize=(5,4))
bounds = [300,700,400,620]

colors=['#66CCEE','#BBBBBB','#EE6677','#228833']
cm = ListedColormap(colors)

# Set opacity for strain
opn = 0.8
opacity_strain = [0,opn,opn,opn,opn]
lim_strain = [0,5]
cm_strain = 'inferno_r'

# Set colormap for colorbar
orig_cmap = plt.get_cmap(cm_strain)
orig_colors = orig_cmap(np.arange(orig_cmap.N))
cutoff= int(orig_cmap.N/5)

alpha = np.concatenate((np.linspace(0,opn,cutoff), np.ones(orig_cmap.N-cutoff)*opn))

orig_colors[:,-1] = alpha

new_cmap = ListedColormap(orig_colors)

# Do the loop to plot

for k,model in enumerate(models_stan):
    
    # Get the appropriate pvtu file
    base_dir = r'/mnt/f44f06b4-89ef-4d7c-a41d-6dbf331c8d4e/riftinversion_production/'
    suffix = r'/output_ri_rift/solution'
    
    pvtu_dir_stan = base_dir + model + suffix
    pvtu_dir_cool = base_dir + models_cool[k] + suffix
    
    # Figure out appropriate timesteps
    tstep_rift_stan = int(times_stan[k]/tstep_interval)
    tstep_rift_cool = int(times_cool[k]/tstep_interval)
    
    # Pull the file locations
    file_stan = vp.get_pvtu(pvtu_dir_stan,tstep_rift_stan)
    file_cool = vp.get_pvtu(pvtu_dir_cool,tstep_rift_cool)
    
    # Plot
    ax = axs.flat[k]
    
    vp.plot2D(file_stan,'comp_field',bounds=bounds,ax=ax,
              cmap=cm)
    
    vp.plot2D(file_stan,'comp_field',bounds=bounds,ax=ax,
              cmap=cm,contours=True,contour_color='black',
              contours_only=True)
    
    vp.plot2D(file_cool,'comp_field',bounds=bounds,ax=ax,
              cmap=cm,contours=True,contour_color='white',
              contours_only=True)
    
    vp.plot2D(file_stan,'noninitial_plastic_strain',bounds=bounds,ax=ax,
              cmap=cm_strain,opacity=opacity_strain,clim=lim_strain,
              colorbar=False)
    
    ax.tick_params(axis='both',labelsize=6)
    ax.set_title(titles[k],fontsize=8)
    
axs[1,0].set_xlabel('X Position (km)',fontsize=6)
axs[1,1].set_xlabel('X Position (km)',fontsize=6)
axs[0,0].set_ylabel('Y Position (km)',fontsize=6)
axs[1,0].set_ylabel('Y Position (km)',fontsize=6)

cax = vp.add_colorbar(fig,vmin=lim_strain[0],vmax=lim_strain[1],cmap=new_cmap,
                    location=[0.2,0.5,0.2,0.02])

cax.tick_params(axis='both',labelsize=6)
cax.set_title('Plastic Strain',fontsize=6)  
cax.set_xticks([0,5])

colors_barorder = [colors[0],colors[3],colors[2],colors[1]]
cm_bar = ListedColormap(colors_barorder)

cax2 = vp.add_colorbar(fig,cmap=cm_bar,
                location=[0.6,0.47,0.05,0.09],ticks=[0.125,0.375,0.625,0.875],
                orientation='vertical')

cax2.tick_params(labelsize=6)

cax2.set_yticklabels(['Asthenosphere','Mantle Lithosphere','Lower Crust','Upper Crust'])
     
plt.tight_layout() 
    
fig.savefig('initial_conditions.pdf')

project_dir = '/home/dyvasey/hawksey/UCD Box/UC Davis/Manuscripts/RiftInversion_Geology/python_figs/initial_conditions.pdf'

fig.savefig(project_dir)    




