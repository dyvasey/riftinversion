"""
Script to forward model AHe for production models in Geology Manuscript
"""
import os
import shutil

import tracemalloc
import linecache

import numpy as np
import pyvista as pv

from riftinversion import vtk_plot as vp

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

#%%
# Compile all directory locations
models_slow = ['063022_rip_c','071822_rip_b','070422_rip_e','072022_rip_a',
          '070422_rip_c','071322_rip','070622_rip_a','072022_rip_b']

models_fast = ['080122_rip_a','080122_rip_e','080122_rip_b','080122_rip_f',
          '080122_rip_c','080122_rip_g','080122_rip_d','080122_rip_h']

all_models = models_slow + models_fast

# Names for output files

names = ['M01-slow_cold_half','M02-slow_cold_half_qui', 'M03-slow_cold_full',
         'M04-slow_cold_full_qui','M05-hot_fast_half','M06-hot_fast_half_qui',
         'M07-hot_fast_full','M08-hot_fast_full_qui',
         'M09-slow_cold_half_fastinvert','M10-slow_cold_half_qui_fastinvert',
         'M11-slow_cold_full_fastinvert','M12-slow_cold_full_qui_fastinvert',
         'M13-hot_fast_half_fastinvert','M14-hot_fast_half_qui_fastinvert',
         'M15-hot_fast_full_fastinvert','M16-hot_fast_full_qui_fastinvert']

model_step = 0.1

tchron_interval = 0.1
tchron_yrs = tchron_interval*1e6

bounds=[325,675,580,620,0,0]

# Rift times post-cooling for both slow and fast sets
rift_times = [16,36,32,52,7.3,27.3,14.5,34.5]
rift_times_all = [16,36,32,52,7.3,27.3,14.5,34.5]*2

invert_times_slow = [x+20 for x in rift_times]
invert_times_fast = [x+4 for x in rift_times]

# Manual input of models that didn't fully finish
invert_times_fast[0] = 19.4
invert_times_fast[1] = 39.5

invert_times_all = invert_times_slow + invert_times_fast

# Directory for new meshes
output_prefix = 'He_meshes/'

overwrite = False
processes=4

if overwrite==True:
    try:
        shutil.rmtree(output_prefix)
    except:
        print("Creating new base directory...")
    else:
        print("Cleared existing base directory...")

# Loop through each model
for x,model in enumerate(all_models):  
    
    print('Processing ' + model + '...')
    
    # Get model files
    base_dir = r'/mnt/f44f06b4-89ef-4d7c-a41d-6dbf331c8d4e/riftinversion_production/'
    suffix = r'/output_ri_rift/particles'
    
    directory = base_dir + model + suffix
    time_total = invert_times_all[x]  
    
    nsteps = int(time_total/model_step)
    rift_step = int(rift_times_all[x]/model_step)
    
    timesteps = np.arange(rift_step,nsteps+1,int(tchron_interval/model_step))
    
    # Clip and store meshes
    folder_meshes = 'clipped_meshes'
    output_dir = output_prefix + model
    os.makedirs(output_dir,exist_ok=True)
    filename = os.path.join(output_dir,folder_meshes+'.vtm')
    
    if overwrite==False:
        if os.path.exists(filename):
            print('Processing Existing Clipped Meshes...')
        else:
            print('No Existing Clipped Meshes...')
            print('Creating New Clipped Meshes...')
            vp.load_particle_meshes(directory,timesteps,
                                             bounds=bounds,filename=filename,
                                             parallel=True,processes=processes)
    
    elif overwrite==True:
        print('Creating New Clipped Meshes...')
        vp.load_particle_meshes(directory,timesteps,
                                         bounds=bounds,filename=filename,
                                         parallel=True,processes=processes)
    
    # Calculate AHe
    folder_He = os.path.join(output_dir,'meshes_He')
    os.makedirs(folder_He,exist_ok=True)
    
    mesh_dir = os.path.join(output_dir,folder_meshes)
    mesh_files = os.listdir(mesh_dir)
    ints = np.arange(0,len(mesh_files),1)
    files = [os.path.join(mesh_dir,folder_meshes +'_'+str(integer)+'.vtu') for integer in ints]
    
    tracemalloc.start()
    
    if overwrite==False:
        if len(os.listdir(folder_He))==len(files):
            print('Skipping AHe Calculation...')
       
        else:
            print('No Existing AHe Meshes...')
            print('Writing AHe Meshes...')
            try:
                vp.He_age_vtk_parallel(files,'AHe',tchron_yrs,batch_size='auto',
                                                     processes=processes,
                                                     path=output_dir)
            except:
                snapshot = tracemalloc.take_snapshot()
                display_top(snapshot)
                tracemalloc.stop()
                raise
            
    elif overwrite==True:
        print('Writing AHe Meshes...')
        vp.He_age_vtk_parallel(files,'AHe',tchron_yrs,batch_size='auto',
                                                 processes=processes,
                                                 path=output_dir)





