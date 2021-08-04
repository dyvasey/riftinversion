# -*- coding: utf-8 -*-
"""
Functions for plotting data from Paraview
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv

def plot(file,output,field='density',bounds=None,contours=True,
         cfields=['crust_upper','crust_lower','mantle_lithosphere'],
         null_field='asthenosphere',off_screen=True,
         camera=None,**kwargs):
    """
    Plot 2D ASPECT results using Pyvista.

    Parameters
    ----------
    file : VTU or PVTU file to plot
    output : Name of image file to output screenshot
    field : Field to use for color. The default is 'density'.
    bounds : Bounds by which to clip the plot. The default is None.
    contours : Boolean for whether to add temperature contours. 
        The default is True.
    cfields : Names of compositional fields to use if field is 'comp_field.' 
        The default is ['crust_upper','crust_lower','mantle_lithosphere'].
    null_field : Null field if field is 'comp_field.'
        The default is 'asthenosphere'.
    off_screen : Boolean for whether Pyvista plotting occurs off-screen.
        The default is True.
    camera : Position for Pyvista camera. The default is None.

    Returns
    -------
    img : img object that can be saved or plotted.

    """
    
    mesh = pv.read(file)
    mesh = mesh.clip_box(bounds=bounds,invert=False)
    if field=='comp_field':
        mesh = comp_field_vtk(mesh,fields=cfields,null_field=null_field)
    
    if contours==True:
        cntrs = add_contours(mesh)
    
    pv.set_plot_theme("document")
    plotter = pv.Plotter(off_screen=off_screen)
    
    plotter.add_mesh(mesh,scalars=field,**kwargs)
    
    if contours ==True:
        plotter.add_mesh(cntrs,color='black',line_width=5)
    
    plotter.view_xy()
    plotter.remove_scalar_bar()

    plotter.window_size = 1200,660
    if camera is not None:
        plotter.camera_position = camera
        print('hey ya')
        plotter.camera_set = True
    if off_screen==False:
        cpos = plotter.show(screenshot='output')
        return(cpos)
    else:
        img = plotter.screenshot(output,transparent_background=True,
                             return_img=True)
        return(img)

def add_contours(mesh,field='T',values=np.arange(500,1700,200)):
    """
    Add contours to mesh in Pyvista.

    Parameters
    ----------
    mesh : Pyvista mesh object.
    field : Scalar in Pyvista mesh object to use for contours. The default is
        T.
    values : Values for the contours. The default is np.arange(500,1700,200).

    Returns
    -------
    cntrs: Pyvista mesh containing the contours.

    """
    contour_mesh = mesh.copy()
    cntrs = contour_mesh.contour(isosurfaces=values,scalars=field)
    return(cntrs)
    

def comp_field_vtk(mesh,fields=['crust_upper','crust_lower','mantle_lithosphere'],
               null_field='asthenosphere'):
    """
    Calculate compositional field from Pyvista VTK mesh.
    
    Uses input fields to assign value based on when fields are >0.9. Any point
    lacking a field >0.9 is assigned to the null field.

    Parameters
    ----------
    mesh : Pyvista mesh
    fields : Names of compositional fields that are scalars in the mesh.
        The default is ['crust_upper','crust_lower','mantle_lithosphere'].
    null_field : Name of field for points not included in compositional fields.
        The default is 'asthenosphere'.

    Returns
    -------
    mesh: Pyvista mesh with 'comp_field' added as a scalar.
    
    """

    # Create empty np array
    output = np.zeros(shape=mesh.point_arrays[fields[0]].shape)
    for x in range(len(fields)):
        array = mesh.point_arrays[fields[x]]
        output = np.where(array>0.5,x+1,output)
    
    mesh.point_arrays['comp_field'] = output
    return(mesh)

def particle_trace(directory,timesteps,point,y_field,x_field='time',
                   plot_path=False):
    """
    Get particle paths over time from pvtu files
    """
    # Set up directory building blocks
    main = directory
    prefix = 'particles-00'
    suffix = '.pvtu'
    
    # Get file paths for all timesteps
    timesteps_str = [str(x).zfill(3) for x in timesteps.tolist()]
    files = [main+'/'+prefix+x+suffix for x in timesteps_str]
    
    x_point = []
    y_point = []
    
    # Loop over files
    for n in range(len(files)):
        mesh = pv.read(files[n]) # Get mesh
        ids = pv.point_array(mesh,'id') # Get particle ids
        y_vals = pv.point_array(mesh,y_field) # Get y field values
        
        # Get x field values if not plotting timesteps
        if x_field!='time':
            x_vals = pv.point_array(mesh,x_field)
            df = pd.DataFrame(
                {x_field:x_vals,y_field:y_vals},index=ids.astype(int))
        else:
            df = pd.DataFrame({y_field:y_vals},index=ids.astype(int))
        
        # Extract values for specific points and add to lists
        point_vals = df.loc[point,:]
        y = point_vals[y_field]
        if x_field!='time':
            x = point_vals[x_field]
            x_point.append(x)
        y_point.append(y)
        
    # Convert lists to dataframe
    if x_field!='time':
        point_df = pd.DataFrame({x_field:x_point,y_field:y_point},index=timesteps)
    else:
        point_df = pd.DataFrame({y_field:y_point},index=timesteps)
    
    if plot_path is True:
        if x_field!='time':
            point_df.plot(x_field,y_field)
            plt.xlabel(x_field)
            
            # Label timesteps
            for n in point_df.index:
                plt.text(x=point_df.loc[n,x_field],y=point_df.loc[n,y_field],
                     s=str(n))
        else:
            plt.plot(point_df.index,point_df[y_field])
            plt.xlabel('Timestep')
        plt.ylabel(y_field)
        plt.annotate('ID: '+str(point),xy=(0.1,0.9),xycoords='axes fraction')
        
        
    return(point_df)
        

