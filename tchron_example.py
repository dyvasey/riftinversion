# -*- coding: utf-8 -*-
"""
Example use of functions in tchron to forward model AHe
"""
import numpy as np
import tchron as tc

from scipy.optimize import fsolve

U = 10.77
Th = 20.55
radius = 56.3
time_interval = 10e6
temps = np.array([500,150,30,30])

age_model = tc.forward_model(U,Th,radius,temps,time_interval,mineral='apatite',nodes=500)

print('Age: ',age_model)





