#last updated 10/27/21 by Isaiah Mumaw

#import modules
import numpy as np
import scipy.optimize as sp_opt
import matplotlib.pyplot as plt
import time

##############################################################################
###########################   PRIMARY FUNCTIONS   ############################
##############################################################################

def IEC_to_array(filepath):
    """Converts .IEC file to a numpy array (IEC1455 standard). Includes scaling if needed.
    
    Parameters:
        filepath (string): filepath of iec file of raw data
    
    Returns:
        data (array): 2D array of data
        scale_array (array): 2D array of scaling factors
    """
    
    try:
        fin = open(filepath,"r")
    except:
        print("File Path Error: File not found")
        return None, None, "Error"
    
    if ".IEC" not in filepath:
        print("File Type Error: File must be of .IEC type")
        fin.close()
        return None, None, "Error"
    
    #set up variables
    at_data=False
    at_scale=False
    num_scale_pts=0
       
    #get all the information from the file
    for (i,row) in enumerate(fin):
        
        #get number of channels
        if i==1:
            row_arr = row_to_array(row)
            num_channels = int(row_arr[-1])
            data = np.zeros((2,num_channels),dtype=float)     #empty array for data
        
        #scaling portion of IEC
        elif "A004SPARE" in row:
            at_scale=True
            scale_array=np.zeros((2,25))  #include extra spot for condition later
        
        #get scaling information
        elif at_scale and "A004" in row:
            row_arr = row_to_array(row)
            
            for i in [0,2]:
                channel=float((row_arr[2+i]))
                energy=float(row_arr[1+i])
                
                if (channel==0 and energy==0) or (num_scale_pts==24):
                    at_scale=False
                
                else:
                    scale_array[0,num_scale_pts]=channel
                    scale_array[1,num_scale_pts]=energy
                    num_scale_pts+=1
        
        #data portion of IEC
        elif "A004USERDEFINED" in row:
            at_data = True
            at_scale=False
            
        #collect all data
        elif at_data and "A004" in row:
            row_arr = row_to_array(row)
            index = int(row_arr[1])
            
            for offset in range(5):
                if index+offset>=num_channels:
                    break
                data[0,index+offset] = float(index+offset)
                data[1,index+offset] = float(row_arr[2+offset])

    fin.close()

    return data, scale_array, "None"

##############################################################################
##############################################################################

def scale_data(data,scale_array):
    """Scales x axis of data based on scaling array. Data points between points of array are scaled linearly.
    Data below scaling array is scaled to 0, and data above it is scaled to most recent points.
    
    Parameters:
        data (2D array): numpy array where first row is x-axis and second row is y-axis
        scale_array (2D array): numpy array with the first row being old x-axis values, and the second row being the corresponding scaled values
    
    Returns
        data (2D array): scaled version of input array
    """
    
    if len(scale_array)==0:
        return data
    
    if len(scale_array)==2:
        factor = scale_array[1,0]/scale_array[0,0]
        data[0] *= factor
        return data
    
    n=0
    
    for (i,current_channel) in enumerate(data[0]):
        
        scale_channel = scale_array[0,n]
        scale_energy = scale_array[1,n]
        
        #condition when we have not exceed scaling range
        if current_channel<=scale_channel:
            
            #condition when we under the scaling range (scale to origin)
            if n==0:
                data[0,i] = (scale_energy/scale_channel)*(current_channel-scale_channel) + scale_energy
            
            #condition when we are between scaling points
            else:
                data[0,i] = ((scale_energy-scale_array[1,n-1])/(scale_channel-scale_array[0,n-1]))*(current_channel-scale_channel) + scale_energy
                
            #advance to next scaling point if needed
            if current_channel==scale_channel:
                n+=1
                
        #condition when we are above scaling range (scale to previous points)
        else:
            data[0,i] = ((scale_energy-scale_array[1,n-1])/(scale_channel-scale_array[0,n-1]))*(current_channel-scale_channel) + scale_energy

    return data

##############################################################################
##############################################################################

def fit_to_curve(data, func, lowerbound=None, upperbound=None):
    """Fits some data to a user-defined curve within given bounds
    
    Parameters:
        data (2D array): numpy array where first row is x-axis and second row is y-axis
        func (function): user-defined function which follows scipy.optimize.curve_fit documentation
        lowerbound, upperbound (float, optional): lower and upper bounds on which x axis points to analyze
    
    Returns:
        params (array): array of parameters for user-defined curve
        covars (array): matrix of covariances for params (see full scipy documentation)
        data (array): 1D array of data
    """
    
    lower=0
    upper=len(data[0])-1

    #error messages
    if lowerbound!=None and upperbound!=None and lowerbound>=upperbound:
        print("Value Error: lowerbound must be less than upperbound.")
        return None
    
    if lowerbound!=None:
        for i in range(upper):
            if data[0,i]>lowerbound:
                break
            else:
                lower=i
    
    if upperbound!=None:
        for i in range(upper,0,-1):
            if data[0,i]<upperbound:
                break
            else:
                upper=i
    
    params, covars = sp_opt.curve_fit(func,data[0,lower:upper],data[1,lower:upper],p0=[850,2.2,0])
    
    return params, covars, data[:,lower:upper]

##############################################################################
##############################################################################

def lab3_plotter(data,params):
    
    plt.plot(data[0],data[1],label="Raw Data")
    
    fit_xpts = np.linspace(data[0,0],data[0,-1],len(data[0])*100)
    fit_ypts = expon_decay(fit_xpts,params[0],params[1],params[2])
    plt.plot(fit_xpts,fit_ypts,label="Fit curve")
    
    return

##############################################################################
##########################   SECONDARY FUNCTIONS   ###########################
##############################################################################

#converts file row to a list
def row_to_array(row):
    row = row.strip()
    row = row.split()
    return row

#decaying exponential function
def expon_decay(x,Coeff,Tau,B):
    return Coeff*np.exp(-1*x/Tau) + B

#convert filepath input to something workable (for Mac)
def fix_filepath(filepath):
    return filepath.replace("\ "," ").strip()

##############################################################################
############################   USER INTERFACE   ##############################
##############################################################################

if __name__ == "__main__":
    
    print("\nProgram started")
    
    while True:
        
        print("\n---------------------------------------------------------------------------")
        
        print("\nSelect one of the following: \n1: Plot raw data with fit line \n2: Exit Program")
        
        choice = input("\nYour choice: ")
        
        try:
            choice = int(choice)
            
            if choice==1:
                filepath = input("\nFilepath of raw data (type or drag/drop): ")
                filepath = fix_filepath(filepath)
                
                data,scale_array,error = IEC_to_array(filepath)
                
                if error=="None":
                    
                    period = float(input("\nPeriod of time calibration (microseconds): "))
                    channels = np.array([55.0554787,114.461088,174.024869,233.714063,
                                         293.065505,352.704687,412.392098,471.785474,
                                         531.409365,591.006519,650.468687,710.20619,
                                         770.109881,829.692895,889.599412,949.480557])
                    
                    if period>0:
                        scale_array = np.zeros((2,len(channels)))
                        
                        for i in range(len(channels)):
                            scale_array[0,i] = channels[i]
                            scale_array[1,i] = period*(i+1)
                        
                        data = scale_data(data,scale_array)
                        
                        bounds = input("\nEnter lower and upper bounds of data to analyze (in microseconds) (separated by spaces): ").split()
                        lower = float(bounds[0])
                        upper = float(bounds[1])
                        
                        params, covars, data = fit_to_curve(data,expon_decay,lowerbound=lower,upperbound=upper)
                        std_dev = np.sqrt(np.diag(covars))
                        
                        title = input("\nEnter a plot title (or press Enter to skip): ")
                        
                        print("\nEquation of fit: A*exp(-x/τ)+B")
                        print("Experimental results::")
                        print("A = %.5f ± %.5f"%(params[0],std_dev[0]))
                        print("τ = %.5f ± %.5f"%(params[1],std_dev[1]))
                        print("B = %.5f ± %.5f"%(params[2],std_dev[2]))
                        
                        lab3_plotter(data,params)
                        
                        plt.xlabel("Decay time (microseconds)")
                        plt.ylabel("Counts")
                        plt.title(title)
                        plt.legend()
                        plt.show()
                        
                        
                    else:
                        print("Value Error: period and channels must be positive, nonzero values")
                
            elif choice==2:
                print("\nExiting program.\n")
                break
            
            else:
                print("\nPlease enter a valid choice.")
                time.sleep(2)
        
        except:
            print("\nPlease enter a valid choice.")
            time.sleep(2)
       
        
        
        
        
        