# -*- coding: utf-8 -*-
"""
Comparing calculated viscosity profiles with output from ASPECT
"""
from geoscripts import geophysics as gph
import pandas as pd
import matplotlib.pyplot as plt

# Dislocation Creep Factors
A = [8.57e-28,7.13e-18,6.52e-16,6.52e-16]
E = [223.e3,345.e3,530.e3,530.e3]
n = [4.,3.,3.5,3.5]
V = [0,0,18.e-6,18.e-6]

# Diffusion Creep Factors
A_df = [1.e-50,1.e-50,1.e-50,2.37e-15]
E_df = [0,0,0,375.e3]
m = [0,0,0,3.]
d = 1.e-3
V_df = [0,0,0,2.e-6]

z,comp,disl,diff,t = gph.viscosity_profile(A=A,A_df=A_df,n=n,d=d,m=m,E=E,E_df=E_df,V=V,
                               V_df=V_df)

test1 = gph.visc_dislocation(A=A[0],n=n[0],E=E[0],P=10,V=V[0],T=300)
test2 = gph.visc_disl_alt(C=A[0],n=n[0],t=300,E=E[0])

path = 'C:/Users/dyvas/Box/UC Davis/ASPECT/diffusioncreep/viscosity_test.csv'
path2 = 'C:/Users/dyvas/Box/UC Davis/ASPECT/diffusioncreep/disl_viscosity.csv'
comp_data = pd.read_csv(path)
disl_data = pd.read_csv(path2)


fig=plt.figure()
ax2 = fig.add_subplot(131)
ax2.plot(disl_data['viscosity'],(disl_data['Points:1']/1000)+200)
ax2.set_xscale('log')
ax2.set_xlim([1e16,1e30])
ax2.set_title('Model Dislocation')
ax2.set_ylim([0,400])

ax = fig.add_subplot(132)
ax.plot(comp_data['viscosity'],comp_data['Points:1']/1000)
ax.set_xscale('log')
ax.set_xlim([1e16,1e30])
ax.set_title('Model Composite')
ax.set_ylim([0,400])
plt.tight_layout()

temps,heat_flows,z,tc2 = gph.cond_geotherm()
ta2 = gph.adiab_geotherm(z=z)



