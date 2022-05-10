#last updated 9/17/21 by Isaiah Mumaw

#import modules
from scipy.stats import skewnorm
import numpy as np
import matplotlib.pyplot as plt


def convert(filepath,num_channels,threshold=2,range_min=0,range_max=1000000000):
    """Converts .csv file to a readable format
    
    Parameters:
        filepath (string): filepath of csv file
        num_channels (int): number of channels being analyzed
        threshold (int, optional): filters out counts less than this value
    
    Returns:
        raw_data (array): 1D array, data as listed in .csv file
        data (array): 1D array, lists channels once per count
    """
    
    fin = open(filepath,"r")
    raw_data = np.zeros((2,num_channels),dtype=int)     #empty array for data
    
    #cycle through imported data - create array with channels vs. counts
    for (i,row) in enumerate(fin):
        
        #skip first row, not needed for this
        if (i!=0):
            
            row = row.strip()
            row = row.split(",")
            
            channel = int(row[0])
            count = int(row[1])
            
            raw_data[0,i-1] = channel
          
            if count>=threshold and ((i-1)>=range_min) and ((i-1)<=range_max):
                raw_data[1,i-1] = count
    
    #now create an array where each channel is listed once per count
    data = np.empty(sum(raw_data[1]),dtype=int)
    index = 0
    
    #populate array
    for (i,value) in enumerate(raw_data[1]):    #cycle through count set
        for j in range(value):                  #cycle through each count
            data[index+j] = raw_data[0,i]       #list channel associated with count
        index+=value                            #move marker to prevent overwrite
    
    return raw_data, data


def get_fit(data,num_channels,resolution=100):
    """Fits skewed Gaussian curve to data
    
    Parameters:
        data (array): data array from convert()
        num_channels (int): number of channels being analyzed
        resolution (int, optional): number of points to calculate per channel
        
    Returns:
        skew (array): array of points used for skew-Gaussian y-axis
        pts (array): array of points used for skew-Gaussian x-axis
        skew_val (float): amount of skew
        mean (float): mean of data
        var (float): variance (std) of data
    """
    
    skew_val,mean,var = skewnorm.fit(data)
    
    pts = np.linspace(0,num_channels-1,resolution*num_channels)
    skew = skewnorm.pdf(pts,skew_val,mean,var)
    
    return skew,pts,skew_val,mean,var



def plotter(data=0,fit=0,pts=0,pltdata=True,pltfit=True,data_label="Data",fit_label="Fit",title="Counts vs channels"): 
    """Plots results
    
    Parameters:
        data (array): array of raw data
        gauss (array): array for Gauss fit
        pts (array): array of points used for Gauss fit
        num_channels (int): number of channels being analyzed
        
    Returns:
        None
    """
  
    fig, ax1 = plt.subplots()
    ax1.set_xlabel("Channel")
    ax1.set_ylabel("Counts")
    
    if pltdata:
        ax1.plot(data[0],data[1],label=data_label,color="tab:red")
        ax1.legend(loc="upper left")
        
    ax2 = ax1.twinx()
    ax2.set_ylabel("Probability Density")
        
    if pltfit:
        ax2.plot(pts,fit,label=fit_label,color="tab:blue")
        ax2.legend(loc="upper right")
        
    ax2.legend(loc="upper right")
    plt.title(title)
    
    plt.show()
    
    return
