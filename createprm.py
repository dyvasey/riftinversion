"""
Script for creating the current prm models to run on Stampede2
"""
import ripropagate

# Reference model to breakup
ripropagate.generate(etime=12,output='./ref_breakup',ver='a') 

# Reference model halfway to breakup
ripropagate.generate(etime=6,output='./ref_half',ver='b') 

# Asymmetric model test run
ripropagate.generate(etime=20,lthick=80,evel=2,output='./asymm_rift',ver='c') 