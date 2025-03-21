"""
Functions for forward modeling of thermochronometric ages
"""
import warnings

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.integrate import romb
from scipy.linalg import solve_banded
from scipy.interpolate import griddata

def tridiag(a, b, c, diag_length):
    """
    Set up a tridiagonal matrix from the values for the 3 diagonals (a,b,c)

    Parameters
    ----------
    a : float
        First diagonal value
    b : float
        Second diagonal value
    c : float
        Third diagonal value
    diag_length : flaot
        Length of principal diagonal 

    Returns
    -------
    tridiag_matrix : NumPy array
        Tridiagonal matri

    """    
    a_array = np.ones(diag_length-1)*a
    b_array = np.ones(diag_length)*b
    c_array = np.ones(diag_length-1)*c
    
    tridiag_matrix = (
        np.diag(a_array, -1) + np.diag(b_array, 0) + np.diag(c_array, 1)
        )
    
    return(tridiag_matrix)

def tridiag_banded(a, b, c, diag_length):
    """
    Set up a tridiagonal matrix in banded form
    from the values for the 3 diagonals (a,b,c).

    Parameters
    ----------
    a : float
        First diagonal value
    b : float
        Second diagonal value
    c : float
        Third diagonal value
    diag_length : flaot
        Length of principal diagonal 

    Returns
    -------
    tridiag_matrix : NumPy array
        Tridiagonal matri

    """
    dtype=np.float32
    
    a_array = np.ones(diag_length,dtype=dtype)*a
    b_array = np.ones(diag_length,dtype=dtype)*b
    c_array = np.ones(diag_length,dtype=dtype)*c
    
    banded_matrix = np.vstack((a_array,b_array,c_array))
    banded_matrix[0,0] = 0
    banded_matrix[-1,-1] = 0
    
    return(banded_matrix) 

def get_parameters(system='AHe'):
    """
    Get appropriate diffusion parameters for particular isotopic system.
    
    Frequency factors and activation energies after Reiners and Brandon, 2006
    and references therein. Stopping distances after Ketcham et al., 2011.

    Parameters
    ----------
    system : string, optional
        Shorthand name of the system. Options include AHe, ZHe, BtAr, MsAr,
        HbAr, and KsAr. The default is 'AHe'.

    Returns
    -------
    freq_factor : float
        Frequency factor (um^2*yr^-1)
    activ_energy : float
        Activation energy (J*mol^-1)
    stopping_distances : tuple
        Set of stopping distances (um) for U238, U235, and Th235. Only for 
        AHe and ZHe.

    """
    if system == 'AHe':
        # Frequency Factor(um^2*yr^-1)
        freq_factor=50e8*3.154e7;
        # Activation Energy (J*mol^-1)
        activ_energy=138000
        # Stopping Distances (um)
        R_238U = 18.81
        R_235U = 21.80
        R_232Th = 22.25
        
    elif system == 'ZHe':
        # Frequency Factor(um^2*yr^-1)
        freq_factor=0.46e8*3.154e7;
        # Activation Energy (J*mol^-1)
        activ_energy=169000
        # Stopping Distances (um)
        R_238U = 15.55
        R_235U = 18.05
        R_232Th = 18.43
    
    elif system == 'BtAr':
        # Frequency Factor(um^2*yr^-1)
        freq_factor=7.5e-2*1e8*3.154e7;
        # Activation Energy (J*mol^-1)
        activ_energy=197000
    
    elif system == 'MsAr':
        # Frequency Factor(um^2*yr^-1)
        freq_factor=9.8e-3*1e8*3.154e7;
        # Activation Energy (J*mol^-1)
        activ_energy=18000
    
    elif system == 'HbAr':
        # Frequency Factor(um^2*yr^-1)
        freq_factor=6e-2*1e8*3.154e7;
        # Activation Energy (J*mol^-1)
        activ_energy=268000
    
    elif system == 'KsAr':
        # Frequency Factor(um^2*yr^-1)
        freq_factor=9.8e-3*1e8*3.154e7;
        # Activation Energy (J*mol^-1)
        activ_energy=183000
    
    else:
        raise Exception('Isotopic System Not Found')
    
    if (system == 'AHe') or (system == 'ZHe'):
        stopping_distances = np.array([R_238U,R_235U,R_232Th])
        return(freq_factor,activ_energy,stopping_distances)
    else:
        return(freq_factor,activ_energy)

def calculate_diffusivity(T,freq_factor,activ_energy,R=8.3144598):
    """
    Calculate diffusivity (kappa) based on temperature and system diffusion
    parameters
    
    After Reiners and Brandon, 2006, with PVa term assumed to be 0.

    Parameters
    ----------
    T : float
        Temperature (K)
    freq_factor : float
        Frequency factor (um^2*yr^-1)
    activ_energy : float
        Activation energy (J*mol^-1)
    R : float, optional
        Gas constant (J*K^-1*mol^-1). The default is 8.3144598.

    Returns
    -------
    kappa : float
        Diffusivity

    """
    kappa = freq_factor*np.exp(-activ_energy/(R*T))
    return(kappa)

def calculate_beta(diffusivity,node_spacing,time_interval):
    """
    Calculate beta, a substitution term based on diffusivity, the spacing
    of nodes within the modeled grain, and the timestep. After Ketcham, 2005.

    Parameters
    ----------
    diffusivity : float
        Diffusivity.
    node_spacing : float
        Spacing of nodes in the modeled crystal (um)
    time_interval : float
        Timestep in the thermal model (yr)

    Returns
    -------
    beta : float
        Beta, after Ketcham, 2005.

    """
    beta = (2*(node_spacing**2))/(diffusivity*time_interval)
    return(beta)

def UTh_ppm2molg(U,Th):
    """
    Convert concentrations of U and Th from ppm to mol/g

    Parameters
    ----------
    U : float
        U concentration (ppm)
    Th : float
        Th concentration (ppm)

    Returns
    -------
    U238_molg : float
        U238 (mol/g)
    U235_molg : float
        U235 (mol/g)
    Th_molg : float
        Th232 (mol/g)
    """
        
    U238_ppm = (137.88/(1+137.88))*U
    U235_ppm = (1/(1+137.88))*U 
    Th_ppm = Th
    
    U238_molg = U238_ppm*1e-6/238
    U235_molg = U235_ppm*1e-6/235
    Th_molg = Th_ppm*1e-6/232
    
    return(U238_molg,U235_molg,Th_molg)

def calculate_He_production_rate(U238_molg,U235_molg,Th_molg):
    """
    Calculate He production rate as a function of U and Th.

    Parameters
    ----------
    U238_molg : float
        U238 (mol/g)
    U235_molg : float
        U235 (mol/g)
    Th_molg : float
        Th232 (mol/g)

    Returns
    -------
    He_production : float
        He production (mol/g)

    """
    
    lambda238 = -np.log(1/2)/4.468e9
    lambda235 = -np.log(1/2)/7.04e8
    lambda232 = -np.log(1/2)/1.40e10
    
    term238 = 8*lambda238*U238_molg
    term235 = 7*lambda235*U235_molg
    term232 = 6*lambda232*Th_molg
    
    He_production = term238+term235+term232
    
    return(He_production)
    

def calculate_node_positions(node_spacing,radius):
    """
    Calculate node positions given spacing and radius.
    
    Follows Ketcham, 2005.

    Parameters
    ----------
    node_spacing : float
        Distance between nodes in the crystal (um)
    radius : float
                Radius of the grain (um)  
    
    Returns
    -------
    node_positions : NumPy array
        Radial positions of each modeled node (um)

    """
    node_positions = np.arange(node_spacing/2,radius,node_spacing)
    
    return(node_positions)

def sum_He_shells(x,node_positions,radius,nodes,print_He=True):
    """
    Sum He produced within all nodes of the modeled crystal. 
    
    Uses substition for He volume after Ketcham, 2005. Converts radial profile
    to system of shells, so He is weighted by volume of shell. Also prints out 
    He volume for comparison with real data.

    Parameters
    ----------
    x : NumPy array
        Matrix x solved for using matrices A and B after Ketcham, 2005.
        Equivalent to the volume times the node position.
    node_positions : NumPy array
        Radial positions of each modeled node (um)
    radius : float
            Radius of the grain (um)    
    nodes : float
            Number of modeled nodes in the crystal

    Returns
    -------
    He_molg : float
        Total amount (mol/g) of He within the modeled crystal.
    v : NumPy array
        Radial profile of He (mol/g)

    """
    
    # Back-substitute u=vr to get radial profile
    v = (x/node_positions)
    
    # Get volumes of spheres at each node
    sphere_volumes = (node_positions)**3 * (4*np.pi/3)
    
    # Get total volume of the sphere
    total_volume = radius**3 * (4*np.pi/3)
    
    # Calculate volumes for the shell corresponding to each node
    shell_volumes = np.empty(sphere_volumes.size)
    for x in range(sphere_volumes.size):
        if x==0:
            shell_volumes[x]=sphere_volumes[x]
        else:
            shell_volumes[x] = sphere_volumes[x] - sphere_volumes[x-1]
    
    # Get shell as fraction of total volume
    shell_fraction = shell_volumes/total_volume
    
    # Scale He within radial profile by shell fraction
    v_shells = v*shell_fraction
    
    # Integrate weighted radial profile
    He_molg = romb(v_shells)
    He_nccg = He_molg * 22.4e12
    
    if print_He==True:
        print('He (ncc/g): ',He_nccg)
        print('He (nmol/g): ',He_molg*1e9)

    return(He_molg,v)

def calculate_age(He_molg,U238_molg,U235_molg,Th_molg):
    """
    Calculate (U-Th)/He age.
    
    Note that no alpha correction is applied here. Instead, the alpha 
    correction is applied to the amounts of each parent isotope fed into 
    this function, following Ketcham et al., 2011.

    Parameters
    ----------
    He_molg : float
        Amount of He (mol/g)
    U238_molg : float
        Amount of U238 (mol/g)
    U235_molg : float
        Amount of U235 (mol/g)
    Th_molg : float
        Amount of Th232 (mol/g)

    Returns
    -------
    age_Ma : float
        Calculated (U-Th)/He age

    """
    
    lambda238 = -np.log(1/2)/4.468e9
    lambda235 = -np.log(1/2)/7.04e8
    lambda232 = -np.log(1/2)/1.40e10
    
    ageterm_238 = 8*U238_molg
    ageterm_235 = 7*U235_molg
    ageterm_232 = 6*Th_molg
    
    def age_equation(t):
        root = (
            ageterm_238*(np.exp(lambda238*t)-1)
            + ageterm_235*(np.exp(lambda235*t)-1)
            + ageterm_232*(np.exp(lambda232*t)-1) - He_molg
            ) 
    
        return(root)
    
    warnings.filterwarnings('ignore','The iteration is not making good progress')
    
    age = float(fsolve(age_equation,1e6))
    age_Ma = age/1e6
    
    return(age_Ma)

def alpha_correction(stopping_distance,radius):
    """
    Calculate alpha ejection correction factor, after Ketcham et al., 2011.

    Parameters
    ----------
    stopping_distance : float
        Stopping distance for particular isotopic system (um).
    radius : float
        Radius of the grain (um)

    Returns
    -------
    tau : float
        Alpha correction factor

    """
    volume = (4/3) * np.pi * radius**3
    surface_area = 4 * np.pi * radius**2
    
    tau = 1 - 0.25*((surface_area*stopping_distance)/volume)
    
    return(tau)

def model_alpha_ejection(node_positions,stopping_distance,radius):
    """
    Model retained fraction of He after alpha ejection, given node position,
    stopping distances, and radius.

    Parameters
    ----------
    node_positions : NumPy array
        Radial positions of each modeled node (um)
    stopping_distance : float
        Stopping distance for particular isotopic system (um).
    radius : float
        Radius of the grain (um)

    Returns
    -------
    retained_fraction_edge : NumPy array
        Fraction of He retained after alpha ejection for each node position

    """
    
    # Find edge nodes based on stopping distance and radius
    edge_nodes = node_positions >= radius-stopping_distance
    
    # Calculate intersection planes for all nodes
    intersection_planes = (
        (node_positions**2 + radius**2 - stopping_distance**2)/(2*node_positions)
        )
    
    # Calculate retained fractions for all nodes hypothetically
    retained_fractions_all = (
        0.5 + (intersection_planes-node_positions)/(2*stopping_distance)
        )
    
    # Only apply retained fraction to edge nodes
    retained_fractions_edge = np.where(edge_nodes,retained_fractions_all,1)
    
    return(retained_fractions_edge)

def forward_model(U,Th,radius,temps,time_interval,system,nodes=513,
                  initial_He=np.nan,calc_age=True,print_age=True):
    """
    Forward model a (U-Th)/He age for a particular time-temperature path.
    
    Uses finite difference method for diffusion within a sphere as described 
    in Ketcham, 2005. Applies alpha ejection correction after Ketcham et al.,
    2011. Returns corrected age but uncorrected age also printed.

    Parameters
    ----------
    U : float
        U concentration (ppm)
    Th : float
        Th concentration (ppm)
    radius : float
        Radius of the grain (um)
    temps : NumPy array
        List of temperatures (K) for the time-temperature path
    time_interval : float
        Time (yr) between each temperature in the time-temperature path.
    system : string
        Isotopic system. Current options are 'AHe' and 'ZHe'.
    nodes : float, optional
        Number of nodes to model within the crystal. The default is 513.

    Returns
    -------
    age_corrected : float
        (U-Th)/He age (Ma) corrected for alpha ejection

    """
    
    # Find node spacing and time interval based on radius and T-t path
    node_spacing = radius/nodes
    
    node_positions = calculate_node_positions(node_spacing,radius)
    
    # Get parameters for the appropriate mineral
    freq_factor,activ_energy,stop_distances = get_parameters(system)
    
    # Get mol/g of U,Th
    U238_molg,U235_molg,Th_molg = UTh_ppm2molg(U,Th)
    
    # Package parameters to pass to He profile
    
    node_information = (nodes,node_spacing,node_positions)
    UTh_molg = (U238_molg,U235_molg,Th_molg)
    system_parameters = (freq_factor,activ_energy,stop_distances)
    
    # Calculate He profile
    x = He_profile(temps,time_interval,node_information,radius,UTh_molg,
                   system_parameters,initial_He)
    
    if calc_age==True:
    
        # Calculate corrected age age
        age,vol,pos = profile2age(x,node_positions,radius,nodes,UTh_molg,
                                  stop_distances,print_age)
        
        return(age,vol,pos,x)
    
    else:
        return(x)

def He_profile(temps,time_interval,node_information,radius,UTh_molg,
               system_parameters,initial_He=np.nan):    
    
    # Unpack parameters
    nodes,node_spacing,node_positions = node_information
    U238_molg,U235_molg,Th_molg = UTh_molg
    freq_factor,activ_energy,stop_distances = system_parameters

    # Modify mol/g of U,Th for alpha ejection
    U238_alpha = (
        U238_molg*model_alpha_ejection(node_positions,stop_distances[0],
                                                radius)
        )
    
    U235_alpha = (
        U235_molg*model_alpha_ejection(node_positions,stop_distances[1],
                                                radius)
        )
    
    Th_alpha = (
        Th_molg*model_alpha_ejection(node_positions,stop_distances[2],
                                                radius)
        )
    
    # Calculate He production based on U and Th, adjusted for alpha ejection.
    He_production = calculate_He_production_rate(U238_alpha,U235_alpha,Th_alpha)
    
    if np.all(np.isnan(initial_He)):
        # Set initial x (He) equal to 0
        x = np.zeros(nodes)
    else:
        x = initial_He
    
    # Loop through each step of the T-t path
    
    for temp in temps:
        
        # Use temperature to calculate diffusivity and beta
        
        diffusivity = calculate_diffusivity(temp,freq_factor,activ_energy)
        beta = calculate_beta(diffusivity,node_spacing, time_interval)
        
       # Calculate A (banded) and use x to calculate new B

        AB = tridiag_banded(1,-2-beta,1,nodes)
        AB[1,0]=-3-beta # Following Guenthner Matlab script - Neumann
        B = np.zeros(nodes)
        # Loop through each node
        for j in range(len(node_positions)):
            # For first node, use boundary condition (Neumann)
            if j==0:
                B[j] = (
                    x[j] + (2-beta)*x[j] - x[j+1]
                    - He_production[j]*node_positions[j]*beta*time_interval
                    )
                
            # For last node, use boundary condition (Drichlet)
            elif j==(len(B)-1):
                B[j] = (
                    -x[j-1] + (2-beta)*x[j] - 0
                    - He_production[j]*node_positions[j]*beta*time_interval
                    )
            # Use previous and subsequent nodes for remaining nodes
            else:
                B[j] = (
                    -x[j-1] + (2-beta)*x[j] - x[j+1]
                    - He_production[j]*node_positions[j]*beta*time_interval
                    )
        
        # Solve for x using banded A and B
        x = solve_banded((1,1),AB,B)
        
    return(x)

def profile2age(x,node_positions,radius,nodes,UTh_molg,stop_distances,
                print_age=True,):
        
    He_molg,volumes = sum_He_shells(x,node_positions,radius,nodes,
                                    print_He=print_age)
    
    U238_molg,U235_molg,Th_molg = UTh_molg
    
    # Because alpha ejection modeled, model age is an "uncorrected" age.
    age_uncorrected = calculate_age(He_molg,U238_molg,U235_molg,Th_molg)

    # "Corrected" age uses alpha-adjusted U-Th values
    
    # Get array of correction values (238,235,232)
    tau = alpha_correction(stop_distances,radius)
    
    # Correct U and Th accordingly
    U238_corr = U238_molg*tau[0]
    U235_corr = U235_molg*tau[1]
    Th_corr = Th_molg*tau[2]
    
    age_corrected = calculate_age(He_molg,U238_corr,U235_corr,Th_corr)
    
    if print_age==True:
        print('Age (Ma) Uncorrected: ',age_uncorrected)
        print('Age (Ma) Corrected: ',age_corrected)
    
    # Make diffusional profile
    volumes_normalized = volumes/np.max(volumes)
    position_normalized = node_positions/radius
    
    return(age_corrected,volumes_normalized,position_normalized)

def interpolate(x,y,age,**kwargs):
    all_parts = (x,y)
    
    
    
    known_x = x[~np.isnan(age)]
    known_y = y[~np.isnan(age)]
    knowns = (known_x,known_y)
    
    known_ages = age[~np.isnan(age)]
    
    # Make negative ages 0
    positive_ages = np.where(known_ages>0,known_ages,0)
    
    filled_grid = griddata(knowns,positive_ages,all_parts,**kwargs)
    
    return(filled_grid)
        
        
        
    
                               



