""" 
Script from JN for generating a temperature profile, which combines and smoothly
blends a conductive and adiabatic profile. Assumes the temperature at the base
of the lithosphere is equal to the adiabatic surface temperature in ASPECT.

Modified by DV to additionally output resulting values as a CSV to import
into scripts to modify .prm files
"""

# Notes from JN
# geotherm_conductive_plus_adiabatic.py:
#   A python script to generate a temperature profile, which combines and smoothly blends a
#   conductive and adiabatic profile. This is done, in part, by assuming the temperature at
#   the base of the lithosphere is equal to the adiabatic surface temperature used in ASPECT.
# Command to execute from interpreter:
#   exec(open("geotherm_v3.py").read())

from numpy import *;  import matplotlib.pyplot as plt;
import pandas as pd

# Plot end results?
plot_or_not = 'yes'

# Adiabatic surface temperature
ast = 1573.

# Define variables for lithosphere layer thickness, heat production, top/basal temperature,
# and top/basal heat flux.
k   = array([2.5,2.5,2.5])        # Thermal conductivity
dz  = array([20.e3,20.e3,80.e3]) # Layer thickness (m)
A   = array([1.e-6,2.5e-7,0.,])   # Radiogenic heat production (W/m**3)
Tt  = array([273.,0.,0.])         # Temperature at top of layer
Tb  = array([0.,0.,0.])           # Temperature at base of layer
qt  = array([0.04812,0.,0.])        # Heat flow at top of layer
qb  = array([0.,0.,0.])           # Heat flow at base of layer

lith = round(dz.sum()/1000,None) #lithosphere thickness in km

# Determine heat flow at base of upper crust
qb[0] = qt[0] - (A[0]*dz[0])

# Determine temperature at base of upper crust
Tb[0] = Tt[0] + (qt[0]/k[0])*dz[0] - (A[0]*dz[0]**2)/(2.*k[0])

# Assing temperature and heat flow at top of lower crust
Tt[1] = Tb[0]
qt[1] = qb[0]

# Determine temperature at base of lower crust
Tb[1] = Tt[1] + (qt[1]/k[1])*dz[1] - (A[1]*dz[1]**2)/(2.*k[1])

# Determine heat flow at base of lower crust
qb[1] = qt[1] - (A[1]*dz[1])

# Assign temperature and heat flow at top of lithospheric mantle
Tt[2] = Tb[1]
qt[2] = qb[1]

# Determine heat flow at base of lithospheric mantle
qb[2] = qt[2] - (A[2]*dz[2])

# Determine temperature at base of lower crust
Tb[2] = Tt[2] + (qt[2]/k[2])*dz[2] - (A[2]*dz[2]**2)/(2.*k[2])

# Print thermal values
print(' ')
print('Values for conductive profile')
print('Tt Tb qt qb k')
print(' ')
print('Upper Crust') 
print(Tt[0], Tb[0], qt[0], qb[0], k[0])
print('')
print('Middle/Lower Crust')
print(Tt[1], Tb[1], qt[1], qb[1], k[1])
print('')
print('Lithospheric Mantle')
print(Tt[2], Tb[2], qt[2], qb[2], k[2])
print('')

# Write thermal values to csv
output = pd.Series(data=concatenate((Tt,Tb[2],qt),axis=None),index=[
    'ts1','ts2','ts3','ts4','qs1','qs2','qs3'])
                                             
output.to_csv('thermal_'+str(lith)+'km.csv')

# Define arrays for depth and temperature
zi = 1.0e3
z  = array(range(0,121,1))*zi  # depth from 0 to 100 km (0.5 km increments)
tc = array(range(0,121,1))*0.  # array for comductive temperature values
ta = array(range(0,121,1))*0.  # array for adiabatic temperature value
tt = array(range(0,121,1))*0.  # array for total (conductive + adiabatic) temperature values

# Calculate conductive temperature as a function of depth
for i in range(size(z)):
  if z[i]<=dz[0]:
    tc[i] = Tt[0] + (qt[0]/k[0])*z[i] - (A[0]*(z[i]**2))/(2*k[0])
  elif z[i]>dz[0] and z[i]<=(dz[0]+dz[1]):
    tc[i] = Tt[1] + (qt[1]/k[1])*(z[i]-dz[0]) - (A[1]*((z[i]-dz[0])**2))/(2*k[1])
  elif z[i]>(dz[0]+dz[1]) and z[i]<=(dz[0]+dz[1]+dz[2]):
    tc[i] = Tt[2] + (qt[2]/k[2])*(z[i]-dz[0]-dz[1]) - (A[2]*((z[i]-dz[0]-dz[1])**2))/(2*k[2])
  elif (z[i]>(dz[0]+dz[1]+dz[2])):
    tc[i] = Tb[2] # Constant temperature beneath LAB, to be later replaced with adiabatic values

# Values used when calculating adiabatic temperature profile
gravity             = 9.81
thermal_expansivity = 2.e-5
heat_capacity       = 750.

# Calculate adiabatic temperature profile
for i in range(size(z)):
  if i==0:
    ta[i] = ast # By design, the adiabatic surface temperature is the LAB temp
  else:
    # See line 124 in source/adiabatic_conditions/compute_profile
    ta[i] = ta[i-1] * (1 + (thermal_expansivity * gravity * zi * 1./heat_capacity))
 
# The total temeprature is the conductive profile + the adiabatic temperature - the abdiabaic surface
# temperature (equal to LAB temperature by design).
tt = tc + ta - ast

print('')
print('LAB Depth       = ', sum(dz)/1.e3, 'km')
print('LAB Temperature = ', tt[int(sum(dz)/zi)], 'K')
print('')


# Plot results
if plot_or_not == 'yes':
  plt.plot(tt,z/1.e3,'r--'); plt.gca().invert_yaxis();
  plt.xlabel('Temperature (K)'); plt.ylabel('Depth (km)'); plt.show()

