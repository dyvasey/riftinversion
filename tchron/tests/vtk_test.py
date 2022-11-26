"""
Test for forward modeling of ASPECT output, using cookbook output
"""

#%% Import and setup files
import os
import tracemalloc
import linecache

import matplotlib.pyplot as plt
from matplotlib import cm,colors

import numpy as np

import pyvista as pv

import vtk_plot as vp

# Read in sample data from continental extension cookbook
files_dir = '../../sample_data/vtk_tchron_test/'
files_all = os.listdir(files_dir)
ints = np.arange(0,len(files_all),1)
files = [os.path.join(files_dir,'vtk_tchron_test_'+str(integer)+'.vtu') for integer in ints]

#%% Set up tracemalloc
def display_top(snapshot, key_type='lineno', limit=10):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        print("#%s: %s:%s: %.1f KiB"
              % (index, frame.filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))

#%% Add He ages to final mesh and save
tracemalloc.start()

He_mesh = vp.He_age_vtk_parallel(files,'AHe',1e5,batch_size=100,
                                 interpolate_profile=False,file_prefix='meshes_He')
He_mesh_interp = vp.He_age_vtk_parallel(files,'AHe',1e5,batch_size=100,
                                        interpolate_profile=True,file_prefix='meshes_He_interp')

print(tracemalloc.get_traced_memory())

snapshot = tracemalloc.take_snapshot()
display_top(snapshot)

tracemalloc.stop()

#%% Plot the new mesh

fig,axs = plt.subplots(2,dpi=300)

vp.plot2D('meshes_He/meshes_He_20.vtu','AHe',bounds=[0,200,90,100],cmap='plasma_r',ax=axs[0],
          clim=[0,2])

vp.plot2D('meshes_He_interp/meshes_He_interp_20.vtu','AHe',bounds=[0,200,90,100],cmap='plasma_r',ax=axs[1],
          clim=[0,2])

cbar = vp.add_colorbar(fig,0,2,'plasma_r',label='AHe Age',ticks=[0,1,2])

fig.savefig('vtk_tchron_test.pdf')

