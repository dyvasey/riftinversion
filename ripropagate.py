"""
Module to propagate base rift inversion .prm files to different parameters
"""

import os
import re

import numpy as np
import pandas as pd

def thickness(thickness,directory,base=100):
    """
    Convert .prm file to new lithospheric thickness.
    """
    thick_str = str(thickness)+'km' # String version of thickness  
    os.makedirs(directory,exist_ok=True) # Make new directory
    
    csv = 'thermal_'+thick_str+'.csv'
    thermal = pd.read_csv(csv,index_col=0).squeeze().to_dict()
    
    base_thermal = pd.read_csv('thermal_'+str(base)+'km.csv',
                               index_col=0).squeeze().to_dict()
    
    params = ['ts1','ts2','ts3','ts4','qs1','qs2','qs3']
    
    for file in os.listdir("."):
        if file.endswith('100km_base.prm'): # Find the base .prm file
            filename = os.path.join(".",file) # Join root to filename
            # Get new file name for use later.
            newfilename = file.replace(str(base),str(thickness))

    with open(filename) as f_prm: # Open the file
        contents = f_prm.read() # Read file
        copy = contents
        for param in params:
            old = param+'='+str(round(base_thermal[param],5))
            new = param+'='+str(round(thermal[param],5))
            copy = copy.replace(old,new)
                    
        newpath = os.path.join(directory,newfilename) # Create new path
        newfile = open(newpath,"w")
        newfile.writelines(copy)
        newfile.close()
    return(copy)

def evelocity(vel,directory=".",base=1):
    """
    Convert base .prm file to new extension velocity.
    """
    vel_str = str(vel)+'cm' # String version of velocity
    vel_str = vel_str.replace('.','-') # Make sure no decimals
    newdir = directory+'/'+vel_str
    os.makedirs(newdir,exist_ok=True) # Make new directory
    
    
    # Convert total velocity in cm/yr to half velocity in m/yr
    v = (vel/2)/100
    v_base = (base/2)/100 
    
    for file in os.listdir(directory):
        if file.endswith('base.prm'): # Find the base .prm file
            filename = os.path.join(directory,file) # Join root to filename
            # Get new file name for use later.
            oldname = str(base)+'cm'
            newfilename = file.replace(oldname,vel_str)

    with open(filename) as f_prm: # Open the file
        contents = f_prm.read() # Read the file
        copy = contents
        old = 'v='+str(v_base)
        new = 'v='+str(v)
        copy = copy.replace(old,new)
         
        newpath = os.path.join(newdir,newfilename) # Create new path
        newfile = open(newpath,"w")
        newfile.writelines(copy)
        newfile.close()
    return(copy)
    