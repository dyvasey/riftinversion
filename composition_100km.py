# Runtime options:
# 1. Within notebook: exec(open("random_plastic_strain.py").read())
# 2. Within terminal: ipython random_plastic_strain.py
# ToDo: Add description of varibales in example.py

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


# Input variables

plot_or_not = 'yes'

xmin    =   0.0e3
xmax    = 1000.0e3
ymin    =   0.0e3
ymax    = 200.0e3
gres    =   2.0e3
rmin    =   0.5
rmax    =   1.5

# Plastic strain
xmin_ep = 375.e3
xmax_ep = 625.e3
ymax_ep = 200.e3
ymin_ep = 140.e3

# Compositonal layers
ymin_cu = 180.e3
ymin_cl = 160.e3
ymin_ml = 100.e3

cfix    = 'true'
wela    = 'true'

# Setup of 2D spatial grid
xpts = int((xmax - xmin)/gres) + 1
ypts = int((ymax - ymin)/gres) + 1
#
x = np.linspace(xmin,xmax,xpts)
y = np.linspace(ymin,ymax,ypts)
#
xx, yy = np.meshgrid(x,y,indexing='ij')

# Array for randomized plastic strain and viscous strain
ep = np.zeros([xpts,ypts])

# Open outfile for composition data
outfile=open('composition.txt','w')
outfile.write('# POINTS: %-i %i\n'% (x.size,y.size))

# Loop through grid points
for i in range(y.size):

  for j in range(x.size):

      # Randomized plastic strain is non-zero only in specified regions
      if x[j]>xmin_ep and x[j]<xmax_ep and y[i]>ymin_ep and y[i]<ymax_ep:
      
        if cfix == 'true':
          if (np.random.random() < 0.5):
            ep[j,i] = rmin
          else:
            ep[j,i] = rmax
        else:
          ep[j,i] = rmin + (np.random.random() * (rmax - rmin))
      
      # Write spatial coordinates
      outfile.write('%-8.3e  ' % (x[j]))
      outfile.write('%-8.3e  ' % (y[i]))

      # Write elastic stresses
      if wela == 'true':
          outfile.write('%6.4f  ' % (0.0))
          outfile.write('%6.4f  ' % (0.0))
          outfile.write('%6.4f  ' % (0.0))

      # Write noninitial plastic strain values
      outfile.write('%6.4f  ' % (0.0))
     
      # Write plastic strain values
      outfile.write('%6.4f  ' % (ep[j,i]))
          
      # Write upper crust values
      if y[i]>ymin_cu:
        outfile.write('%6.4f  ' % (1.0))
      else:
        outfile.write('%6.4f  ' % (0.0))
      
      # Write lower crust values
      if y[i]<=ymin_cu and y[i]>ymin_cl:
        outfile.write('%6.4f  ' % (1.0))
      else:
        outfile.write('%6.4f  ' % (0.0))

      # Write lithospheric mantle values
      if y[i]<=ymin_cl and y[i]>ymin_ml:
        outfile.write('%6.4f  \n' % (1.0))
      else:
        outfile.write('%6.4f  \n' % (0.0))

# Close outfile
outfile.close()

# Plot random plastic strain
if plot_or_not == 'yes':
  # Plastic strain
  fig, ax = plt.subplots()
  ax.set_aspect('equal')
  ax.set_title('Initial Plastic Strain', fontsize=14)
  ax.set_xlim(xmin/1.e3,xmax/1.e3)
  ax.set_ylim(ymin/1.e3,ymax/1.e3)
  ax.set_xlabel('Horizontal Position (km)')
  ax.set_ylabel('Height (km)')
  ctf = ax.contourf(xx[:,:]/1.e3,yy[:,:]/1.e3,ep[:,:])
  divider = make_axes_locatable(ax)
  cax = divider.append_axes("right", size="1%", pad=0.05)
  fig.colorbar(ctf, cax=cax)
  plt.savefig('initial_plastic_strain.png',dpi=300)

