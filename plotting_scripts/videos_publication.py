"""
Plotter for publication-ready videos for Geology manuscript
"""
import os
import shutil

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import cv2

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

invert_times_slow = [x+20 for x in rift_times]
invert_times_fast = [x+4 for x in rift_times]

# Manual input of models that didn't fully finish
invert_times_fast[0] = 19.4
invert_times_fast[1] = 39.5

invert_times_all = invert_times_slow + invert_times_fast

model_step = 0.1
image_dir = 'images/'

# Set up directory for videos
output_dir = 'videos_publication/'
try:
    shutil.rmtree('videos_publication/')
except:
    print("Creating new video directory...")
else:
    print("Cleared existing video directory...")
    
os.makedirs(output_dir,exist_ok=False)

# Set up colormaps
colors=['#99CCCC','#996633','#990000','#339966']
cm = ListedColormap(colors)

# For legend colorbar
colors_barorder = ['#99CCCC','#339966','#990000','#996633']
cm_bar = ListedColormap(colors_barorder)

opaque_cm = 'inferno_r'
opaque_cm_rev = 'inferno'

lim_strain = [0,5]
lim_strainrate = [1e-20,1e-14]
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
    
    timesteps = np.arange(0,nsteps+1,1)
    
    files = vp.get_pvtu(directory,timesteps)
    
    # Clear image directory
    try:
        shutil.rmtree(image_dir)
    except:
        print("Creating new image directory...")
    else:
        print("Cleared existing image directory...")
    
    os.makedirs(image_dir,exist_ok=False)
    
    # Plot each timestep
    for k,step in enumerate(tqdm(timesteps)):
        time = step*model_step
        time_str = str(round(time,1)).zfill(5).replace('.','-')
        
        # Set up figure and plot
        fig,axs = plt.subplots(2,2,dpi=150,figsize=(7,5))
        
        axs = axs.flatten()
    
        axs[0].set_title(str(round(time,1)) +' Ma',loc='left')
        
        axs[1].set_title('Strain',loc='center')
        
        vp.plot2D(files[k],'comp_field',bounds=[250,750,450,620],ax=axs[0],
                  cmap=cm,colorbar=False,contours=True)
        vp.plot2D(files[k],'plastic_strain',bounds=[250,750,450,620],ax=axs[1],
                  cmap=opaque_cm,colorbar=bar,clim=lim_strain)
    
        axs[2].set_title('Strain Rate')
        
        
        vp.plot2D(files[k],'strain_rate',bounds=[250,750,450,620],ax=axs[2],
                  cmap=opaque_cm_rev,log_scale=True,
                  colorbar=bar,clim=lim_strainrate)
        
        axs[3].set_title('Viscosity')
        
        vp.plot2D(files[k],'viscosity',bounds=[250,750,450,620],ax=axs[3],
                  cmap=opaque_cm,log_scale=True,
                  colorbar=bar,clim=lim_viscosity)
        
        # Format axes
        axs[2].set_xlabel('X Position (km)')
        axs[3].set_xlabel('X Position (km)')
        axs[0].set_ylabel('Y Position (km)')
        axs[2].set_ylabel('Y Position (km)')

        
        # Add colorbars
        cax = vp.add_colorbar(fig,vmin=lim_strain[0],vmax=lim_strain[1],
                              cmap=opaque_cm,
                            location=[0.7,0.5,0.2,0.02])

        cax.tick_params(axis='both',labelsize=cbar_label)
        cax.set_title('Plastic Strain',fontsize=cbar_label,pad=0)
        cax.set_xticks([0,1,2,3,4,5])
        
        cax2 = vp.add_colorbar(fig,vmin=lim_strainrate[0],vmax=lim_strainrate[1],
                              cmap=opaque_cm_rev,log=True,
                            location=[0.2,0.04,0.2,0.02])

        cax2.tick_params(axis='both',labelsize=cbar_label,pad=0)
        cax2.set_title('Strain Rate ($s^{-1}$)',fontsize=cbar_label,pad=0)  
        
        cax3 = vp.add_colorbar(fig,vmin=lim_viscosity[0],vmax=lim_viscosity[1],
                              cmap=opaque_cm,log=True,
                            location=[0.7,0.04,0.2,0.02])

        cax3.tick_params(axis='both',labelsize=cbar_label,pad=0)
        cax3.set_title('Viscosity ($Pa \cdot s$)',fontsize=cbar_label,pad=0)  

        cax_comp = vp.add_colorbar(fig,cmap=cm_bar,
                        location=[0.1,0.45,0.05,0.12],ticks=[0.125,0.375,0.625,0.875],
                        orientation='vertical')

        cax_comp.tick_params(labelsize=cbar_label)

        cax_comp.set_yticklabels(['Asthenosphere','Mantle Lithosphere',
                                  'Lower Crust','Upper Crust'])
    
        plt.tight_layout()
        fig.savefig(image_dir+time_str+'.jpg')
        
        fig.clear()
        plt.close(fig)
        
    # Make movie
    img_paths = [image_dir+file for file in sorted(os.listdir(image_dir)) if file.endswith('.jpg')]
    
    frame = cv2.imread(img_paths[0])
    height,width,layers = frame.shape
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    frate = 2/model_step
    
    name = output_dir + names[x] +'.mp4'
    
    video = cv2.VideoWriter(name, fourcc, frate, (width,height))
    
    for img in img_paths:
        video.write(cv2.imread(img))
    
    cv2.destroyAllWindows()
    video.release()
