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

# Set up the figures

fig1,axs1 = plt.subplots(8,5,dpi=300,figsize=(6.5,9))
#fig2,axs2 = plt.subplots(4,5,dpi=300,figsize=(7,5))
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
    
    #axes = np.concatenate((axs1.flatten(),axs2.flatten()))
    axes = axs1.flatten()
    
    # Get the appropriate pvtu file
    base_dir = r'/mnt/f44f06b4-89ef-4d7c-a41d-6dbf331c8d4e/riftinversion_production/'
    suffix = r'/output_ri_rift/solution'
    pvtu_dir = base_dir + model + suffix
    
    # Figure out appropriate timesteps
    tsteps_invert = np.array([int(round((times[k]+x)/tstep_interval)) for x in [0,5,10,15,20]])
    
    # Pull the file locations
    files = vp.get_pvtu(pvtu_dir,tsteps_invert)
    
    # Plot
    for n,file in enumerate(files):
        ax = axes[k*5+n]
        vp.plot2D(file,'comp_field',bounds=bounds,ax=ax,
                  cmap=cm,contours=True)
    
        vp.plot2D(file,'noninitial_plastic_strain',bounds=bounds,ax=ax,
                  cmap=cm_strain,opacity=opacity_strain,clim=lim_strain)
        
        time_label = str((tsteps_invert[n]-tsteps_invert[0])/10)
        
        ax.set_title(names[k] + ': '+ time_label + ' m.y.',fontsize=6,
                     weight='bold')
        
        ax.set_xticks([300,700])
        ax.set_yticks([400,600])
        
        ax.tick_params(axis='both',
                       labelsize=6)
        if n==0:
            ax.set_ylabel('Y Position (km)',fontsize=6)
        elif n>0:
            ax.tick_params(axis='y',labelleft=False)
        
        if k==7:
            ax.set_xlabel('X Position (km)',fontsize=6)
        elif k<7:
            ax.tick_params(axis='x',labelbottom=False)

# Set colormap for colorbar
orig_cmap = plt.get_cmap(cm_strain)
orig_colors = orig_cmap(np.arange(orig_cmap.N))
cutoff= int(orig_cmap.N/5)

alpha = np.concatenate((np.linspace(0,0.8,cutoff), np.ones(orig_cmap.N-cutoff)*0.8))

orig_colors[:,-1] = alpha

new_cmap = ListedColormap(orig_colors)

for fig in [fig1]:
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
    
fig1.savefig('all_final_slow_ext.pdf')
fig1.savefig('all_final_slow_ext.jpg')
#fig2.savefig('all_final_slow_ext2.pdf')
#fig2.savefig('all_final_slow_ext2.jpg')

project_dir1 ='/home/dyvasey/hawksey/tufts_box/internal_files/manuscripts/Vasey_RiftInversion_Geology/python_figs/all_final_slow_ext.pdf'
fig1.savefig(project_dir1)    

#project_dir2 ='/home/dyvasey/hawksey/tufts_box/internal_files/manuscripts/Vasey_RiftInversion_Geology/python_figs/all_final_slow_ext2.pdf'
#fig2.savefig(project_dir2)     




