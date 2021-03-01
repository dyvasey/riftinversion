"""
Module to propagate base rift inversion .prm files to different parameters
"""

import os

import numpy as np
import pandas as pd

def lthickness(text,lthick):
    """
    Replace thermal values and other parameters to alter lithosphere thickness
    
    Parameters:
        text: String of prm base file to alter
        lthick: Lithosphere thickness (km)
    
    Returns:
        text: Altered prm string
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
    text = text.replace('x>XXX','x>'+str(lthick)+'.e3')
    
    return(text)

def evelocity(text,evel):
    """
    Add extension velocity
    
    Parameters:
        text: String of prm base file to alter
        evel: Total extension velocity (cm)
    
    Returns:
        text: Altered prm string
    """
        
    # Convert total velocity in cm/yr to half velocity in m/yr
    v = (evel/2)/100
    
    base = 'XXX' # Dummy value in in base file
     
    old = 'v='+base
    new = 'v='+str(v)
    text = text.replace(old,new)
    
    return(text)

def time(text,time):
    """
    Add time values
    
    Parameters:
        text: String of prm base file to alter
        evel: Time to run model (Myr)
    
    Returns:
        text: Altered prm string
    """
    
    base = 'XXX' # Dummy value in in base file
    
    old = 'set End time                                   = '+base
    new = 'set End time                                   = '+str(time)+'e6'
    text = text.replace(old,new)
    
    return(text)

def version(text,ver):
    """
    Add version letter to Stampede2 job name.
    
    Parameters:
        text: String of sh file to alter
        ver: Letter to add to job name
    
    Returns:
        text: Altered sh string
    """
    old = 'SBATCH -J riftinv'
    new = 'SBATCH -J riftinv'+ver
    text = text.replace(old,new)    
    return(text)

def generate(file='ri_base.prm',lthick=100,evel=1,etime=50,output='.',
             shell='run_base.sh',ver=''):
    """
    Generate .prm file from dummy base file.
    
    Can be used to generate discrete extension, quiescence, or convergence
    file. For quiescence, set evel = 0. For convergence, set evel to a 
    negative number.
    
    Parameters:
        file: Path to prm base file to alter
        lthick: Lithosphere thickness (km)
        evel: Total extension velocity (cm)
        etime: Total model time (Myr)
        output: Directory to place generated file
        shell: Name of base shell script for Stampede2 to generate
        version: Version letter to add to Stampede2 job name
    
    Returns:
        None
    """
    lthick_str = str(lthick)+'km' # String version of thickness  
    vel_str = str(evel)+'cm' # String version of velocity
    vel_str = vel_str.replace('.','-') # Make sure no decimals
    time_str = str(etime)+'Myr' # String version of time
    
    fullstring = vel_str+'_'+lthick_str+'_'+time_str
    
    path = os.path.join('.',file) # Join root to filename
    newname = file.replace('base',fullstring) # Change file name
    
    with open(path) as f_prm: # Open the file
        contents = f_prm.read() # Read file into string
        contents = lthickness(contents,lthick)
        contents = evelocity(contents,evel)
        contents = time(contents,etime)
        if 'XXX' in contents:
            print('WARNING: PRM generated contains XXX') 
        newpath = os.path.join(output,newname)
        newfile = open(newpath,"w",newline='\n')
        newfile.writelines(contents)
        newfile.close()
    
    # Generate run.sh for Stampede2
    spath = os.path.join('.',shell)
    with open(spath) as f_sh: # Open the file
        contents = f_sh.read() # Read file into string
        contents = contents.replace('XXX',newname)
        contents = version(contents,ver)
        if 'XXX' in contents:
            print('WARNING: .sh generated contains XXX')
        new_spath = os.path.join(output,'run'+ver+'.sh')
        newfile = open(new_spath,"w",newline='\n')
        newfile.writelines(contents)
        newfile.close()
    return
    