"""
Functions for forward modeling of thermochronometric ages
"""
import numpy as np
from scipy.optimize import fsolve

def tridiag(a, b, c, diag_length):
    a_array = np.ones(diag_length-1)*a
    b_array = np.ones(diag_length)*b
    c_array = np.ones(diag_length-1)*c
    
    tridiag_matrix = (
        np.diag(a_array, -1) + np.diag(b_array, 0) + np.diag(c_array, 1)
        )
    
    return(tridiag_matrix) 

def get_parameters(system='AHe'):
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
    kappa = freq_factor*np.exp(-activ_energy/(R*T))
    return(kappa)

def calculate_beta(diffusivity,node_spacing,time_interval):
    beta = (2*(node_spacing**2))/(diffusivity*time_interval)
    return(beta)

def UTh_ppm2molg(U,Th):
        
    U238_ppm = (137.88/(1+137.88))*U
    U235_ppm = (1/(1+137.88))*U 
    Th_ppm = Th
    
    U238_molg = U238_ppm*1e-6/238
    U235_molg = U235_ppm*1e-6/235
    Th_molg = Th_ppm*1e-6/232
    
    return(U238_molg,U235_molg,Th_molg)

def calculate_He_production(U238_molg,U235_molg,Th_molg):
    
    lambda238 = -np.log(1/2)/4.468e9
    lambda235 = -np.log(1/2)/7.04e8
    lambda232 = -np.log(1/2)/1.40e10
    
    term238 = 8*lambda238*U238_molg
    term235 = 7*lambda235*U235_molg
    term232 = 6*lambda232*Th_molg
    
    He_production = term238+term235+term232
    
    return(He_production)

def initial_conditions(node_spacing,nodes,time_interval,He_production,beta):
    node_positions = np.arange(node_spacing/2,nodes*node_spacing,node_spacing)
    B_initial = -He_production/(nodes)*node_positions*beta*time_interval
    A_initial = tridiag(1,-2-beta,1,nodes)
    
    return(A_initial,B_initial,node_positions)

def sum_He(x,node_positions):
    volumes = x/node_positions
    He_molg = np.sum(volumes)
    He_nccg = He_molg * 22.4e12
    
    print('He (ncc/g): ',He_nccg)

    return(He_molg)

def calculate_age(He_molg,U238_molg,U235_molg,Th_molg):
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
    volume = (4/3) * np.pi * radius**3
    surface_area = 4 * np.pi * radius**2
    
    tau = 1 - 0.25*((surface_area*stopping_distance)/volume)
    
    return(tau)

def forward_model(U,Th,radius,temps,time_interval,system,nodes=500):
    
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
        
        
        
    
                               



