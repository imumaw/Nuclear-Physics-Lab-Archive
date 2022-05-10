import lab_3 as l3

data,array,err = l3.IEC_to_array("/Users/isaiahmumaw/Documents/College/Fall 2021/Modern Phys Lab/Lab 3/time_cal.IEC")

f = open("/Users/isaiahmumaw/Documents/College/Fall 2021/Modern Phys Lab/Lab 3/time_cal.csv", "w")

for i in range(len(data[0])):
    f.write(str(data[0,i])+","+str(data[1,i])+"\n")

f.close()