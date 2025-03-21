"""
Module to propagate base rift inversion .prm files to different parameters
"""

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def lthickness(text,lthick,depth=600):
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
    csv = 'thermal_' + str(lthick) + '_' + str(depth) + '.csv'
    thermal = pd.read_csv(csv,index_col=0).squeeze().to_dict()
    
    base = 'XXX' # Dummy value in in base file
    
    params = ['ts1','ts2','ts3','ts4','qs1','qs2','qs3']

    # Replace thermal parameters
    for param in params:
        old = param+'='+base
        new = param+'='+str(round(thermal[param],5))
        text = text.replace(old,new)
    
    # Replace bottom temperature
    bottom_old = 'set Bottom temperature = XXX'
    bottom_new = 'set Bottom temperature = ' + str(round(thermal['base'],None))
    text = text.replace(bottom_old,bottom_new)
    
    # Replace Adiabatic function expression
    text = text.replace('x>XXX','x>'+str(lthick)+'.e3')
    
    # Replace temperature function expression
    text = text.replace('(h-y)<=XXX','(h-y)<='+str(lthick)+'.e3')

    # Replace AMR values
    amr_vals = pd.read_csv('amr_temps.csv',index_col=0).squeeze().to_dict()
    amr_150 = str(int(amr_vals['t150_'+str(lthick)]))
    amr_250 = str(int(amr_vals['t250_'+str(lthick)]))
    old = '    set Isosurfaces = 2,2,  Temperature: 273|XXX; 1,1, Temperature: XXX|XXX'
    new = '    set Isosurfaces = 2,2,  Temperature: 273|' + amr_150 + '; 1,1, Temperature: ' + amr_150 + '|' + amr_250
    text = text.replace(old,new)
    
    return(text)

def evelocity(text,evel,p1=400e3,p2=200e3,quiescence=False,v1=None,v2=None,start=None,end=None):
    """
    Add extension velocity
    
    Parameters:
        text: String of prm base file to alter
        evel: Total extension velocity (cm)
    
    Returns:
        text: Altered prm string
    """
    base = 'XXX' # Dummy value in in base file
    
    if quiescence==False:
        # Convert total velocity in cm/yr to half velocity in m/yr
        v = (evel/2)/100
        
        # Get slope based on extension velocity and transition to outflow depth
        s = (v*2)/(p2-p1)
        
        old = 'v='+base
        new = 'v='+str(v)
        text = text.replace(old,new)
        
        old = 's='+base
        new = 's='+str(s)
        text = text.replace(old,new)

    elif quiescence==True:
        v1_half = (v1/2)/100
        old = 'v1='+base
        new = 'v1='+str(v1_half)
        text = text.replace(old,new)

        v2_half = (v2/2)/100
        old = 'v2='+base
        new = 'v2='+str(v2_half)
        text = text.replace(old,new)

        s1 = (v1_half*2)/(p2-p1)
        old = 's1='+base
        new = 's1='+str(s1)
        text = text.replace(old,new)

        s2 = (v2_half*2)/(p2-p1)
        old = 's2='+base
        new = 's2='+str(s2)
        text = text.replace(old,new)

        t1 = start*1e6 + 1e6
        old = 't1='+base
        new = 't1='+str(t1)
        text = text.replace(old,new)

        t2 = end*1e6 - 1e6
        old = 't2='+base
        new = 't2='+str(t2)
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
    
    base = 'XXX' # Dummy value in base file
    
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

def strain_softening(text,value):
    """
    Set value for strain softening.
    """
    
    base = 'XXX' # Dummy value in base file
    
    # Cohesion
    old_cohesion = 'set Cohesion strain weakening factors            = '+base
    new_cohesion = 'set Cohesion strain weakening factors            = '+str(value)
    
    text = text.replace(old_cohesion,new_cohesion)
    
    # Friction
    old_friction = 'set Friction strain weakening factors            = '+base
    new_friction = 'set Friction strain weakening factors            = '+str(value)
    
    text = text.replace(old_friction,new_friction)
    
    return(text)
    
def generate(file='ri_base.prm',lthick=100,depth=600,evel=1,etime=50,soft=0.375,
             p1=400,p2=200,output='.',
             shell='run_base.sh',ver='',nodes=1,
             quiescence=False,v1=None,v2=None,start=None,end=None):
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
        soft: Strain softening factor
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
    time_str = time_str.replace('.','-') # Make sure no decimals
    soft_str = str(round(soft*30))
    soft_str = soft_str.replace('.','-')
    
    fullstring = vel_str+'_'+lthick_str+'_'+time_str+'_'+soft_str
    
    path = os.path.join('.',file) # Join root to filename
    newname = file.replace('base',fullstring) # Change file name
    
    p1_m = p1*1e3
    p2_m = p2*1e3
    
    if os.path.exists(output)==False:
        os.makedirs(output)
    
    with open(path) as f_prm: # Open the file
        contents = f_prm.read() # Read file into string
        contents = lthickness(contents,lthick,depth)
        contents = evelocity(contents,evel,p1_m,p2_m,
            quiescence,v1,v2,start,end=etime)
        contents = time(contents,etime)
        contents = strain_softening(contents,soft)
        if 'XXX' in contents:
            print('WARNING: PRM generated contains XXX') 
        newpath = os.path.join(output,newname)
        newfile = open(newpath,"w",newline='\n')
        newfile.writelines(contents)
        newfile.close()
    
    # Generate run.sh
    spath = os.path.join('.',shell)
    with open(spath) as f_sh: # Open the file
        contents = f_sh.read() # Read file into string
        contents = contents.replace('$ASP XXX','$ASP '+newname)
        contents = contents.replace('log_XXX','log_ri_'+fullstring)
        contents = contents.replace('-N XXX','-N '+str(nodes))
        contents = contents.replace('-n XXX','-n '+str(nodes*64))
        contents = contents.replace('$ASPDIR/build/./aspect ./XXX','$ASPDIR/build/./aspect ./'+newname)
        contents = version(contents,ver)
        if 'XXX' in contents:
            print('WARNING: .sh generated contains XXX')
        new_spath = os.path.join(output,'run.sh')
        newfile = open(new_spath,"w",newline='\n')
        newfile.writelines(contents)
        newfile.close()
    return

def comp_ascii(thicknesses=[20,20,60],width=1000,depth=400,resolution=2,
               rmin=0.5,rmax=1.5,strain_width=250,strain_depth=60,
               seed=25,plot=True,
               cfix=True,wela=False,non_initial=False,output='.'):
    """
    Create composition ASCII file after Naliboff script for ASPECT model
    
    Parameters:
        thicknesses: Thicknesses of upper crust, lower crust, and mantle
            lithosphere in km.
        x: Length of model (km)
        y: Depth of model (km)
        resolution: Grid resolution (km)
        rmin: Minimum random strain
        rmax: Maximum random strain
        strain_width: Width of zone of plastic strain (km)
        strain_depth: Depth of zone of plastic strain (km)
        plot: Whether to plot model setup
        cfix: Not sure what this does
        wela: Whether to add 3 additional fields for viscoelastic stresses.
        non_initial: Whether to add additional field for non-initial plastic
            strain.
            
    Returns:
        None.
    """
    km2m = 1000
    
    xmin    = 0
    xmax    = width*km2m
    ymin    = 0
    ymax    = depth*km2m
    
    gres = resolution*km2m
    
    # Plastic strain
    ep_width = strain_width*km2m
    ep_depth = strain_depth*km2m
    xmin_ep = (xmax/2)-(ep_width/2)
    xmax_ep = (xmax/2)+(ep_width/2)
    ymax_ep = ymax
    ymin_ep = ymax-ep_depth
    
    # Compositonal layers
    ymin_cu = ymax - thicknesses[0]*km2m
    ymin_cl = ymin_cu - thicknesses[1]*km2m
    ymin_ml = ymin_cl - thicknesses[2]*km2m
    
    # Setup of 2D spatial grid
    xpts = int((xmax - xmin)/gres) + 1
    ypts = int((ymax - ymin)/gres) + 1
    #
    x = np.linspace(xmin,xmax,xpts)
    y = np.linspace(ymin,ymax,ypts)
    #
    xx, yy = np.meshgrid(x,y,indexing='ij')
    
    # Array for randomized plastic strain and viscous strain
    ep = np.zeros([xpts,ypts])
    
    # Set random seed
    np.random.seed(seed)
    
    # Make box of random strain with y values based on ep depth
    ep_ypts = int((ymax_ep-ymin_ep)/gres) + 1
    rn = np.random.rand(xpts,ep_ypts)
    
    # Open outfile for composition data
    path = os.path.join(output,'composition.txt')
    outfile=open(path,'w')
    outfile.write('# RANDOM SEED = %i\n'% (seed))
    outfile.write('# POINTS: %-i %i\n'% (x.size,y.size))
    
    # Loop through grid points
    for i in range(y.size):
    
      for j in range(x.size):
    
          # Randomized plastic strain is non-zero only in specified regions
          if x[j]>xmin_ep and x[j]<xmax_ep and y[i]>ymin_ep and y[i]<ymax_ep:
              
            if cfix == True:
              
              # Invert i indices for processing ep
              i_inverted = ypts-i
              
              if (rn[j,i_inverted] < 0.5):
                ep[j,i] = rmin
              else:
                ep[j,i] = rmax
            
            else:
              ep[j,i] = rmin + (rn[j,i_inverted] * (rmax - rmin))
          
          # Write spatial coordinates
          outfile.write('%-8.3e  ' % (x[j]))
          outfile.write('%-8.3e  ' % (y[i]))
    
          # Write elastic stresses
          if wela == True:
              outfile.write('%6.4f  ' % (0.0))
              outfile.write('%6.4f  ' % (0.0))
              outfile.write('%6.4f  ' % (0.0))
         
          # Write plastic strain values
          outfile.write('%6.4f  ' % (ep[j,i]))

          # Write noninitial plastic strain values
          if non_initial == True:
            outfile.write('%6.4f  ' % (0.0))
              
          # Write upper crust values
          if y[i]>ymin_cu:
            outfile.write('%6.4f  ' % (1.0))
          else:
            outfile.write('%6.4f  ' % (0.0))
          
          # Write lower crust values
          if y[i]<=ymin_cu and y[i]>ymin_cl:
            outfile.write('%6.4f  ' % (1.0))
          else:
            outfile.write('%6.4f  ' % (0.0))
    
          # Write lithospheric mantle values
          if y[i]<=ymin_cl and y[i]>ymin_ml:
            outfile.write('%6.4f  \n' % (1.0))
          else:
            outfile.write('%6.4f  \n' % (0.0))
    
    # Close outfile
    outfile.close()
    
    # Plot random plastic strain
    if plot == True:
      # Plastic strain
      fig, ax = plt.subplots()
      ax.set_aspect('equal')
      ax.set_title('Initial Plastic Strain', fontsize=14)
      ax.set_xlim(xmin/1.e3,xmax/1.e3)
      ax.set_ylim(ymin/1.e3,ymax/1.e3)
      ax.set_xlabel('Horizontal Position (km)')
      ax.set_ylabel('Height (km)')
      ctf = ax.contourf(xx[:,:]/1.e3,yy[:,:]/1.e3,ep[:,:])
      fig.colorbar(ctf)
      
    return(xx,yy,ep)
    
    
    