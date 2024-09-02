"""
Compare rifted and inversion tchron signals for NSF proposal
"""
import sys
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pyvista as pv
import cmcrameri as cmc
from matplotlib import rc
rc("pdf", fonttype=42)

sys.path.append('/home/dyvasey/git/riftinversion/')
import vtk_plot as vp

os.environ['GALLIUM_DRIVER']='softpipe'
pv.start_xvfb()

glauc = '/home/vaseylab/glaucophane/'

directory = os.path.join(glauc,'fastscape_testing/060524_rif/output_ri_rift/solution')
directory_He = os.path.join(glauc,'fastscape_testing/meshes_He_060524_rif')
time1 = 16
time2 = 36

model_step = 0.1

step1 = int(time1/model_step)
step2 = int(time2/model_step)

file1 = vp.get_pvtu(directory,step1)
file2 = vp.get_pvtu(directory,step2)
file1_He = os.path.join(directory_He,'meshes_He_060524_rif_160.vtu')
file2_He = os.path.join(directory_He,'meshes_He_060524_rif_360.vtu')

colors=['#66CCEE','#BBBBBB','#EE6677','#228833']
cm = ListedColormap(colors)

opaque_cm = 'cmc.lapaz_r'
cm_strain = 'inferno_r'

opacity_strain = [0,0.8,0.8,0.8,0.8]
lim_strain = [0,5]

lim_He = [0,36]

time_str1 = str(round(step1/2,1)).zfill(5).replace('.','-')
time_str2 = str(round(step2/2,1)).zfill(5).replace('.','-')
    
fig,axs = plt.subplots(3,2,dpi=300,figsize=(4,3))

axs = axs.flatten()

bounds = [250,750,450,620]

axs[0].set_title('Rift',fontsize=8)
axs[1].set_title('Orogen',fontsize=8)

axs[2].set_title('AHe Ages',loc='center',fontsize=8)

vp.plot2D(file1,'comp_field',bounds=bounds,ax=axs[0],
           cmap=cm,colorbar=False,contours=True)

vp.plot2D(file2,'comp_field',bounds=bounds,ax=axs[1],
            cmap=cm,colorbar=False,contours=True)

vp.plot2D(file1,'noninitial_plastic_strain',bounds=bounds,ax=axs[0],
          cmap=cm_strain,opacity=opacity_strain,clim=lim_strain)

vp.plot2D(file2,'noninitial_plastic_strain',bounds=bounds,ax=axs[1],
          cmap=cm_strain,opacity=opacity_strain,clim=lim_strain)

vp.plot2D(file1_He,'AHe',bounds=bounds,ax=axs[2],
            cmap=opaque_cm,colorbar=False,clim=lim_He)

vp.plot2D(file2_He,'AHe',bounds=bounds,ax=axs[3],
            cmap=opaque_cm,colorbar=False,clim=lim_He)

mesh1 = pv.read(file1_He)
mesh2 = pv.read(file2_He)

x1 = np.round(mesh1.points[:,0]/1000,0)
x2 = np.round(mesh2.points[:,0]/1000,0)
He1 = mesh1['AHe']
He2 = mesh2['AHe']

df1 = pd.DataFrame({'x':x1,'AHe':He1})
df1_max = df1.groupby('x').agg({'x':'first','AHe':'max'})
df2 = pd.DataFrame({'x':x2,'AHe':He2})
df2_max = df2.groupby('x').agg({'x':'first','AHe':'max'})
print(df2_max)

axs[0].set_ylabel('Y Distance (km)',fontsize=6)
axs[2].set_ylabel('Y Distance (km)',fontsize=6)
axs[4].plot(df1_max['x'],df1_max['AHe'])
axs[5].plot(df2_max['x'],df2_max['AHe'])
axs[4].set_xlim(250,750)
axs[5].set_xlim(250,750)
axs[4].set_ylim(40,-5)
axs[5].set_ylim(40,-5)
axs[4].set_title('Surface AHe Age',fontsize=6)
axs[4].set_ylabel('Maximum AHe Age (Ma)',fontsize=6)
axs[4].set_xlabel('X Distance (km)',fontsize=6)
axs[5].set_xlabel('X Distance (km)',fontsize=6)

for ax in axs:
    ax.tick_params(axis='both', which='major', labelsize=6)
    

plt.tight_layout()

fig.savefig('riftvsinv.pdf')

# Separately plot colorbar
fig2 = plt.figure(dpi=300)
cax = vp.add_colorbar(fig2,vmin=0,vmax=36,cmap=opaque_cm,location=[0.1,0.1,0.2,0.02])

cax.tick_params(axis='both',labelsize=6)
cax.set_title('AHe Age',fontsize=6)  
cax.set_xticks([0,36])

fig2.savefig('AHe_colorbar.pdf')
