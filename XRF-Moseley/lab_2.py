#last updated 10/5/21 by Isaiah Mumaw

#import modules
from scipy.stats import linregress
from scipy.signal import savgol_filter
import numpy as np
import matplotlib.pyplot as plt

##############################################################################
##############################################################################

def convert(filepath,num_channels,noisepath=False, smooth=False, window=10, degree=2, cal_pts = 6):
    """Converts .iec file to a readable format. Accounts for noise floor
    
    Parameters:
        filepath (string): filepath of iec file of raw data
        num_channels (int): number of channels being analyzed
        noisepath (bool or string): filepath of csv file of noise floor data. If false, does not account for noise
        smooth (bool): whether or not to smooth plot
    
    Returns:
        raw_data (array): 1D array, data as listed in .csv file
    """
    
    fin = open(filepath,"r")
    raw_data = np.zeros((2,num_channels),dtype=float)     #empty array for data
    
    cal_chan = np.zeros(cal_pts+1,dtype=float)
    cal_en = np.zeros(cal_pts+1,dtype=float)
    
    n=1
    at_data=False
       
    #cycle through imported data - create array with channels vs. counts
    for (i,row) in enumerate(fin):
            
        #skip first row, not needed for this
        if (i>=10 and i<=12):
            
            row = row.strip()
            row = row.split()
            
            cal_chan[n] = float(row[2])
            cal_en[n] = float(row[1])
            
            n+=1
            
            cal_chan[n] = float(row[4])
            cal_en[n] = float(row[3])
            
            n+=1
            
        elif "A004USERDEFINED" in row:
            at_data = True
            
        elif at_data and "A004" in row:
            
            row = row.strip()
            row = row.split()
            
            index = int(row[1])
            
            raw_data[0,index+0] = float(index+0)
            raw_data[0,index+1] = float(index+1)
            raw_data[0,index+2] = float(index+2)
            raw_data[0,index+3] = float(index+3)
            raw_data[0,index+4] = float(index+4)
            
            raw_data[1,index+0] = float(row[2])
            raw_data[1,index+1] = float(row[3])
            raw_data[1,index+2] = float(row[4])
            raw_data[1,index+3] = float(row[5])
            raw_data[1,index+4] = float(row[6])
    
    n=1
    
    for (i,element) in enumerate(raw_data[0]):
        
        if element<=cal_chan[n]:
            
            e_n = cal_en[n]
            e_m = cal_en[n-1]
            x_n = cal_chan[n]
            x_m = cal_chan[n-1]
            
            m = (e_n - e_m)/(x_n-x_m)
            
            raw_data[0,i] = m*(element-x_n) + e_n
            
        elif (element>cal_chan[n]) and (n<cal_pts):
            
            n+=1
            
            e_n = cal_en[n]
            e_m = cal_en[n-1]
            x_n = cal_chan[n]
            x_m = cal_chan[n-1]
            
            m = (e_n - e_m)/(x_n-x_m)
            
            raw_data[0,i] = m*(element-x_n) + e_n
            
        else:
            
            e_n = cal_en[n]
            e_m = cal_en[n-1]
            x_n = cal_chan[n]
            x_m = cal_chan[n-1]
            
            m = (e_n - e_m)/(x_n-x_m)
            
            raw_data[0,i] = m*(element-x_n) + e_n
        
      
    if noisepath != False:
      
        noisefin = open(noisepath,"r")
        noisedata = np.zeros((2,num_channels),dtype=float)     #empty array for data
        
        cal_chan = np.zeros(cal_pts+1,dtype=float)
        cal_en = np.zeros(cal_pts+1,dtype=float)
      
        n=1
        at_data=False
           
        #cycle through imported data - create array with channels vs. counts
        for (i,row) in enumerate(noisefin):
                
            #skip first row, not needed for this
            if (i>=10 and i<=12):
                
                row = row.strip()
                row = row.split()
                
                cal_chan[n] = float(row[2])
                cal_en[n] = float(row[1])
                
                n+=1
                
                cal_chan[n] = float(row[4])
                cal_en[n] = float(row[3])
                
                n+=1
                
            elif "A004USERDEFINED" in row:
                at_data = True
                
            elif at_data and "A004" in row:
                
                row = row.strip()
                row = row.split()
                
                index = int(row[1])
                
                noisedata[0,index+0] = float(index+0)
                noisedata[0,index+1] = float(index+1)
                noisedata[0,index+2] = float(index+2)
                noisedata[0,index+3] = float(index+3)
                noisedata[0,index+4] = float(index+4)
                
                noisedata[1,index+0] = float(row[2])
                noisedata[1,index+1] = float(row[3])
                noisedata[1,index+2] = float(row[4])
                noisedata[1,index+3] = float(row[5])
                noisedata[1,index+4] = float(row[6])
        
        n=1
        
        for (i,element) in enumerate(noisedata[0]):
            
            if element<=cal_chan[n]:
                
                e_n = cal_en[n]
                e_m = cal_en[n-1]
                x_n = cal_chan[n]
                x_m = cal_chan[n-1]
                
                m = (e_n - e_m)/(x_n-x_m)
                
                noisedata[0,i] = m*(element-x_n) + e_n
                
            elif (element>cal_chan[n]) and (n<cal_pts):
                
                n+=1
                
                e_n = cal_en[n]
                e_m = cal_en[n-1]
                x_n = cal_chan[n]
                x_m = cal_chan[n-1]
                
                m = (e_n - e_m)/(x_n-x_m)
                
                noisedata[0,i] = m*(element-x_n) + e_n
                
            else:
                
                e_n = cal_en[n]
                e_m = cal_en[n-1]
                x_n = cal_chan[n]
                x_m = cal_chan[n-1]
                
                m = (e_n - e_m)/(x_n-x_m)
                
                noisedata[0,i] = m*(element-x_n) + e_n
            
        
            
        for (i,energy) in enumerate(raw_data[0]):
            neg,pos = find_nearest(noisedata[0],energy)
            
            if neg==pos:
                raw_data[1,i] -= noisedata[1,neg]
            else:    
                raw_data[1,i] -= approximate(noisedata[0,neg],noisedata[0,pos],noisedata[1,neg],noisedata[1,pos],energy)
    
        raw_data[raw_data<0]=0
    
    if smooth:
        
        raw_data[1] = savgol_filter(raw_data[1],window,degree)
        raw_data[raw_data<0]=0
    
    return raw_data

##############################################################################
##############################################################################

def find_nearest(array,val):
    """Finds index of values adjacent to chosen value in numpy array
    """
    
    comparison_array = array-val
    
    neg = np.where(comparison_array<=0)[0]
    pos = np.where(comparison_array>=0)[0]
    
    if len(neg)>0 and len(pos)>0:
        neg = neg[-1]
        pos = pos[0]
    else:
        neg = 0
        pos = 1
    
    return neg,pos

##############################################################################
##############################################################################

def approximate(x1,x2,y1,y2,xval):
    """Linearly approximates the value at point xval given two nearby points
    """
    
    dy = y2-y1
    dx = x2-x1
    
    m = dy/dx
    
    yval = m*(xval-x1) + y1
    
    return yval

##############################################################################
##############################################################################

def convert_3(filepath,num_points):
    """Converts .csv file to a readable format for linear regression function
    
    Parameters:
        filepath (string): filepath of csv file
        num_points (int): number of channels being analyzed
    
    Returns:
        data (array): 1D array, data as listed in .csv file
    """
    
    fin = open(filepath,"r")
    data = np.zeros((3,num_points),dtype=float)     #empty array for data
    
    #cycle through imported data - create array with channels vs. counts
    for (i,row) in enumerate(fin):
        
        #skip first row, not needed for this
        if (i!=0):
            
            row = row.strip()
            row = row.split(",")
            
            channel = float(row[0])
            count = float(row[1])
            error = float(row[2])
            
            data[0,i-1] = channel
            data[1,i-1] = count
            data[2,i-1] = error
    
    return data

##############################################################################
##############################################################################

def plotter(data=0,title=""): 
    """Plots results
    
    Parameters:
        data (array): array of raw data
        title (string): plot title
        
    Returns:
        None
    """
    
    plt.xlabel("Energy (keV)")
    plt.ylabel("Counts")
    
    plt.plot(data[0],data[1],color="tab:blue")

    plt.title(title)
    
    plt.show()
    
    return

##############################################################################
##############################################################################

def get_input():
    
    filepath = input("\nInput filepath for .iec file (or drag/drop file into command terminal): ")
    filepath = filepath.replace("\\ "," ").strip()
    
    
    noisy = input("\nAccount for noise floor? (y/n): ")
    if noisy=="y":
        noise_floor = input("\nInput filepath for .csv file for noise floor: ")
        noise_floor = noise_floor.replace("\\ "," ").strip()
    else:
        noise_floor = False
        
    smoothing = input("\nApply smoothing algorithm (Savitzky-Golay)? (y/n): ")
    if smoothing=="y":
        smooth=True
        window=int(input("Window size (must be odd): "))
        degree=int(input("Polynomial order (must be smaller than window): "))
    else:
        smooth=False
        window=0
        degree=0   
    
    chart_title = input("\nChart title: ")
    
    return filepath, chart_title, noise_floor, smooth, window, degree

##############################################################################
##############################################################################

def get_input_lin():
    
    filepath = input("\nInput filepath for .csv file (or drag/drop file into command terminal): ")
    filepath = filepath.replace("\\ "," ")
    
    num_points = int(input("\nNumber of data points: "))
    
    chart_title = input("\nChart title: ")
    
    return filepath, num_points, chart_title

##############################################################################
##############################################################################

def options(choice):
    
    if choice==1:

        filepath, chart_title, noise_floor, smooth, window, degree = get_input()

        num_channels=4100

        raw_data = convert(filepath,num_channels,noise_floor,smooth,window,degree)
        
        plotter(raw_data,chart_title)
        plt.show()
        
    elif choice==2:
        
        filepath, num_points, chart_title = get_input_lin()
        data = convert_3(filepath, num_points)
        
        scatter_color = "black"
        error_bar_color = "tab:red"
        fit_line_color = "tab:blue" 
        
        fig, ax = plt.subplots()

        x_axis_points = data[0]
        y_axis_points = (data[1]/(4.135667696e-15)/1000)**0.5
        error_values = (data[2]/(4.135667696e-15)/1000)**0.5
        
        plt.errorbar(x_axis_points, y_axis_points,yerr=error_values,
                     fmt=".",color=scatter_color,ecolor=error_bar_color,capsize=5)
        
        slope, intercept, r_value, p_value, std_err = linregress(x_axis_points, y_axis_points)
        plt.plot(x_axis_points,intercept+slope*x_axis_points,color=fit_line_color)
        
        ax.set_xlabel("Atomic Number (Z)")
        ax.set_ylabel("Square Root of Frequency (Hz^0.5)")
        ax.set_title(chart_title)
        ax.grid(True)
        
        print("Results from line of fit:")
        print("Slope: "+str(slope))
        print("Y-intercept: "+str(intercept))
        print("R^2 value: "+str(r_value**2))
        print("Standard error on slope: "+str(std_err))
        
        plt.show()
        
    elif choice==3:
        print("Program ended\n")
        return True
        
    else:
        print("Invalid input!")
    
    return False

##############################################################################
##############################################################################

if __name__ == "__main__":
    
    print("\nProgram started")
    
    quit = False
    
    while not quit:
        print("\n---------------------------------------------------------------------------")
        print("\nSelect one of the following: \n1: Plot raw data \n2: Plot linear data with error bars and fit line \n3: Exit Program")
        choice = input("\nYour choice: ")
        
        try:
            choice = int(choice)
            
        except:
            print("\nInvalid input! Please enter a valid integer.")
            
        quit = options(choice)
        
        
        
        
        
        
        