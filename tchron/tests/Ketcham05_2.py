"""
Second test of age and diffusion profile from Ketcham, 2005.
"""
import numpy as np
import matplotlib.pyplot as plt
from riftinversion.tchron import tchron as tc

age_ketcham = 26.5

U = 1
Th = 1
radius = 50
time_interval = 10e6
temps = np.linspace(120,20,7) + 273
times = np.arange(60,0-1,-10)

fig, axs = plt.subplots(1,2)

fig.suptitle('Ketcham 2005, Linear Cooling')

axs[0].plot(times,temps-273)
axs[0].grid(True)
axs[0].set_xlim(100,0)
axs[0].set_ylim(200,0)
axs[0].set_xlabel('Time (Ma)')
axs[0].set_ylabel('Temperature (K)')
axs[0].set_title('Time-Temperature History')

age_model,volumes,positions = tc.forward_model(U,Th,radius,temps,time_interval,system='AHe')

axs[1].plot(positions,volumes)
axs[1].grid(True)
axs[1].set_xlabel('Radius (um)')
axs[1].set_ylabel('He Concentration (mol/g)')
axs[1].set_title('He Profile')
axs[1].annotate(str(round(age_model,2))+' Ma',xy=(0.5,0.5),xycoords='axes fraction')

plt.tight_layout()

fig.savefig('Ketcham05_Test2.pdf')