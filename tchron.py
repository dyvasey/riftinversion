"""
Functions for forward modeling of thermochronometric ages
"""
import numpy as np
from scipy.optimize import fsolve

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
    
    if system == ('AHe' or 'ZHe'):
        stopping_distances = np.array([R_238U,R_235U,R_232Th])
        return(freq_factor,activ_energy,stopping_distances)
    else:
        return(freq_factor,activ_energy)

def calculate_diffusivity(T,freq_factor,activ_energy,R=8.3144598):
    """
    Calculate diffusivity (kappa) based on temperature and system diffusion
    parameters

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

def calculate_He_production(U238_molg,U235_molg,Th_molg):
    """
    Calculate He production as a function of U and Th.

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

def initial_conditions(node_spacing,nodes,time_interval,He_production,beta):
    """
    Calculate initial A and B matrices to solve for x for initial timestep.
    
    Follows Ketcham, 2005.

    Parameters
    ----------
    node_spacing : float
        Distance between nodes in the crystal (um)
    nodes : float
        Number of modeled nodes in the crystal
    time_interval : float
        Interval between modeled timesteps (yr)
    He_production : float
        He production (mol/g)
    beta : float
        Beta, a substitution defined in Ketcham, 2005.

    Returns
    -------
    A_initial : NumPy array
        Initial A matrix
    B_initial : NumPy array
        Initial B matrix
    node_positions : NumPy array
        Radial positions of each modeled node (um)

    """
    node_positions = np.arange(node_spacing/2,nodes*node_spacing,node_spacing)
    B_initial = -He_production/(nodes)*node_positions*beta*time_interval
    A_initial = tridiag(1,-2-beta,1,nodes)
    
    return(A_initial,B_initial,node_positions)

def sum_He(x,node_positions):
    """
    Sum He produced within all nodes of the modeled crystal. 
    
    Uses substition for He volume after Ketcham, 2005. Also prints out He
    volume in ncc/g for comparison with real data.

    Parameters
    ----------
    x : NumPy array
        Matrix x solved for using matrices A and B after Ketcham, 2005.
        Equivalent to the volume times the node position.
    node_positions : NumPy array
        Radial positions of each modeled node (um)

    Returns
    -------
    He_molg : float
        Total amount (mol/g) of He within the modeled crystal.

    """
    volumes = x/node_positions
    He_molg = np.sum(volumes)
    He_nccg = He_molg * 22.4e12
    
    print('He (ncc/g): ',He_nccg)

    return(He_molg)

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
        Calculated U

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

def forward_model(U,Th,radius,temps,time_interval,system,nodes=500):
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
        Number of nodes to model within the crystal. The default is 500.

    Returns
    -------
    age_corrected : float
        (U-Th)/He age (Ma) corrected for alpha ejection

    """
    
    # Find node spacing and time interval based on radius and T-t path
    node_spacing = radius/nodes
    print('Node Spacing (microns): ',node_spacing)
    
    # Get parameters for the appropriate mineral
    freq_factor,activ_energy,stop_distances = get_parameters(system)
    
    # Get array of correction values (238,235,232)
    tau = alpha_correction(stop_distances,radius)
    
    # Calculate He production based on U and Th
    U238_molg,U235_molg,Th_molg = UTh_ppm2molg(U,Th)
    He_production = calculate_He_production(U238_molg,U235_molg,Th_molg)
    
    # Loop through each step of the T-t path
    
    for k,temp in enumerate(temps):
        
        # Use temperature to calculate diffusivity and beta
        
        diffusivity = calculate_diffusivity(temp,freq_factor,activ_energy)
        beta = calculate_beta(diffusivity,node_spacing, time_interval)
        
        # For first timestep, use boundary conditions to get initial A and B
        # and set up node positions
        if k==0:
            A,B,node_positions = initial_conditions(node_spacing,nodes,
                                                    time_interval,He_production,
                                                    beta)
       # For subsequent timesteps, calculate new A and use x to calculate new B
        else:
            A = tridiag(1,-2-beta,1,nodes)
            B = np.empty(nodes)
            # Loop through each node
            for j in range(len(B)):
                # For first node, use boundary condition (Neumann)
                if j==0:
                    B[j] = (
                        x[j] + (2-beta)*x[j] - x[j+1]
                        - He_production/nodes*node_positions[j]*beta*time_interval
                        )
                
                # For last node, use boundary condition (Drichlet)
                elif j==(len(B)-1):
                    B[j] = (
                        x[j] + (2-beta)*x[j] - 0
                        - He_production/nodes*node_positions[j]*beta*time_interval
                        )
                    
                # Use previous and subsequen nodes for remaining nodes
                else:
                    B[j] = (
                        -x[j-1] + (2-beta)*x[j] - x[j+1]
                        - He_production/nodes*node_positions[j]*beta*time_interval
                        )
        
        # Solve for x using A and B

        x = np.linalg.solve(A,B)
        
    He_molg = sum_He(x,node_positions)
    
    age_uncorrected = calculate_age(He_molg,U238_molg,U235_molg,Th_molg)
    
    print('Age (Ma) Uncorrected: ',age_uncorrected)
    
    parent_uncorrected = np.array([U238_molg,U235_molg,Th_molg])
    parent_corrected = parent_uncorrected*tau
    
    age_corrected = calculate_age(He_molg,parent_corrected[0],
                                  parent_corrected[1],parent_corrected[2])
    
    print('Age (Ma) Corrected: ',age_corrected)
    
    return(age_corrected)
        
        
        
    
                               



