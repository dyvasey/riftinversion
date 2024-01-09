"""
Plotter for extended timestep figures for supplemental models for
Geology manuscript
"""
import os
import shutil

import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv
from matplotlib.colors import ListedColormap

from tqdm import tqdm

from riftinversion import vtk_plot as vp

# Get model paths
base_dir = r'/mnt/f44f06b4-89ef-4d7c-a41d-6dbf331c8d4e/ri_production_supp/'
suffix = r'/output_ri_rift/solution'

models = [folder for folder in os.listdir(base_dir) if folder.endswith("_inv")]
models.sort()

# Rift times post-cooling
rift_times = [16]*4 + [56]

# Final invert times
invert_times= [36,36,56,116,76]

model_step = 0.1
image_dir = 'images/'

# Set up directory for images
output_dir = 'extended_timesteps_supp/'
try:
    shutil.rmtree(output_dir)
except:
    print("Creating new directory...")
else:
    print("Cleared existing directory...")
    
os.makedirs(output_dir,exist_ok=False)

# Set up colormaps
colors=['#66CCEE','#BBBBBB','#EE6677','#228833']
cm = ListedColormap(colors)

# For legend colorbar
colors_barorder = [colors[0],colors[3],colors[2],colors[1]]
cm_bar = ListedColormap(colors_barorder)

opaque_cm = 'inferno_r'
opaque_cm_rev = 'inferno'

lim_strain = [0,5]
lim_strainrate = [1e-20,2e-13]
lim_viscosity = [1e19,1e25]

# Pyvista colorbar on image
bar=False

# Colorbar label size
cbar_label = 8

# Loop through each model
for x,model in enumerate(models):  
    
    # Get model files
    directory = base_dir + model + suffix
    time_total = invert_times[x]  
    
    nsteps = int(time_total/model_step)
    
    # Get inversion timesteps in equal increments of strain
    start = rift_times[x]
    start_step = int(start/model_step)
    
    end = time_total
    inv_time = end-start
    
    scale_factor = 1
    
    if inv_time==20:
        increment=5*scale_factor
    elif inv_time==40:
        increment=10*scale_factor
    elif inv_time==100:
        increment=25*scale_factor
    else:
        print('Invalid invert time')
    
    timesteps = np.arange(start_step,nsteps,increment)
    times = timesteps*model_step
    
    files = vp.get_pvtu(directory,timesteps)
    
    # Set up lists of parameters for the 4 figures
    titles = ['Comp/Temp','Strain','Strain Rate','Viscosity']
    fields = ['comp_field','plastic_strain','strain_rate','viscosity']
    cbars = ['False',bar,bar,bar]
    log_scale = [False,False,True,True]
    contours = [True,False,False,False]
    clims = [[0,3],lim_strain,lim_strainrate,lim_viscosity]
    cmaps = [cm,opaque_cm,opaque_cm_rev,opaque_cm]
    bounds = [250,750,450,620]
    
    max_srates = np.zeros(len(timesteps))
    bounds_maxsr = [300,700,550,620]
    
    for k,step in enumerate(tqdm(timesteps)):
        mesh = pv.read(files[k])
        bounds_mesh = [bound*1e3 for bound in bounds_maxsr] + [0,0]
        clipped = mesh.clip_box(bounds_mesh)
        srates = clipped['strain_rate']
        max_srates[k] = np.max(srates)
        
    sfig,ax = plt.subplots(1,dpi=300)
    ax.plot(times,max_srates)
    ax.set_ylim(1e-15,2e-13)
    sfig.savefig(output_dir+models[x]+'_'+'max_sr'+'.jpg')
    
    for n in range(4):
        fig,axs = plt.subplots(8,5,dpi=300,figsize=(24,15))
        axs = axs.flatten()
        fig.suptitle(titles[n])
    
        # Plot each timestep
        for k,step in enumerate(tqdm(timesteps)):
            time = step*model_step
            time_str = str(round(time,1)).zfill(5).replace('.','-')
            
            axs[k].set_title(str(round(time,1)) +' Ma',loc='left')
            
            vp.plot2D(files[k],fields[n],bounds=bounds,ax=axs[k],
                      cmap=cmaps[n],colorbar=cbars[n],contours=contours[n],
                      clim=clims[n],log_scale=log_scale[n])
    
            
            # Add colorbars
            #cax = vp.add_colorbar(fig,vmin=clims[n][0],vmax=clims[n][1],
            #                      cmap=cmaps[n],
            #                    location=[0.7,0.5,0.2,0.02])
    
            #cax.tick_params(axis='both',labelsize=cbar_label)
            
            # Get max strain rate
            

            
        plt.tight_layout()
        fig.savefig(output_dir+models[x]+'_'+fields[n]+'.jpg')
        
        fig.clear()
        plt.close(fig)
        

        
        

