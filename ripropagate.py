"""
Module to propagate base rift inversion .prm files to different parameters
"""

import os
import re

import numpy as np
import pandas as pd

def thickness(thickness,directory=".",base=100):
    """
    Convert .prm file to new lithospheric thickness.
    """
    thick_str = str(thickness)+'km' # String version of thickness
    os.makedirs(thick_str,exist_ok=True) # Make new directory
    newdir = directory+'/'+thick_str
    
    csv = 'thermal_'+thick_str+'.csv'
    thermal = pd.read_csv(csv,index_col=0).squeeze().to_dict()
    
    base_thermal = pd.read_csv('thermal_'+str(base)+'km.csv',
                               index_col=0).squeeze().to_dict()
    
    params = ['ts1','ts2','ts3','ts4','qs1','qs2','qs3']
    
    for file in os.listdir(directory):
        if file.endswith('100km_base.prm'): # Find the base .prm file
            filename = os.path.join(directory,file) # Join root to filename
            # Get new file name for use later.
            newfilename = file.replace(str(base),str(thickness))

    with open(filename) as f_prm: # Open the file
        contents = f_prm.read() # Read file
        copy = contents
        for param in params:
            old = param+'='+str(round(base_thermal[param],5))
            new = param+'='+str(round(thermal[param],5))
            copy = copy.replace(old,new)
                    
        newpath = os.path.join(newdir,newfilename) # Create new path
        newfile = open(newpath,"w")
        newfile.writelines(copy)
        newfile.close()
    return(copy)

def evelocity(vel,directory=".",base=1):
    """
    Convert base .prm file to new extension velocity.
    """
    # Convert total velocity in cm/yr to half velocity in m/yr
    v = (vel/2)/100
    v_base = (base/2)/100 
    
    for file in os.listdir(directory):
        if file.endswith('base.prm'): # Find all the base .prm files
            filename = os.path.join(directory,file) # Join root to filename

            with open(filename) as f_prm: #open each file
                contents = f_prm.read() #read file as lines
                copy = contents
                old = 'v='+str(v_base)
                new = 'v='+str(v)
                copy = copy.replace(old,new)
            
                oldname = str(base)+'cm'
                newname = str(vel)+'cm'
                # Make sure no decimals in the new filename
                newname = newname.replace('.','-') 
                newfilename = filename.replace(oldname,newname)
                newfile = open(newfilename,"w")
                newfile.writelines(copy)
                newfile.close()
    return(copy)
    