"""
Test for forward modeling of ASPECT output, using cookbook output
"""

#%% Import and setup files
import matplotlib.pyplot as plt
from matplotlib import cm,colors

import numpy as np

import pyvista as pv

import vtk_plot as vp

# Read in sample data from continental extension cookbook
meshes = pv.read('../../sample_data/vtk_tchron_test.vtm')

#%% Add He ages to final mesh and save
He_mesh = vp.He_age_vtk_parallel(meshes,'AHe',1e5,batch_size=100,
                                 interpolate_profile=False,filename='meshes_He.vtm')
He_mesh_interp = vp.He_age_vtk_parallel(meshes,'AHe',1e5,batch_size=100,
                                        interpolate_profile=True,filename='meshes_He_interp.vtm')

#%% Plot the new mesh

fig,axs = plt.subplots(2,dpi=300)

vp.plot2D('meshes_He/meshes_He_20.vtu','AHe',bounds=[0,200,90,100],cmap='plasma_r',ax=axs[0],
          clim=[0,2])

vp.plot2D('meshes_He_interp/meshes_He_interp_20.vtu','AHe',bounds=[0,200,90,100],cmap='plasma_r',ax=axs[1],
          clim=[0,2])

ages = He_mesh[-1].point_data['AHe']

cax = fig.add_axes([0.1,0.08,0.8,0.02])

norm = colors.Normalize(vmin=0,vmax=2)
mappable = cm.ScalarMappable(norm=norm,cmap='plasma_r')
cbar = plt.colorbar(mappable,orientation='horizontal',cax=cax)
cbar.set_label('AHe Age')
cbar.set_ticks([0,1,2])

fig.savefig('vtk_tchron_test.pdf')

