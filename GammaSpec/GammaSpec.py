#by Isaiah Mumaw

#import modules
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

#########################################################################################################

def convert( filepath, calibrate=True, verbose=False ):
    """Converts .iec file to a numpy array
    
    Parameters
        filepath (string) : filepath of iec file of raw data
        calibrate (bool, optional) : if true, includes calibration points in output
        verbose (bool, optional) : if true, includes output for file reading process
    
    Returns
        raw_data (array) : 1D array, data as listed in .csv file
    """
    
    #open file
    fin = open( filepath, "r" )
    
    #init variables
    spare = False
    userdefined = False
    
    #iterate through file to get info
    for ( i, row ) in enumerate( fin ):
        
        #remove A004 prefix
        row = strip_A004( row )
        
        #ROW 0 CONTAINS GENERAL INFO ON DETECTOR -- NOT NEEDED
        
        #ROW 1 CONTAINS RUNTIME AND CHANNEL INFO
        if i==1:

            #get channel from row
            row = str_to_arr( row, dtype=float )
            channels = int(row[-1])
            
            #create raw data array
            raw_data = np.zeros( (2,channels), dtype=float )
            
            #output
            if verbose:
                print( "Number of channels:", channels )
                print( "Data was collected for:", row[0], "seconds.")
       
        #ROW 2 CONTAINS DATE AND TIME INFO
        elif i==2 and verbose:
            print( "Date and time of data collection:",row.strip() )
          
        #ROW 3 TO SPARE CONTAINS MISCELLANEOUS DATA FOR GAMMA SOFTWARE
          
        #SPARE SIGNIFIES CALIBRATION DATA START POINT
        elif "SPARE" in row:
            spare = True
            cal_pts_raw = np.empty(0)
        
        #now get all calibration points
        elif spare:
            
            #get float array form of row
            row = str_to_arr( row, dtype=float )
            
            #append all values
            for ( i, element ) in enumerate( row ):
                
                #check that calibration point exists
                if element==0:
                    spare=False
                    
                    size = np.size( cal_pts_raw )
                    cal_pts = np.empty( (2, int(size/2)) )
                    
                    #reshape to correct format - every other element goes in each row
                    j=0
                    for i in range( len(cal_pts_raw) ):
                        
                        if i%2==0:
                            cal_pts[0][j] = cal_pts_raw[i]
                        
                        else:
                            cal_pts[1][j] = cal_pts_raw[i]
                            j+=1
                                
                    if verbose:
                        print("Calibration points:",cal_pts)
                        
                    break
                
                cal_pts_raw = np.append( cal_pts_raw, element )
                    
        elif "USERDEFINED" in row:
            userdefined = True
        
        elif userdefined:
            row = str_to_arr( row, dtype=int )
            index = row[0]
            
            for i in range(5):
                if index+i < channels:
                    raw_data[0][index+i] = index+i
                    raw_data[1][index+i] = row[i+1]
    
    if verbose:
        print( "Data:", raw_data )
            
    if calibrate:
        return raw_data, cal_pts
    
    else:
        return raw_data

#########################################################################################################

def strip_A004( in_string ):
    """Removes leading A004 from IEC line"""
    
    return in_string.strip("A004")

#########################################################################################################

def str_to_arr( in_string, dtype=str ):
    """Converts string to array. Optionally switches data type
    
    Parameters:
        in_string (string) : input string to be converted
        dtype (data type, optional) : type of output elements. Defaults to string
        
    Returns:
        arr (array): numpy array containing the line
    """
    
    line = in_string.strip()
    line_arr = line.split()
    
    arr = np.empty( len(line_arr), dtype=dtype )
    
    for ( i, element ) in enumerate( line_arr ):
        arr[i] = dtype(element)
    
    return arr

#########################################################################################################

def calibrate( raw_data, cal_pts ):
    
    dat = linregress(cal_pts[0], cal_pts[1])
    
    raw_data[0] *= dat[0]
    raw_data[0] += dat[1]
    
    return raw_data, dat

#########################################################################################################

filepath = input("Filepath: ")

raw_data, cal = convert(filepath)

data, dat = calibrate( raw_data, cal )

print( dat )

plt.figure("Linear plot")
plt.plot( data[0], data[1] )
plt.xlabel("Energy (keV)")
plt.ylabel("Counts")

plt.figure("Log plot")
plt.plot( data[0], data[1] )
plt.xlabel("Energy (keV)")
plt.ylabel("Counts")

ax = plt.gca()
ax.set_yscale("log")

plt.show()