#last updated 9/17/21 by Isaiah Mumaw

#inside of the brackets, list all points along the x-axis in order
x_axis_points = [50,100,150,200,250]

#inside of the brackets, list all corresponding points along the y-axis
y_axis_points = [965.1595901881589,
                 1106.955435038906,
                 1248.3719758064517,
                 1388.4860038610038,
                 1523.8025706940873]

#inside of the brackets, list all corresponding error values for each data point
error_values = [8.502176927161468,
                7.037853276156161,
                7.577688422071424,
                7.622727970633007,
                7.544493119153263]

#title
chart_title = "Peaks vs. Channels"

#axis labels
x_axis_label = "Distance (cm)"
y_axis_label = "Channels"


##############################################################################
#######################  IGNORE EVERYTHING BELOW HERE  #######################
##############################################################################

import numpy as np
import scipy.stats as sps
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

x_axis_points = np.array(x_axis_points)
y_axis_points = np.array(y_axis_points)
error_values = np.array(error_values)

plt.errorbar(x_axis_points, y_axis_points,yerr=error_values,
             fmt=".",capsize=8)

slope, intercept, r_value, p_value, std_err = sps.linregress(x_axis_points, y_axis_points)

plt.plot(x_axis_points,intercept+slope*x_axis_points)

ax.set_xlabel(x_axis_label)
ax.set_ylabel(y_axis_label)
ax.set_title(chart_title)
ax.grid(True)

print("Results from line of fit:")
print("Slope: "+str(slope))
print("Standard error on slope: "+str(std_err))
print("Y-intercept: "+str(intercept))
print("R^2 value: "+str(r_value**2))

plt.show()