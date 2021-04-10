# -*- coding: utf-8 -*-
"""
Functions for plotting data from Paraview
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv

def byerlee(density,depth):
    """
    Calculate failure criterion from density and depth using Byerlee's Law.

    Parameters
    ----------
    density: Density of material (kg/m^3)
    depth : Depth of material (m)      

    Returns
    -------
    tau : Shear stress (Pa)

    """
    
    g = 9.81 # m/s^2
    lith_stress = density*g*depth # Pa (kg/m*s^2)
    tau = 0.85*lith_stress.where(lith_stress<=200e6) # Pa
    tau2 = 0.6*lith_stress.where(lith_stress>200e6)+60e6 # Pa
    tau.update(tau2)
    
    return(tau)

def strength_profile(data,strain_rate=1e-15,ax=None,**kwargs):
    """
    Plot strength profile from Paraview CSV.

    Parameters
    ----------
    data : DataFrame containing density, viscosity, temperature data 
    strain_rate : Strain rate in s^-1. The default is 1e-15.
    ax : Axes on which to plot the profile. The default is None.

    Returns
    -------
    ax : Axes with strain profile plotted

    """
    if ax==None:
        ax=plt.gca()
    
    # Get key variables
    depth = abs(data['Points:1']-200000) # m
    visc = data['viscosity']

    density = data['density']
    temperature = data['T']
    
    tau = byerlee(density,depth)
    
    viscous_strength = 2*visc*strain_rate
    
    max_strength = np.minimum(tau,viscous_strength)
    
    ax.plot(max_strength/1e6,depth/1000,**kwargs)
    
    ax.set_ylim(depth[0]/1000,0)
    ax.set_xlim(0,max_strength.max()/1e6+100)
    ax.set_xlabel('Differential Stress (MPa)')
    ax.set_ylabel('Depth (km)')
    
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    return(ax)

def temperature(data,ax=None,**kwargs):
    """
    Plot temperature profile from Paraview CSV.

    Parameters
    ----------
    data : DataFrame containing temperature data 
    ax : Axes on which to plot the profile. The default is None.

    Returns
    -------
    ax : Axes with temperature profile plotted

    """
    if ax==None:
        ax=plt.gca()
    
    temp = data['T']
    depth = abs(data['Points:1']-200000) # km
    
    ax.plot(temp,depth/1000,**kwargs)
    ax.set_ylim(depth[0]/1000,0)
    ax.set_xlim(0,temp.iloc[0]+100)
    ax.set_xlabel('Temperature (K)')
    ax.set_ylabel('Depth (km)')
    
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    return(ax)

def grid(data,ax=None,field='density',**kwargs):
    """
    Plot grid from Paraview CSV using Matplotlib tricontourf.

    Parameters
    ----------
    data : DataFrame of Paraview CSV data
    ax : Axes on which to plot the grid. The default is None.
    field : ParaView field to use to color the grid. The default is 'density'.

    Returns
    -------
    ax : Axes with grid plotted.

    """
    if ax==None:
        ax=plt.gca()
    
    if field=='comp_field':
        data['comp_field'] = comp_field(data)
    
    ax.tricontourf(data['Points:0']/1000,data['Points:1']/1000,data[field],
                   **kwargs)
    ax.set_aspect('equal', adjustable='box')
    ax.spines["top"].set_visible(False)
    return(ax)

def comp_field(df,fields=['crust_upper','crust_lower','mantle_lithosphere'],
               null_field='asthenosphere'):
    """
    Create compositional field category for Paraview plotting.
    
    Uses input fields to assign value based on when fields are >0.9. Any point
    lacking a field >0.9 is assigned to the null field.

    Parameters
    ----------
    df : DataFrame with field information.
    fields : Names of compositional fields to use. The default is 
        ['crust_upper','crust_lower','mantle_lithosphere'].
    null_field : Name of field to assign all values <0.9 for each field.
        The default is 'asthenosphere'.

    Returns
    -------
    output : Series with compositional field values.

    """

    output = pd.Series(np.nan,index=df.index)
    for x in range(len(fields)):
        output.mask(df[fields[x]]>0.5,x+1,inplace=True)
    output.mask(output.isna(),0,inplace=True)
    return(output)

def cmyk2rgb(cmyk):
    """
    " Convert CMYK colors to RGB"

    Parameters
    ----------
    cmyk : List or tuple of colors as C,M,Y,K

    Returns
    -------
    rgb : Tuple of colors as R,G,B

    """
    r = (1-cmyk[0]/100)*(1-cmyk[3]/100)
    g = (1-cmyk[1]/100)*(1-cmyk[3]/100)
    b = (1-cmyk[2]/100)*(1-cmyk[3]/100)
    rgb = (r,g,b)
    return(rgb)

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
    
    

