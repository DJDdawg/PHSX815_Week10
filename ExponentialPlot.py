#! /usr/bin/env python

#Creates Plot of Data

#import packages
import sys
import math
import numpy as np
import matplotlib.pyplot as plt

# import our Random class from python/Random.py file
sys.path.append(".")
import Random as rng

# main function
if __name__ == "__main__":
   
    haveInput = False

    for i in range(1,len(sys.argv)):
        if sys.argv[i] == '-h' or sys.argv[i] == '--help':
            continue

        InputFile = sys.argv[i]
        haveInput = True
    
    if '-h' in sys.argv or '--help' in sys.argv or not haveInput:
        print ("Usage: %s [options] [input file]" % sys.argv[0])
        print ("  options:")
        print ("   --help(-h)          print options")
        print ("   -Beta [float number]  Shape Parameter of the Exponential Distribution. Inverse of the rate parameter.")
        print
        sys.exit(1)
    
    Beta = 1.0
    
    if '-Beta' in sys.argv:
        p = sys.argv.index('-Beta')
        ptemp = float(sys.argv[p+1])
        Beta = ptemp
    
    data = [] # will turn 2D array into 1D array
    
    Nmeas = 1 #Will redefine later. 
    Nexp = 0 #will count 1 by 1. Each new line in data file is a new experiment.
    
    #Count total number of measurements and experiments
    with open(InputFile) as ifile:
        for line in ifile: #Each line is a new experiment. 
            lineVals = line.split() #Each experiment.
            Nmeas = len(lineVals) #Each experiment has Nmeas measurements.
            
            for v in lineVals: #each measurement in an experiment.
               val = float(v) 
               data.append(val) #each measurement in the 2D array gets fed into a 1D array.

            Nexp += 1 

    #Calculate total amount of measurements throughout all experiments
    Ntot = Nmeas * Nexp
   
    #Print out data to see if working correctly
    #print(data) 
    
#Create graph of data
    data = np.asarray(data)
    
    n, bins, patches = plt.hist(data, 16, edgecolor = 'black', linewidth = 3, density = True, facecolor = 'orange', alpha=0.75)
    
#Plot actual curve
    x = np.linspace(0, 5, 1000)
    y = []
    
    def f(x):
        f = 1/Beta * np.exp(-x/Beta)
        return f 
        
    for i in range(len(x)):
         y.append(f(x[i]))
    
    plt.plot(x, y, color = 'blue', label = 'Exponential Curve')
    
# plot formating options
    plt.xlabel('x', fontsize = 15) 
    plt.ylabel('P(x | $\\beta$)', fontsize = 15)
    plt.title('Exponential Distribution', fontsize = 20)
    
    plt.legend(loc = 'upper right')
    plt.grid(True)
    
    plt.show()
