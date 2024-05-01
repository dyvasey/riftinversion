"""
Plotter for comparing He results across models in a directory
"""

import sys
import os
import shutil

import numpy as np
import matplotlib.pyplot as plt
import cv2
import pyvista as pv

from tqdm import tqdm

import vtk_plot as vp

pv.start_xvfb()

dirs = [d for d in os.listdir(sys.argv[1]) if (os.path.isdir(os.path.join(sys.argv[1],d))) & d.startswith('meshes_He')]
print(dirs)

time = float(sys.argv[2])
model_step = float(sys.argv[3])

nsteps = int(time/model_step)

timesteps = np.arange(0,nsteps+1,1)

image_dir = 'images/'

try:
    shutil.rmtree(image_dir)
except:
    print("Creating new image directory...")
else:
    print("Cleared existing image directory...")

os.makedirs(image_dir,exist_ok=False)

cm='viridis_r'
clim = [0,float(time)]

bar=True

for k,step in enumerate(tqdm(timesteps)):
    time = step*model_step
    time_str = str(round(step/2,1)).zfill(5).replace('.','-')
    
    fig,axs = plt.subplots(len(dirs),dpi=300,figsize=(8.5,11))

    fig.suptitle(str(round(time,1)) +' Ma')

    axs_flat = axs.flatten()

    for k,ax in enumerate(axs_flat):

        directory = dirs[k]
        print(directory)
        ax.set_title(directory)

        end_string = '_'+str(step)+'.vtu'
        file = [os.path.join(directory,file) for file in os.listdir(directory) if file.endswith(end_string)][0]
        print(file)
    
        vp.plot2D(file,'AHe',bounds=[400,600,550,620],ax=ax,
                cmap=cm,colorbar=bar,clim=clim)

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
