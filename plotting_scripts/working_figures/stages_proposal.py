"""
Script to plot rift inversion evolution for NSF proposal on Blueschist
"""

import sys
sys.path.append('/home/dyvasey/git/riftinversion/')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pyvista as pv

from matplotlib import rc
rc("pdf", fonttype=42)

import vtk_plot as vp

pv.start_xvfb()
# slow_cold_half_qui 071822_rip_b

# Make list of models with appropriate names
model = '071822_rip_b'

# Indicate times for each model
t0 = 0
t1 = 16
t2 = 36
t3 = 56
tstep_interval = 0.1

# Set up the figure

fig,axs = plt.subplots(1,4,dpi=300,figsize=(6.5,3))
bounds = [300,700,400,620]

colors=['#66CCEE','#BBBBBB','#EE6677','#228833']
cm = ListedColormap(colors)

# Set opacity for strain
opacity_strain = [0,0.8,0.8,0.8,0.8]
lim_strain = [0,5]
cm_strain = 'inferno_r'

    
# Get the appropriate pvtu file
base_dir = r'/home/vaseylab/glaucophane/riftinversion_production/'
suffix = r'/output_ri_rift/solution'
    
pvtu_dir = base_dir + model + suffix
    
# Figure out appropriate timesteps
tstep_rift = int(t1/tstep_interval)
tstep_intermed = int(t2/tstep_interval)
tstep_final = int(t3/tstep_interval)
    
tsteps = np.array([t0,tstep_rift,tstep_intermed,tstep_final])
    
# Pull the file locations
files = vp.get_pvtu(pvtu_dir,tsteps)
    
# Plot

for k,ax in enumerate(axs):
    ax.tick_params(axis='both',labelsize=6)
    
    vp.plot2D(files[k],'comp_field',bounds=bounds,ax=ax,
                cmap=cm,contours=True)

    vp.plot2D(files[k],'noninitial_plastic_strain',bounds=bounds,ax=ax,
                cmap=cm_strain,opacity=opacity_strain,clim=lim_strain)

axs[0].set_title('Initial Conditions',fontsize=8)
axs[1].set_title('Rift',
                    fontsize=8)
axs[2].set_title('Post-Rift Cooling',
                    fontsize=8)
axs[3].set_title('Rift Inversion',
                    fontsize=8)
    
    
axs[0].set_xlabel('X Position (km)',fontsize=6)
axs[1].set_xlabel('X Position (km)',fontsize=6)
axs[2].set_xlabel('X Position (km)',fontsize=6)
axs[3].set_xlabel('X Position (km)',fontsize=6)

axs[0].set_ylabel('Y Position (km)',fontsize=6)
     
plt.tight_layout() 
    
fig.savefig('stages_proposal.pdf')  




