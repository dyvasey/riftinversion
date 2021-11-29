"""
Test for forward modeling of ASPECT output, using cookbook output
"""

#%% Import and setup files
import matplotlib.pyplot as plt
import numpy as np

import pyvista as pv

import vtk_plot as vp

# Read in sample data from continental extension cookbook
meshes = pv.read('../../sample_data/vtk_tchron_test.vtm')

#%% Add He ages to final mesh and save
He_mesh = vp.He_age_vtk_parallel(meshes,'AHe',1e5,batch_size=100,interpolate_profile=False)

#%% Plot the new mesh

fig,ax = plt.subplots(dpi=300)

vp.plot2D('mesh_He.vtu','AHe',bounds=[0,200,90,100],cmap='magma_r',ax=ax,
          clim=[0,2])

ages = He_mesh.point_data['AHe']

fig.savefig('vtk_tchron_test.pdf')

