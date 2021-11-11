"""
Script to generate gotherms needed for rift inversion modeling. Goal is to
balance desired thickness with surface heat flow that produces the desired
LAB temperature (1573 K).
"""
from geoscripts import geophysics as gph

gtherm_100 = gph.geotherm(thicknesses=[20,20,60],heat_flow=0.05296)

gtherm_80 = gph.geotherm(thicknesses=[20,20,40],heat_flow=0.06021)

gtherm_120 = gph.geotherm(thicknesses=[20,20,80],heat_flow=0.04812)

gtherm_60 = gph.geotherm(thicknesses=[20,20,20],heat_flow=0.07230)

gtherm_100_deep = gph.geotherm(thicknesses=[20,20,60],heat_flow=0.05296,
                               depth=600)


