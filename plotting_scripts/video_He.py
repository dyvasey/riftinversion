"""
Video plotter for He ages from command line. Requires 4 arguments: base directory, time covered by model, 
time between model outputs, and output file
"""
import sys
import re
import os
import shutil

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import cv2
import pyvista as pv

from tqdm import tqdm

import vtk_plot as vp

pv.start_xvfb()

directory = sys.argv[1]

time = float(sys.argv[2])
model_step = float(sys.argv[3])

nsteps = int(time/model_step)

timesteps = np.arange(0,nsteps+1,1)

files = [os.path.join(directory,file) for file in os.listdir(directory) if file.endswith('.vtu')]
files.sort(key = lambda x: int(re.split('_|\.', x)[-2]))
print(files)

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

# Get scalar range
for k,step in enumerate(tqdm(timesteps)):
    time = step*model_step
    time_str = str(round(step/2,1)).zfill(5).replace('.','-')
    
    fig,axs = plt.subplots(1,dpi=300,figsize=(8.5,11))

    axs.set_title(str(round(time,1)) +' Ma',loc='left')
    
    vp.plot2D(files[k],'AHe',bounds=[400,600,550,620],ax=axs,
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
