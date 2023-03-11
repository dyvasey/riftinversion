"""
Script to do strain analysis on initial rift inversion models
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import mpltern
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

bounds = [300,700,400,620]

# Plot to see strain distribution
field = 'noninitial_plastic_strain'

# Create dataframe for final values
final = pd.DataFrame([],columns=['Localization','Symmetry','C-ness'])

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
    x_rounded = np.round(x,-2)
    
    # Pull strains and x positions into dataframe
    strains = mesh[field]
    df = pd.DataFrame([x_rounded,strains]).T
    df.columns = ['X','Strain']
    
    # Sum strains along same x and clip
    strains_summed = df.groupby('X').sum()
    strains_summed_clipped = strains_summed[3e5:7e5+1]
    
    # Isolate x values (km) and strains
    x_values = strains_summed_clipped.index/1000
    y_values = strains_summed_clipped['Strain']
    
    # Use filter to smooth strains
    y_smoothed = savgol_filter(y_values,25,polyorder=3)
    
    # Normalized smoothed strain using maximum strain value
    y_normalized = y_smoothed/np.max(y_smoothed)
    
    peaks = find_peaks(y_normalized,height=0.9,prominence=0.1,rel_height=0.9)
    peak_indices = peaks[0]
    x_peaks = x_values[peak_indices]
    heights = peaks[1]['peak_heights']
    
    widths,width_heights,left_ips,right_ips = peak_widths(y_normalized,peak_indices,
                                                          rel_height=0.9)
    min_x_peaks = x_values[left_ips.astype(int)]
    max_x_peaks = x_values[right_ips.astype(int)]
    
    widths_x = max_x_peaks-min_x_peaks
    
    widths_norm = np.array(widths_x).sum()/400
    
    localization = 1-widths_norm
    final.loc[k+1,'Localization'] = localization
    
    areas = np.array([])
    left_areas = np.array([])
    right_areas = np.array([])
    for n,peak in enumerate(x_peaks):
        
        y_limited = y_normalized[left_ips.astype(int)[n]:right_ips.astype(int)[n]]
        area = np.trapz(y_limited)
        areas = np.append(areas,area)
        
        y_left = y_normalized[:peak_indices[n]]
        y_right = y_normalized[peak_indices[n]:]
        
        left_area = np.trapz(y_left)
        right_area = np.trapz(y_right)
        left_areas = np.append(left_areas,left_area)
        right_areas = np.append(right_areas,right_area)   
        
    
    total_area = np.trapz(y_normalized)
    
    symmetry = left_areas/right_areas
    symmetry_corrected = np.reciprocal(symmetry,out=symmetry,where=(symmetry>1))
    final.loc[k+1,'Symmetry'] = symmetry_corrected
    
    cness = symmetry_corrected*localization
    final.loc[k+1,'C-ness'] = cness
    
    area_ratio = np.sum(areas)/total_area
    hw_ratio = heights/widths_x
    print('\nModel ',k+1)
    print('Area ratio: ',area_ratio)
    print('Heights: ',heights)
    print('Widths: ',widths_norm)
    print('Height/width ratios: ',np.array(hw_ratio))
    print('Left Areas: ',left_areas)
    print('Right Areas: ',right_areas)
    print('Symmetry: ',symmetry_corrected)
    
    fig,axs = plt.subplots(4,figsize=(8.5,11),dpi=300)
    vp.plot2D(file,field,bounds,ax=axs[0])
    axs[1].plot(x_values,y_values)
    
    axs[2].plot(x_values,y_normalized)
    axs[2].scatter(x_peaks,heights,c='red')
    axs[2].hlines(y=width_heights,xmin=min_x_peaks,xmax=max_x_peaks,color='red')
    
    axs[3].scatter(x_peaks,symmetry_corrected)
    axs[3].set_xlim(300,700)
    axs[3].set_ylim(0,1)
    
    plt.tight_layout()
    
fig,ax = plt.subplots(1)

for k,row in final.iterrows():
    ax.scatter(row['Localization'],row['Symmetry'],label=k)
    ax.annotate(k,(row['Localization'],row['Symmetry']))
    
ax.legend()
ax.set_xlabel('Localization')
ax.set_ylabel('Symmetry')

fig,ax = plt.subplots(1,subplot_kw={'projection': 'ternary'})

cness_zeroed = final['C-ness']-final['C-ness'].min()
cness_norm = cness_zeroed/cness_zeroed.max()

local_zeroed = final['Localization']-final['Localization'].min()
local_norm = local_zeroed/local_zeroed.max()
bness = 1-local_norm

symm_zeroed = final['Symmetry']-final['Symmetry'].min()
symm_norm = symm_zeroed/symm_zeroed.max()
aness = 1-symm_norm

for k,row in final.iterrows():
    ax.scatter(cness_norm[k],aness[k],bness[k],label=k)
    ax.legend()