# Filename: SoL.py
# Purpose: Built to analyze data from speed of light experiment in Professor Zech's
#          Advanced Physics Lab.
# Author: Isaiah Mumaw, imumaw@nd.edu or isaiah.mumaw@gmail.com
# Date Created: 3/16/22, last modified 3/17/22

###############################################################################
##################################  MODULES  ##################################
###############################################################################

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skewnorm
from scipy.stats import norm
import scipy.stats as sps

###############################################################################
#################################  FUNCTIONS  #################################
###############################################################################

def CSV_to_array( filepath, channels=4100, dtype=int ):
    """Converts .csv file to a numpy integer array
    Chose not to use pandas methods as they are typically slower
    
    Parameters:
        filepath (string): filepath of csv file
        channels (int, optional): number of channels in data. Defaults to 4100
        dtype (type, optional): data type for numpy array. Defaults to int
    
    Returns:
        data (array): 2D array, data as listed in .csv file
    """
    
    if ".csv" not in filepath:
        print("Invalid filetype, must be .csv")
        return np.array([[-1],[-1]])
    
    try:
        fin = open( filepath, "r" )
        
    except:
        print("File does not exist")
        return np.array([[-1],[-1]])
        
    fin.readline()  #we will skip the header line
    
    data = np.zeros( (2, channels), dtype=dtype )     #empty array for data
    
    #cycle through imported data - create array with channels vs. counts
    for (i,row) in enumerate(fin):
           
        row = row.strip()
        row = row.split(",")
        
        channel = dtype( row[0] )
        data[0,i] = channel
        
        counts = dtype( row[1] )
        data[1,i] = counts

    fin.close()

    return data

###############################################################################

def get_skew_fit( data, channels=4100, resolution=100, scale=True ):
    """Fits skewed Gaussian curve to data
    
    Parameters:
        data (array): data array from CSV_to_array or filtered data from filter_data()
        num_channels (int, optional): number of channels being analyzed. Defaults 4100
        resolution (int, optional): number of points to calculate per channel. Defaults 100
        scale (bool, optional): if true, scales so that data and fit can be plotted on same axes. If false, gives true probability distribtion

    Returns:
        x_pts (array): array of points used for skew-Gaussian x-axis
        y_pts (array): array of points used for skew-Gaussian y-axis
        skew (float): amount of skew
        mean (float): mean of data
        var (float): variance (std) of data
    """

    dist = np.empty(sum(data[1]),dtype=int)
    index = 0
    
    #populate array
    for (i,value) in enumerate(data[1]):        #cycle through count set
        for j in range(value):                  #cycle through each count
            dist[index+j] = data[0,i]           #list channel associated with count
        index+=value                            #move marker to prevent overwrite
    
    #skew, mean, var = skewnorm.fit(dist)
    mean, var = norm.fit(dist)
    
    x_pts = np.linspace(0,channels-1,resolution*channels)
    #y_pts = skewnorm.pdf(x_pts,skew,mean,var)
    y_pts = norm.pdf(x_pts,mean,var)
    
    if scale:
        y_pts *= np.max(data[1])/np.max(y_pts)
    
    return x_pts, y_pts, mean, var#skew, mean, var

###############################################################################

def filter_data( data, min_x, max_x, min_y, max_y ):
    """Isolates desired portion of data
    
    Parameters:
        data (array): data array from CSV_to_array
        min_x, max_x (int): minimum and maximum channels to allow through
        min_y, max_y (int): minimum and maximum counts allowed
        
    Returns:
        filtered_data (array): data array after being filtered
    """
    
    filtered_data = np.copy(data)
    
    for i in range(len(data[0])):
        if i<min_x or i>max_x or data[1][i]<min_y:
            filtered_data[1,i] = 0
        elif data[1,i] > max_y:
            filtered_data[1,i] = max_y
    
    return filtered_data

###############################################################################
###############################################################################
###############################################################################

if __name__=="__main__":

    #set up output file
    from datetime import datetime
    now = datetime.now()
    
    while True:
        
        print("\033[H\033[J")
        print("Speed of Light Lab")
        print("")
        print("Please select one of the following:")
        print("    1 - Analyze data")
        print("    2 - Get time calibration")
        print("    3 - Save all results and exit")
        print("")
        
        choice = input("    Your choice: ")
        
        #Run program
        if choice == "1":
            
            #get file
            path = input("\nInput filepath: ")
            data = CSV_to_array(path)
            
            if data[0][0]!=-1:
                
                print("Plotting raw data...")
                
                #plot raw data - no filter applied
                plt.plot(data[0],data[1])
                plt.title("Raw Data")
                plt.xlabel("Channels")
                plt.ylabel("Counts")
                plt.show()
                
                while True:
                
                    choice = input("Apply filter? (y/n): ")
                    
                    if choice=="y":
                        
                        xmin = int(input("Minimum channel: "))
                        xmax = int(input("Maximum channel: "))
                        ymin = int(input("Minimum count: "))
                        ymax = np.max(data[1])
                        
                    else:
                        xmin = 0
                        xmax = np.max(data[0])
                        ymin = 0
                        ymax = np.max(data[1])   
                        
                    filtered_data = filter_data( data, xmin, xmax, ymin, ymax )
                        
                    x_pts, y_pts, mean, var = get_skew_fit( filtered_data )
                        
                    title = input("Plot title: ")
                    
                    print("Plotting raw data with filtered fit curve...")
                    
                    #print("Skew value: ", skew_val)
                    print("Mean: ", mean)
                    print("Variance: ", var)
                    
                    plt.plot(data[0],data[1],label="Data")
                    plt.plot(x_pts,y_pts,label="Fit curve")
                    
                    plt.title(title)
                    plt.xlabel("Channels")
                    plt.ylabel("Counts")
                    plt.legend()
                    
                    plt.xlim([500,1700])
                        
                    plt.show()
                    
                    choice = input("Try new filter parameters? (y/n): ")
                    
                    if choice!='y':
                        break
            
                #update log
                out = open( "SoL_Results "+str(now)+".log", 'a' )           
                
                out.write("Plot title: "+title+"\n")
                out.write("Data file: "+path+"\n")
                out.write("Min channel: "+str(xmin)+"\n")
                out.write("Min channel: "+str(xmax)+"\n")
                out.write("Min count: "+str(ymin)+"\n")
                out.write("Max count: "+str(ymax)+"\n")
                out.write("Mean: "+str(mean)+"\n")
                out.write("Variance: "+str(var)+"\n")
                out.write("\n")
                
                out.close()
            
            else:
                input("Press enter to continue")
            
        #this entire chunk is a mess but I honestly don't care enough to make it look nice
        elif choice == "2":
         
            #get file
            path = input("\nInput filepath: ")
            data = CSV_to_array(path)
            peaks = []
            errors = []
            num = 0
            denom = 0
            i=0
            
            while i in data[0]:
                if data[1][i]>0:
                    xvalues = []
                    yvalues = []
                    while data[1][i] > 0:
                        xvalues.append(i)
                        yvalues.append(data[1][i])
                        num += data[1][i] * i
                        denom += data[1][i]
                        i += 1
                    avg = num/denom
                    peaks.append(avg)
                    num = 0
                    denom = 0
                
                    dist = np.zeros(np.sum(yvalues))
                    index = 0
                
                    for (k,value) in enumerate(yvalues):        #cycle through count set
                        for j in range(value):                  #cycle through each count
                            dist[j+index] = xvalues[k]
                        index += value
                            
                    errors.append(np.std(dist))
                    
                i+=1
            
            cal_peaks = np.array(peaks)
            print(cal_peaks)
            cal_error = np.array(errors)
            print(cal_error)
            
            period = float(input("Calibration period (µs): "))
            time_peaks = np.linspace( period, len(cal_peaks)*period, len(cal_peaks))
            
            fig, ax = plt.subplots()
            
            plt.errorbar( time_peaks, cal_peaks, yerr=cal_error, fmt="o",capsize=3 )

            slope, intercept, r_value, p_value, std_err = sps.linregress(time_peaks, cal_peaks)

            plt.plot(time_peaks,intercept+slope*time_peaks)

            ax.set_ylabel("Channels")
            ax.set_xlabel("Time")
            ax.set_title("Time vs. Channels")
            ax.grid(True)

            print("Results from line of fit:")
            print("Slope: "+str(slope))
            print("Standard error on slope: "+str(std_err))
            print("Y-intercept: "+str(intercept))
            print("R^2 value: "+str(r_value**2))

            plt.show()
            
            input("Press enter to continue")
        
        elif choice == "3":
            break
        
        else:
            print("Invalid input")






