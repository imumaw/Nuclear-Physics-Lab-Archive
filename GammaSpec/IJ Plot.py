import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

x = np.array( [1, 2, 3, 3, 4, 4, 5, 5, 5, 7, 8, 8] )
y = np.array( [94.810, 305.782, 753.346, 806.575, 1322.795, 1475.81, 1530.812, 1503.81, 1529.782, 1817.009, 1843.46, 1841.831] )

ychan = (y-7.023)/1.1
yerr = np.sqrt( (ychan**2)*(0.006313927164763389**2) + (5.200627452513809**2) )

j = (((1.054e-34)**2)/(2*y*1.6022e-16))*(x*(x+1))

plt.scatter(x, j)
plt.errorbar(x, j, yerr=yerr*((1.054e-28)**2)/2, fmt="o", capsize=8)

plt.xlabel("Angular Momentum Quantum Number (I)")
plt.ylabel("Moment of Inertia (J, kg m^2)")