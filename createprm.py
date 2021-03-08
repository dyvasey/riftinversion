"""
Script for creating the current prm models to run on Stampede2
"""
import ripropagate

ripropagate.generate(etime=20,ver='b') # Generate reference model for 20 Myr run
