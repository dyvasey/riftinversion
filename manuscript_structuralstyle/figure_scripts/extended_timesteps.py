"""
Plotter for publication-ready videos for Geology manuscript
"""
import os
import shutil

import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv
from matplotlib.colors import ListedColormap

from tqdm import tqdm

from riftinversion import vtk_plot as vp

# Compile all directory locations
models_slow = ['063022_rip_c','071822_rip_b','070422_rip_e','072022_rip_a',
          '070422_rip_c','071322_rip','070622_rip_a','072022_rip_b']

models_fast = ['080122_rip_a','080122_rip_e','080122_rip_b','080122_rip_f',
          '080122_rip_c','080122_rip_g','080122_rip_d','080122_rip_h']

all_models = models_slow + models_fast

# Names for output files

names = ['M01-slow_cold_half','M02-slow_cold_half_qui', 'M03-slow_cold_full',
         'M04-slow_cold_full_qui','M05-hot_fast_half','M06-hot_fast_half_qui',
         'M07-hot_fast_full','M08-hot_fast_full_qui',
         'M09-slow_cold_half_fastinvert','M10-slow_cold_half_qui_fastinvert',
         'M11-slow_cold_full_fastinvert','M12-slow_cold_full_qui_fastinvert',
         'M13-hot_fast_half_fastinvert','M14-hot_fast_half_qui_fastinvert',
         'M15-hot_fast_full_fastinvert','M16-hot_fast_full_qui_fastinvert']

# Rift times post-cooling for both slow and fast sets
rift_times = [16,36,32,52,7.3,27.3,14.5,34.5]
rift_times_doubled = rift_times*2

invert_times_slow = [x+20 for x in rift_times]
invert_times_fast = [x+4 for x in rift_times]

# Manual input of models that didn't fully finish
invert_times_fast[0] = 19.4
invert_times_fast[1] = 39.5

invert_times_all = invert_times_slow + invert_times_fast

model_step = 0.1
image_dir = 'images/'

# Set up directory for images
output_dir = 'extended_timesteps/'
try:
    shutil.rmtree('extended_timesteps')
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
for x,model in enumerate(all_models):  
    
    # Get model files
    base_dir = r'/mnt/f44f06b4-89ef-4d7c-a41d-6dbf331c8d4e/riftinversion_production/'
    suffix = r'/output_ri_rift/solution'
    
    directory = base_dir + model + suffix
    time_total = invert_times_all[x]  
    
    nsteps = int(time_total/model_step)
    
    # Get inversion timesteps in equal increments of strain
    start = rift_times_doubled[x]
    start_step = int(start/model_step)
    
    end = time_total
    
    scale_factor = 1
    
    if (end-start)>10:
        increment=5*scale_factor
    else:
        increment=1*scale_factor
    
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
    sfig.savefig(output_dir+names[x]+'_'+'max_sr'+'.jpg')
    
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
        fig.savefig(output_dir+names[x]+'_'+fields[n]+'.jpg')
        
        fig.clear()
        plt.close(fig)
        

        
        

