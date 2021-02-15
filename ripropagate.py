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

def evelocity(text,evel):
    """
    Add extension velocity
    """
        
    # Convert total velocity in cm/yr to half velocity in m/yr
    v = (evel/2)/100
    
    base = 'XXX' # Dummy value in in base file
     
    old = 'v='+base
    new = 'v='+str(v)
    text = text.replace(old,new)
    
    return(text)

def generate(file='ri_base.prm',output='.',lthick=100,evel=1):
    """
    Generate .prm file from dummy base file. Thickness only.
    """
    lthick_str = str(lthick)+'km' # String version of thickness  
    vel_str = str(evel)+'cm' # String version of velocity
    vel_str = vel_str.replace('.','-') # Make sure no decimals
    
    fullstring = vel_str+'_'+lthick_str
    
    path = os.path.join('.',file) # Join root to filename
    newname = file.replace('base',fullstring) # Change file name
    
    with open(path) as f_prm: # Open the file
        contents = f_prm.read() # Read file into string
        contents = lthickness(contents,lthick)
        contents = evelocity(contents,evel)
        if 'XXX' in contents:
            print('WARNING: PRM generated contains XXX') 
        newpath = os.path.join(output,newname)
        newfile = open(newpath,"w")
        newfile.writelines(contents)
        newfile.close()


    