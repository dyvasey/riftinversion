"""
Script to plot AHe ages from calculate_He.py
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv
from matplotlib.colors import ListedColormap

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

fig,axs = plt.subplots(4,2,dpi=300,figsize=(7,9.5))
bounds = [325,675,575,620]

fig2,axs2 = plt.subplots(4,2,dpi=300,figsize=(7,9.5))

colors=['#99CCCC','#996633','#990000','#339966']
cm = ListedColormap(colors)

# Set opacity for strain
opacity_strain = [0,0.7,0.7,0.7,0.7]
lim_He = [0,20]
cm_He = 'plasma_r'

# Do the loop to plot

for k,model in enumerate(models):
    
    ax = axs.flat[k]
    ax2 = axs2.flat[k]
    
    # Get the appropriate vtu file
    base_dir = r'/home/dyvasey/git/riftinversion/plotting_scripts/He_meshes/'
    suffix = r'/meshes_He'
    vtu_dir = base_dir + model + suffix
    
    # Get last mesh
    file = os.path.join(vtu_dir,'meshes_He_199.vtu')
    
    mesh = pv.read(file)
    print(mesh['AHe'].max(),mesh['AHe'].min())
    
        
    # Pull the topography
    topo_base = r'/mnt/f44f06b4-89ef-4d7c-a41d-6dbf331c8d4e/riftinversion_production/'
    topo_suffix = r'/output_ri_rift/'
    topo_dir = topo_base + model + topo_suffix
    topo_allfiles = os.listdir(topo_dir)
    topo_files = []
    for tfile in topo_allfiles:
        if tfile.startswith('topography'):
            topo_files.append(tfile)
    topo_files.sort()            
    topo = os.path.join(topo_dir,topo_files[-1])
    
    surface_particles = vp.get_surface_particles(mesh,topo,buffer=1000)
    surface_ids = surface_particles.index
    ids = mesh['id']
    ages = mesh['AHe']
    surface_ages = []
    for n in surface_ids:
        # Add 0 index to avoid duplicates
        index = np.where(ids==n)[0]
        age = ages[index][0]
        surface_ages.append(age)
    
    surface_x = surface_particles['X']
    
    # Plot
    vp.plot2D(file,'AHe',bounds=bounds,ax=ax,
              cmap=cm_He,opacity=1,clim=lim_He)
    
    ax.set_title(names[k] + ': '+ str(times[k]+20) + ' Myr',fontsize=8)
    ax.tick_params(axis='both',labelsize=6)
    
    ax2.scatter(surface_x,surface_ages,vmin=lim_He[0],vmax=lim_He[1],c=surface_ages,
                cmap='plasma_r')
    ax2.set_ylim(-10,50)
    ax2.set_xlim(bounds[0]*1000,bounds[1]*1000)
    ax2.invert_yaxis()

axs[3,0].set_xlabel('X Position (km)',fontsize=6)
axs[3,1].set_xlabel('X Position (km)',fontsize=6)
axs[0,0].set_ylabel('Y Position (km)',fontsize=6)
axs[1,0].set_ylabel('Y Position (km)',fontsize=6)
axs[2,0].set_ylabel('Y Position (km)',fontsize=6)
axs[3,0].set_ylabel('Y Position (km)',fontsize=6)

cax = vp.add_colorbar(fig,vmin=lim_He[0],vmax=lim_He[1],cmap=cm_He,
                    location=[0.2,0.05,0.2,0.01])

cax.tick_params(axis='both',labelsize=6)
cax.set_title('AHe Age',fontsize=6,pad=1)  

colors_barorder = ['#99CCCC','#339966','#990000','#996633']
cm_bar = ListedColormap(colors_barorder)

cax2 = vp.add_colorbar(fig,cmap=cm_bar,
                location=[0.6,0.03,0.025,0.045],ticks=[0.125,0.375,0.625,0.875],
                orientation='vertical')

cax2.tick_params(labelsize=6)

cax2.set_yticklabels(['Asthenosphere','Mantle Lithosphere','Lower Crust','Upper Crust'])

plt.subplots_adjust(bottom=0.1)
   
fname1 = 'all_He_slow.pdf'
fname2 = 'He_slow_surface.pdf'
project_dir = r'/home/dyvasey/hawksey/UCD Box/UC Davis/Manuscripts/RiftInversion_Geology/python_figs/'
    
fig.savefig(fname1)
fig.savefig(project_dir+fname1)

fig2.savefig(fname2)
fig2.savefig(project_dir+fname2)

