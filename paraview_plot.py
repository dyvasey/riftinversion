# -*- coding: utf-8 -*-
"""
Functions for plotting data from Paraview
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv

def byerlee(density,depth):
    # density kg/m^3
    # depth m
    
    g = 9.81 # m/s^2
    lith_stress = density*g*depth # Pa (kg/m*s^2)
    tau = 0.85*lith_stress.where(lith_stress<=200e6) # Pa
    tau2 = 0.6*lith_stress.where(lith_stress>200e6)+60e6 # Pa
    tau.update(tau2)
    
    return(tau)

def viscosity(temperature,pressure=0,strain_rate=0,flow_law='wet quartz'):
    """ Currently broken """
    if flow_law=='wet quartz':
        A = 8.57e-28 # prefactor
        n = 4.0 # stress exponent
        E = 223e3 # activation energy
        V = 0 # activation volume
    
    d = 0
    m = 0
    R = 8.314 # J/mol*K
    
    #visc = 0.5*A**(-1/n)*d**(m/n)*strain_rate
    visc_simple = A*np.exp(E/R*temperature)
    
    return(visc_simple)

def strength_profile(data,strain_rate=1e-15,ax=None,**kwargs):
    if ax==None:
        ax=plt.gca()
    
    # Get key variables
    depth = abs(data['Points:1']-200000) # m
    visc = data['viscosity']
    #strain_rate = data['strain_rate']
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

    output = pd.Series(np.nan,index=df.index)
    for x in range(len(fields)):
        output.mask(df[fields[x]]>0.5,x+1,inplace=True)
    output.mask(output.isna(),0,inplace=True)
    return(output)

def cmyk2rgb(cmyk):
    r = (1-cmyk[0]/100)*(1-cmyk[3]/100)
    g = (1-cmyk[1]/100)*(1-cmyk[3]/100)
    b = (1-cmyk[2]/100)*(1-cmyk[3]/100)
    rgb = (r,g,b)
    return(rgb)

def plot(file,output,field='density',bounds=None,contours=True,
         cfields=['crust_upper','crust_lower','mantle_lithosphere'],
         null_field='asthenosphere',off_screen=True,
         camera=None,**kwargs):
    
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
    #plotter.remove_bounding_box()
    #plotter.reset_camera()
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
    contour_mesh = mesh.copy()
    cntrs = contour_mesh.contour(isosurfaces=values,scalars=field)
    return(cntrs)
    

def comp_field_vtk(mesh,fields=['crust_upper','crust_lower','mantle_lithosphere'],
               null_field='asthenosphere'):

    # Create empty np array
    output = np.zeros(shape=mesh.point_arrays[fields[0]].shape)
    for x in range(len(fields)):
        array = mesh.point_arrays[fields[x]]
        output = np.where(array>0.5,x+1,output)
    
    mesh.point_arrays['comp_field'] = output
    return(mesh)
    
    

