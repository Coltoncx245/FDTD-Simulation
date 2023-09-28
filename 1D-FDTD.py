# Finite-Difference Time-Domain simulation in 1 Dimension

import numpy as np
import math
import matplotlib.animation as animation 
import matplotlib.pyplot as plt 
import numpy as np

fig, ax = plt.subplots()
plt.ylim(-1.5, 1.5)
plt.xlabel("Spatial Step (mm)")
plt.ylabel("E-Field z (V/m)")

size = 200              # define spatial axis size
source_node = 10        # define source node
impedance = 377         # free space impedance

H_y = np.zeros(size)                        # magnetic field y-component
E_z = np.zeros(size)                        # electric field z-component
spatial_axis = np.linspace(0, size, size)   # define spatial axis


line2, = ax.plot(spatial_axis, E_z) # plot electric field vs spatial axis


# handle inhomogeneities along spatial axis
relative_permittivity = np.ones(size)       # initialize relative dielectric permittivity for all points along spatial axis to 1 
relative_permeability = np.ones(size)       # initialize relative magnetic permeability for all points along spatial axis to 1 


# UNCOMMENT BELOW to add a dialectric with relative permittivity of 8 beginning at point 150 on the spatial axis
# relative_permittivity[150:] = 8
# plt.axvspan(150, size, alpha=0.5, color='y')


# update equation for y-component of magnetic field (H-field)
def updateMagneticField():
    for i in range(0, size-1):
        H_y[i] = H_y[i] + (E_z[i+1] - E_z[i]) / impedance / relative_permeability[i]

# update equation for z-component of electric field (E-field)
def updateElectricField():
    for i in range(1, size):
        E_z[i] = E_z[i] + (H_y[i] - H_y[i - 1]) * impedance / relative_permittivity[i]




def update(t):
    
    # absorbing boundary condition for magnetic field
    H_y[size-1]=H_y[size-2]

    # update magnetic field
    updateMagneticField()

    # magnetic field total-field/scattered-field boundary
    H_y[source_node-1] -= math.exp(-(t-30) * (t-30) / 100) / impedance

    # absorbing boundary condition for electric field
    E_z[0] = E_z[1]
    
    # update electric field
    updateElectricField()

    # electric field total-field/scattered-field boundary
    E_z[source_node] += math.exp(-(t+0.5-(-0.5)-30) * (t+0.5-(-0.5)-30) / 100)

    # Plot electric field vs. spatial axis
    line2.set_data(spatial_axis, E_z)
    return line2


ani = animation.FuncAnimation(fig=fig, func=update, frames=500, interval=1, repeat=False)
plt.show()