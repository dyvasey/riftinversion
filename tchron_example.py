# -*- coding: utf-8 -*-
"""
Example use of functions in tchron to forward model AHe
"""
import numpy as np

import tchron as tc

U = 10.77 # ppm
Th = 20.55 # ppm
radius = 100 # microns
time_interval = 10e6 # years
temps = np.array([500,150,30,30]) # C

age_model = tc.forward_model(
    U,Th,radius,temps,time_interval,system='ZHe',nodes=500)





