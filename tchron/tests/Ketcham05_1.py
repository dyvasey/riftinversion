"""
First test of age and diffusion profile from Ketcham, 2005.
"""
import numpy as np
import matplotlib.pyplot as plt
from tchron import tchron as tc
from matplotlib import rc
rc("pdf", fonttype=42)

age_ketcham = 54.6

U = 100
Th = 100
radius = 100
time_interval = 1e5
early_t = np.linspace(120,20,101)
late_t = np.linspace(20,20,500)
temps = np.append(early_t,late_t) + 273
times = np.arange(60,-0.001,-0.1)

fig, axs = plt.subplots(1,2,figsize=(8,4),dpi=300)

fig.suptitle('Python Forward Model')

axs[0].plot(times,temps-273)
axs[0].grid(True)
axs[0].set_xlim(100,0)
axs[0].set_ylim(200,0)
axs[0].set_xlabel('Time (Ma)')
axs[0].set_ylabel('Temperature (C)')
axs[0].set_title('Time-Temperature History')
axs[0].set_xticks(np.arange(0,101,10))
axs[0].set_yticks(np.arange(0,201,20))

age_model,volumes,positions,x = tc.forward_model(U,Th,radius,temps,time_interval,system='AHe')

axs[1].plot(positions,volumes)
axs[1].grid(True)
axs[1].set_xlabel('Radius (normalized)')
axs[1].set_ylabel('He Concentration (normalized)')
axs[1].set_title('He Profile')
axs[1].annotate('AHe Age: '+str(round(age_model,1))+' Ma',xy=(0.3,0.5),xycoords='axes fraction',
                backgroundcolor='white',fontsize=12)
axs[1].set_xticks(np.arange(0,1.01,0.1))
axs[1].set_yticks(np.arange(0,1.01,0.1))

plt.tight_layout()

fig.savefig('Ketcham05_Test1.pdf')