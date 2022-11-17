# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 16:21:32 2021

@author: dyvas
"""
import numpy as np

import vtk_plot as vp
from geoscripts import geophysics as gph

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import ListedColormap
from matplotlib import rc
rc("pdf", fonttype=42)
font = {'size':6}
rc('font',**font)

directory = '/mnt/f44f06b4-89ef-4d7c-a41d-6dbf331c8d4e/riftinversion_production/063022_rip_c/output_ri_rift/solution'
directory_hot = '/mnt/f44f06b4-89ef-4d7c-a41d-6dbf331c8d4e/riftinversion_production/070422_rip_c/output_ri_rift/solution'

timesteps = 0

file = vp.get_pvtu(directory,timesteps)
file_hot = vp.get_pvtu(directory_hot,timesteps)

# Set constants from prm
strain_rate = 1e-15

rho_uc_low = 2729.044834307992
rho_lc_low = 2826.510721247563
rho_mantle_low =3216.374269005848

densities = [rho_uc_low,rho_lc_low,rho_mantle_low,rho_mantle_low]

# Dislocation Creep Factors
A = [8.57e-28,7.13e-18,6.52e-16,6.52e-16]
E = [223.e3,345.e3,530.e3,530.e3]
n = [4.,3.,3.5,3.5]
V = [0,0,18.e-6,18.e-6]

# Diffusion Creep Factors
A_df = [1.e-50,1.e-50,1.e-50,2.37e-15]
E_df = [0,0,0,375.e3]
m = [0,0,0,3.]
d = 1.e-3
V_df = [0,0,0,2.e-6]

# Calculate cold profile

z,comp,disl,diff,t,p = gph.viscosity_profile(A=A,A_df=A_df,n=n,d=d,m=m,E=E,E_df=E_df,V=V,
                               V_df=V_df,densities=densities,thicknesses=[20,20,80],
                               heat_flow=0.04812)


viscous_strength = 2*comp*strain_rate

plastic_strength = gph.drucker_prager(p,internal_friction=30)

eff_strength = np.minimum(viscous_strength,plastic_strength)


# Calculate hot profile
z_hot,comp,disl,diff,t_hot,p = gph.viscosity_profile(A=A,A_df=A_df,n=n,d=d,m=m,E=E,E_df=E_df,V=V,
                               V_df=V_df,densities=densities,thicknesses=[20,20,40],
                               heat_flow=0.06021)


viscous_strength = 2*comp*strain_rate

plastic_strength = gph.drucker_prager(p,internal_friction=30)

eff_strength_hot = np.minimum(viscous_strength,plastic_strength)


#%% Plotting

fig,axs = plt.subplots(2,3,dpi=300,figsize=(7,5))

axs = axs.flat

colors=['#99CCCC','#996633','#990000','#339966']
cm = LinearSegmentedColormap.from_list('fields',colors)

vp.plot2D(file,'comp_field',[0,1000,0,600],ax=axs[0],cmap=cm)
axs[0].set_xlabel('X Position (km)',fontsize=6)
axs[0].set_ylabel('Y Position (km)',fontsize=6)
axs[0].set_title('Model Setup - Slow, Cold Rift')
axs[0].tick_params(axis="y",direction="in", pad=-16)
axs[0].set_yticks([100,200,300,400,500])

axs[1].plot(eff_strength/1e6,z/1000,c='blue',linewidth=1)
axs[1].set_ylim(150,0)
axs[1].set_xlabel('Differential Stress (MPa)',fontsize=6)
axs[1].set_ylabel('Depth (km)',fontsize=6)
axs[1].set_title('Strength Profile')
axs[1].set_xlim(-10,810)

axs[2].plot(t-273,z/1000,c='blue',linewidth=1)
axs[2].set_ylim(150,0)
axs[2].set_xlabel('Temperature ($\degree C$)',fontsize=6)
axs[2].set_title('Geothermal Gradient')

vp.plot2D(file_hot,'comp_field',[0,1000,0,600],ax=axs[3],cmap=cm)
axs[3].set_xlabel('X Position (km)',fontsize=6)
axs[3].set_ylabel('Y Position (km)',fontsize=6)
axs[3].set_title('Model Setup - Hot, Fast Rift')
axs[3].tick_params(axis="y",direction="in", pad=-16)
axs[3].set_yticks([100,200,300,400,500])

axs[4].plot(eff_strength_hot/1e6,z_hot/1000,c='red',linewidth=1)
axs[4].set_ylim(150,0)
axs[4].set_xlabel('Differential Stress (MPa)',fontsize=6)
axs[4].set_ylabel('Depth (km)',fontsize=6)
axs[4].set_title('Strength Profile')
axs[4].set_xlim(-10,810)

axs[5].plot(t_hot-273,z_hot/1000,c='red',linewidth=1)
axs[5].set_ylim(150,0)
axs[5].set_xlabel('Temperature ($\degree C$)',fontsize=6)
axs[5].set_title('Geothermal Gradient')

for ax in axs:
    ax.tick_params(labelsize=6)

colors_barorder = ['#99CCCC','#339966','#990000','#996633']
cm_bar = ListedColormap(colors_barorder)

cax2 = vp.add_colorbar(fig,cmap=cm_bar,
                location=[0.1,0.47,0.03,0.09],ticks=[0.125,0.375,0.625,0.875],
                orientation='vertical')

cax2.tick_params(labelsize=6)

cax2.set_yticklabels(['Asthenosphere','Mantle Lithosphere','Lower Crust','Upper Crust'])

plt.tight_layout()

fig.savefig('initial_analytical.pdf')

project_dir = '/home/dyvasey/hawksey/UCD Box/UC Davis/Manuscripts/RiftInversion_Geology/python_figs/initial_analytical.pdf'
fig.savefig(project_dir)   
