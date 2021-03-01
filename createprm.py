"""
Script for creating the current prm models to run on Stampede2
"""
import ripropagate

ripropagate.generate(etime=20) # Generate reference model for 20 Myr run

# Generate 5 Myr increments
times = [5,10,15,20]
versions = ['a','b','c','d']
folders = [str(x)+'Myr' for x in times] 

for x in range(len(times)):
    ripropagate.generate(etime=times[x],ver=versions[x],output=folders[x])

