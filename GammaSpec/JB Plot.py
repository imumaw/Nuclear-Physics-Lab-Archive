import numpy as np
import matplotlib.pyplot as plt

del_r = np.linspace( -5.21, 5.21, 10000 )
beta = 4/3*((np.pi/5)**.5)*del_r/5.21

j_rigid = (2/5)*(2.756496731e-25)*(5.21e-15**2)*(1+0.31*beta)
j_fluid = (9/8/np.pi)*(2.756496731e-25)*(5.21e-15**2)*beta

plt.plot(beta,j_rigid,label="Rigid")
plt.plot(beta,j_fluid,label="Fluid")
plt.legend()

plt.xlabel("Deformation Parameter (β)")
plt.ylabel("Moment of Inertia (J)")
