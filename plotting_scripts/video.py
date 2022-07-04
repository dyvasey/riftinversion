"""
Basic video plotter from command line. Requires 4 arguments: directory, time covered by model, 
time between model outputs, and output file
"""
import sys
import os
import shutil

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import cv2
import pyvista as pv

from tqdm import tqdm

from riftinversion import vtk_plot as vp

pv.start_xvfb()

directory = sys.argv[1]
time = float(sys.argv[2])
model_step = float(sys.argv[3])

nsteps = int(time/model_step)

timesteps = np.arange(0,nsteps+1,1)

files = vp.get_pvtu(directory,timesteps)

image_dir = 'images/'

try:
    shutil.rmtree(image_dir)
except:
    print("Creating new image directory...")
else:
    print("Cleared existing image directory...")

os.makedirs(image_dir,exist_ok=False)

colors=['#99CCCC','#996633','#990000','#339966']
cm = ListedColormap(colors)

opaque_cm = 'inferno_r'
opaque_cm_rev = 'inferno'

lim_strain = [0,5]

lim_strainrate = [1e-20,1e-14]

lim_viscosity = [1e19,1e25]

bar=True

# Get scalar range
for k,step in enumerate(tqdm(timesteps)):
    time = step*model_step
    time_str = str(round(step/2,1)).zfill(5).replace('.','-')
    
    fig,axs = plt.subplots(2,2,dpi=300,figsize=(8.5,11))
    
    axs = axs.flatten()

    axs[0].set_title(time_str +' Ma',loc='left')
    
    axs[1].set_title('Strain',loc='center')
    
    vp.plot2D(files[k],'comp_field',bounds=[250,750,450,620],ax=axs[0],
              cmap=cm,colorbar=False)
    vp.plot2D(files[k],'plastic_strain',bounds=[250,750,450,620],ax=axs[1],
              cmap=opaque_cm,colorbar=bar,clim=lim_strain)

    axs[2].set_title('Strain Rate',loc='right')
    
    
    vp.plot2D(files[k],'strain_rate',bounds=[250,750,450,620],ax=axs[2],
              cmap=opaque_cm_rev,log_scale=True,
              colorbar=bar,clim=lim_strainrate)
    
    axs[3].set_title('Viscosity',loc='right')
    
    vp.plot2D(files[k],'viscosity',bounds=[250,750,450,620],ax=axs[3],
              cmap=opaque_cm,log_scale=True,
              colorbar=bar,clim=lim_viscosity)

    plt.tight_layout()
    fig.savefig(image_dir+time_str+'.jpg')
    plt.close()
    
#%% Make movie
img_paths = [image_dir+file for file in sorted(os.listdir(image_dir)) if file.endswith('.jpg')]

frame = cv2.imread(img_paths[0])
height,width,layers = frame.shape

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

frate = 2/model_step

video = cv2.VideoWriter(sys.argv[4], fourcc, frate, (width,height))

for img in img_paths:
    video.write(cv2.imread(img))

cv2.destroyAllWindows()
video.release()
