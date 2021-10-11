# -*- coding: utf-8 -*-
"""
Example use of functions in tchron to forward model AHe
"""
import numpy as np

import pyvista as pv
import vtk_plot as vp

import tchron as tc

#%% Example with handmade data

U = 10.77 # ppm
Th = 20.55 # ppm
radius = 100 # microns
time_interval = 1e6 # years
temps = np.array([500,150,30,30])+273 # K

age_model = tc.forward_model(
    U,Th,radius,temps,time_interval,system='AHe',nodes=500)

#%% Example with model output data

meshes = pv.read(r'C:/Users/dyvas/Box/UC Davis/ASPECT/particles/meshes.vtm')

partial_path = np.arange(0,33,1)

point = 8835564.0


tt = vp.particle_trace(meshes,partial_path,point,'T',
                             x_field='time',
                             plot_path=True)
#%% Run Age Model
tt_c = np.array(tt)

age_model_2 = tc.forward_model(
    U,Th,radius,tt_c,time_interval,system='AHe',nodes=500)

