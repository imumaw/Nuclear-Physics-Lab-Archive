#last updated 10/27/21 by Isaiah Mumaw

#import modules
import numpy as np
import scipy.optimize as sp_opt
import matplotlib.pyplot as plt

###############################################################################
###########################   PRIMARY FUNCTIONS   #############################
###############################################################################


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
        return None, None
    
    if ".IEC" not in filepath:
        print("File Type Error: File must be of .IEC type")
        fin.close()
        return None, None
    
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

    return data, scale_array

###############################################################################
###############################################################################

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
        factor = (scale_array[1,1]-scale_array[1,0])/(scale_array[0,1]-scale_array[0,0])
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

###############################################################################
###############################################################################

def fit_to_curve(data, lowerbound=None, upperbound=None):
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
        return None, None, None
    
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
    
    guess_mean = (data[0,upper]+data[0,lower])/2
    guess_std = guess_mean - data[0,lower]
    guess_norm = max(data[1,lower:upper])
    
    params, covars = sp_opt.curve_fit(gauss,data[0,lower:upper],data[1,lower:upper],p0=[guess_std,guess_mean,guess_norm])
    
    return params, covars, data[:,lower:upper]

###############################################################################
###############################################################################

def csv_to_array(filepath,rows,columns,exclude_first=True):
    
    """Converts csv file to numpy array
    
    Parameters:
        filepath (string): filepath of csv file of raw data
        rows/columns (int): number of rows/columns in csv file
        exclude_first (bool, default True): whether or not to exclude the first row of the file
        
    Returns:
        data (2D array): numpy array of data stored in file
    """
    
    try:
        fin = open(filepath,"r")
    except:
        print("File Path Error: File not found")
        return None, None
    
    if ".csv" not in filepath:
        print("File Type Error: File must be of .csv type")
        fin.close()
        return None, None
    
    data = np.zeros((columns,rows))
    
    for (i,row) in enumerate(fin):
        
        if exclude_first and i==0:
            pass
            
        else:     
            temp = row.split(",")
            
            for j in range(columns):
                value = float(temp[j])
                data[j,i] = value
    
    if exclude_first:
        data = data[:,1:rows]
    
    return data



###############################################################################
##########################   SECONDARY FUNCTIONS   ############################
###############################################################################

E_gamma_theoretical = 662
m = 9.10938356e-31
c = 299792458

#converts file row to a list
def row_to_array(row):
    row = row.strip()
    row = row.split()
    return row

def gauss(x,stnd_dev,mean,norm):
    return norm/( stnd_dev * np.sqrt(2*np.pi) ) * np.exp( ((x-mean)**2) / (-2*stnd_dev**2) )

def energy(theta,E_gamma):
    return E_gamma/(1+(E_gamma/(m*(c**2)*6.242e15))*(1-np.cos(theta)))

#convert filepath input to something workable (for Mac)
def fix_filepath(filepath):
    return filepath.replace("\ "," ").strip()

###############################################################################
############################   USER INTERFACE   ###############################
###############################################################################

if __name__ == "__main__":
    
    print("\nProgram started")
    
    while True:
        
        #try:
        print("\n---------------------------------------------------------------------------")
        print("\nSelect one of the following: \n1: Run raw data analysis \n2: Run fit energy equation \n3: Run cross section plotter \n4: Exit")
        choice = input("\nYour choice: ")
        choice = int(choice)
        
        if choice==1:
            
            filepath = input("\nFilepath of raw data (type or drag/drop): ")
            filepath = fix_filepath(filepath)
            
            data,scale_array = IEC_to_array(filepath)
            data = scale_data(data,scale_array)
            
            trial = input("Trial #: ")
            plt.plot(data[0],data[1])
            plt.title("Trial "+str(trial))
            plt.xlabel("Energy (keV)")
            plt.ylabel("Counts")
            plt.show()
            
            
            while True:
            
                lower, upper = input("Lower and upper bounds of Gaussian analysis: ").split()
     
                params, covars, split_data = fit_to_curve(data, int(lower), int(upper))
                std_devs = np.sqrt(np.diag(covars))
                
                print("\nEXPERIMENTAL RESULTS:")
                print("Mean = %.5f ± %.5f"%(params[1],std_devs[1]))
                print("Std. = %.5f ± %.5f"%(params[0],std_devs[0]))
                print("Total counts = "+str(np.sum(data[1])))
                
                plt.plot(data[0],data[1],label="Raw data")
                
                gauss_x = np.linspace(data[0,0],data[0,-1],1000)
                gauss_y = gauss(gauss_x,params[0],params[1],params[2])
                
                plt.plot(gauss_x,gauss_y,label="Fit curve")
                plt.title("Trial "+str(trial))
                plt.xlabel("Energy (keV)")
                plt.ylabel("Counts")
                plt.legend()
                plt.show()
                
                try_again = input("\nTry fitting again? Yes=1, No=2: ")
                
                if int(try_again)==1:
                    pass
                else:
                    break
        
        elif choice==2:
            
            filepath = input("\nFilepath of calculated data (type or drag/drop): ")
            filepath = fix_filepath(filepath)
            
            data = csv_to_array(filepath,35,6)
            
            plt.errorbar(data[5], data[1], yerr=data[3],
                         fmt="o",capsize=3,label="Experimental energies")
            
            params,covars = sp_opt.curve_fit(energy,data[5]/180*np.pi,data[1],p0=[662])
            std_devs = np.sqrt(np.diag(covars))
            
            rad_angles = np.linspace(0,np.pi)
            deg_angles = rad_angles*180/np.pi
            
            plt.plot(deg_angles,energy(rad_angles,params[0]),label="Experimental fit")
            
            scatter_energy = energy(rad_angles,E_gamma_theoretical)
            plt.plot(deg_angles,scatter_energy,label="Theoretical energies")
            
            plt.legend()
            plt.title("Scattering energies")
            plt.xlabel("Angle (degrees)")
            plt.ylabel("Energy (keV)")
            
            print("\nEXPERIMENTAL RESULTS:")
            print("Initial photon energy = %.5f ± %.5f"%(params[0],std_devs[0]))
            
            plt.figure()
            
            plt.errorbar(data[5], data[1]/E_gamma_theoretical, yerr=data[3]/E_gamma_theoretical,
                         fmt="o",capsize=3,label="Exp. energies")
            
            plt.plot(deg_angles,energy(rad_angles,params[0])/E_gamma_theoretical,label="Exp. fit")
            plt.plot(deg_angles,energy(rad_angles,params[0])/params[0],label="Exp. fit - scaled")
            plt.plot(deg_angles,scatter_energy/E_gamma_theoretical,label="Theoretical energies")
            
            plt.legend()
            plt.title("Scattering energies")
            plt.xlabel("Angle (degrees)")
            plt.ylabel("Ratio (experimental/theoretical")
            
            plt.figure()
            
            plt.scatter(data[5],100*(data[1]/energy(data[5]/180*np.pi,E_gamma_theoretical)-1),label="Exp. energies")
            
            plt.title("Experimental deviation from theoretical results")
            plt.xlabel("Angle (degrees)")
            plt.ylabel("Percent difference")              
 
            plt.show()
            
            
        elif choice==3:
            
            filepath = input("\nFilepath of calculated data (type or drag/drop): ")
            filepath = fix_filepath(filepath)
            
            data = csv_to_array(filepath,35,35)
            
            plt.errorbar(data[5,0:18], data[21,0:18], yerr=data[34,0:18],
                         fmt="o",capsize=3,label="Aluminum rings")
            plt.errorbar(data[5,19:35], data[21,19:35], yerr=data[34,19:35],
                         fmt="o",capsize=3,label="Copper rings")
            
            eff1 = 1.102*np.exp(-2.4408/1000*energy(data[1,0:9]/180*np.pi,676))
            eff2 = 1.102*np.exp(-2.4408/1000*energy(data[1,25::]/180*np.pi,676))
            
            y1 = data[21,0:9]*data[12,0:9]/eff1
            y2 = data[21,25::]*data[12,25::]/eff2
            
            plt.plot(data[5,0:9],y1,label="Aluminum, theoretical",color="red")
            plt.plot(data[5,25::],y2,label="Copper, theoretical",color="black")
            
            plt.legend()
            plt.title("Cross sectional analysis")
            plt.xlabel("Angle (degrees)")
            plt.ylabel("Cross section (cm^2)")
 
            plt.show()           
        
        elif choice==4:
            print("\nExiting program.\n")
            break
        
        #except:
        #    print("\nAn error occurred (and it was probably your fault)")
       
        
        
        
        
        