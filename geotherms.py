"""
Script to generate gotherms needed for rift inversion modeling. Goal is to
balance desired thickness with surface heat flow that produces the desired
LAB temperature (1573 K).
"""
import numpy as np
import pandas as pd

from geoscripts import geophysics as gph

gtherm_100 = gph.geotherm(thicknesses=[20,20,60],heat_flow=0.05296)

gtherm_80 = gph.geotherm(thicknesses=[20,20,40],heat_flow=0.06021)

gtherm_120 = gph.geotherm(thicknesses=[20,20,80],heat_flow=0.04812)

gtherm_60 = gph.geotherm(thicknesses=[20,20,20],heat_flow=0.07230)

gtherm_100_deep = gph.geotherm(thicknesses=[20,20,60],heat_flow=0.05296,
                               depth=600)

gtherm_60_deep = gph.geotherm(thicknesses=[20,20,20],heat_flow=0.07230,depth=600)

# Actually used for production runs

gtherm_80_deep = gph.geotherm(thicknesses=[20,20,40],heat_flow=0.06021,depth=600)

t150_80 = gtherm_80_deep[3][150]
t250_80 = gtherm_80_deep[3][250]

gtherm_120_deep = gph.geotherm(thicknesses=[20,20,80],heat_flow=0.04812,depth=600)

t150_120 = gtherm_120_deep[3][150]
t250_120 = gtherm_120_deep[3][250]

output = pd.Series(data=np.concatenate((t150_80,t250_80,t150_120,t250_120),axis=None),
                   index=['t150_80','t250_80','t150_120','t250_120'])

output.to_csv('amr_temps.csv')
