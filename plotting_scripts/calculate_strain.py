"""
Script to do strain analysis on initial rift inversion models
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.signal import savgol_filter,find_peaks,peak_widths
from tqdm import tqdm

import pyvista as pv
import vtk_plot as vp

# The following 8 models need to be plotted
# slow_cold_half 063022_rip_c
# slow_cold_half_qui 071822_rip_b
# slow_cold_full 070422_rip_e
# slow_cold_full_qui 072022_rip_a
# hot_fast_half 070422_rip_c
# hot_fast_half_qui 071322_rip
# hot_fast_full 070622_rip_a
# hot_fast_full_qui 072022_rip_b

# Make list of models with appropriate names
models = ['063022_rip_c','071822_rip_b','070422_rip_e','072022_rip_a',
          '070422_rip_c','071322_rip','070622_rip_a','072022_rip_b']

names = ['Model ' + str(x) for x in range(1,9)]

# Indicate time of final rift of reach model (post-cooling)

times = [16,36,32,52,7.3,27.3,14.5,34.5]
tstep_interval = 0.1

# Set up the figure

fig,axs = plt.subplots(4,2,dpi=300,figsize=(7,9.5))
bounds = [300,700,400,620]

# Plot to see strain distribution
field = 'noninitial_plastic_strain'

for k,model in enumerate(tqdm(models[0:])):
    # Get the appropriate pvtu file
    base_dir = r'/mnt/f44f06b4-89ef-4d7c-a41d-6dbf331c8d4e/riftinversion_production/'
    suffix = r'/output_ri_rift/solution'
    pvtu_dir = base_dir + model + suffix
    
    # Figure out appropriate timesteps
    tstep_invert = int((times[k]+20)/tstep_interval)
    
    # Pull the file locations
    file = vp.get_pvtu(pvtu_dir,tstep_invert)
    mesh = pv.read(file)

    # Get all strain values
    x = mesh.points[:,0]
    x_rounded = np.round(x,0)
    
    strains = mesh[field]
    df = pd.DataFrame([x_rounded,strains]).T
    df.columns = ['X','Strain']
    
    strains_summed = df.groupby('X').sum()
    strains_summed_clipped = strains_summed[3e5:7e5+1]
    
    x_values = strains_summed_clipped.index/1000
    y_values = strains_summed_clipped['Strain']
    
    y_smoothed = savgol_filter(y_values,100,polyorder=3)
    
    peaks = find_peaks(y_smoothed,height=50,prominence=10)
    peak_indices = peaks[0]
    x_peaks = x_values[peak_indices]
    heights = peaks[1]['peak_heights']
    
    widths,width_heights,left_ips,right_ips = peak_widths(y_smoothed,peak_indices)
    min_x_peaks = x_values[left_ips.astype(int)]
    max_x_peaks = x_values[right_ips.astype(int)]
    
    for n,peak in enumerate(x_peaks):
        
        y_limited = y_smoothed[left_ips.astype(int)[n]:right_ips.astype(int)[n]+1]
        area = np.trapz(y_limited)
        print(peak,area)
    
    total_area = np.trapz(y_smoothed)
    
    hw_ratio = heights/widths
    print(hw_ratio)
    
    fig,axs = plt.subplots(4,dpi=300)
    vp.plot2D(file,field,bounds,ax=axs[0])
    axs[1].plot(x_values,y_values)
    axs[2].plot(x_values,y_smoothed)
    axs[2].scatter(x_peaks,heights,c='red')
    axs[2].hlines(y=width_heights,xmin=min_x_peaks,xmax=max_x_peaks,color='red')
    axs[3].scatter(np.arange(0,len(hw_ratio)),hw_ratio)
    
    plt.tight_layout()