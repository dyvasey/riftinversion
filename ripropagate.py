"""
Module to propagate base rift inversion .prm files to different parameters
"""

import os
import re

import numpy as np
import pandas as pd

def lthickness(text,lthick):
    """
    Replace thermal values and other parameters to alter lithospheric thickness
    """
    
    # Read in thermal values from csv
    thick_str = str(lthick)+'km' # String version of thickness  
    csv = 'thermal_'+thick_str+'.csv'
    thermal = pd.read_csv(csv,index_col=0).squeeze().to_dict()
    
    base = 'XXX' # Dummy value in in base file
    
    params = ['ts1','ts2','ts3','ts4','qs1','qs2','qs3']

    # Replace thermal parameters
    for param in params:
        old = param+'='+base
        new = param+'='+str(round(thermal[param],5))
        text = text.replace(old,new)
    
    # Replace Adiabatic function expression
    text = text.replace('x>XXX','X>'+str(lthick)+'.e3')
    
    return(text)

def evelocity(vel,directory,base=1):
    """
    Convert base .prm file to new extension velocity.
    """
    vel_str = str(vel)+'cm' # String version of velocity
    vel_str = vel_str.replace('.','-') # Make sure no decimals

    os.makedirs(directory,exist_ok=True) # Make new directory
    
    
    # Convert total velocity in cm/yr to half velocity in m/yr
    v = (vel/2)/100
    v_base = (base/2)/100 
    
    for file in os.listdir('.'):
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
         
        newpath = os.path.join(directory,newfilename) # Create new path
        newfile = open(newpath,"w")
        newfile.writelines(copy)
        newfile.close()
    return(copy)

def generate(file,output='.',lthick=100):
    """
    Generate .prm file from dummy base file. Thickness only.
    """
    lthick_str = str(lthick)+'km' # String version of thickness  
    
    path = os.path.join('.',file) # Join root to filename
    newname = file.replace('base',lthick_str) # Change file name
    
    with open(path) as f_prm: # Open the file
        contents = f_prm.read() # Read file into string
        contents = lthickness(contents,lthick)
        newpath = os.path.join(output,newname)
        newfile = open(newpath,"w")
        newfile.writelines(contents)
        newfile.close()


    