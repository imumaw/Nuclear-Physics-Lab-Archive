#last updated 9/17/21 by Isaiah Mumaw

#change this to whatever file you need, just keep it in quotes
filepath = "/Users/isaiahmumaw/Documents/College/Fall 2021/Modern Phys Lab/Lab 1/csv files/Trial 5.csv"

#if you want to focus on specific channels use these.
range_min = 0       #lowest channel of focus
range_max = 4100    #highest channel of focus

#Removes noise. If a channel has counts below this number, it will be changed to 0.
threshold=5

#title
chart_title = "Speed of Light"

#legend labels. Leave as "" if you don't want to have legend
data_label = "Data"
fit_label = "Skew-Gaussian fit"

#if True, plots that information. If False, does not plot that information
plot_data=True
plot_fit=True

#resolution of fit lines (points per channel)
resolution=100


##############################################################################
#######################  IGNORE EVERYTHING BELOW HERE  #######################
##############################################################################

from lab_1 import *

num_channels=4100

raw_data, data = convert(filepath,num_channels,threshold,range_min,range_max)
skew,pts,skew_val,mean,var = get_fit(data,num_channels,resolution)

print("")

print("RESULTS:")
print("Skew factor: "+str(skew_val))
print("Mean channel: "+str(mean))
print("Standard deviation: "+str(var))

print("")

plotter(raw_data,skew,pts,plot_data,plot_fit,data_label,fit_label,chart_title)
