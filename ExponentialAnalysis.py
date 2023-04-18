#! /usr/bin/env python

#Import packages
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

# import our Random class from python/Random.py file
sys.path.append(".")
import Random as rng


# main function for our Analysis
if __name__ == "__main__":
    # if the user includes the flag -h or --help print the options
    if '-h' in sys.argv or '--help' in sys.argv:
        print ("Usage: %s [options]" % sys.argv[0])
        print ("  options:")
        print ("   --help(-h)          print options")
        print ("   -input0 [filename]  name of data file ")
        print ("   -Beta [float number]  Shape Parameter of the Exponential Distribution")
        print
        sys.exit(1)
        
    #Initialize Variables
    Beta = 1.0 #shape parameter. Beta = 1/lambda where lambda is the rate parameter
    Nmeas = 0 
    Nexp = 0 #will count 1 by 1. Each new line in data file is a new experiment.
    
    #System Inputs          
    if '-input0' in sys.argv:
        p = sys.argv.index('-input0')
        InputFile0 = sys.argv[p+1]

    if '-Beta' in sys.argv:
        p = sys.argv.index('-Beta')
        ptemp = float(sys.argv[p+1])
        Beta = ptemp
           
    #Analyze Data
    data_0 = [] # array of lists. Each list is an experiment.
    
    #Count Nmeas and Nexp
    with open(InputFile0) as ifile:
        for line in ifile: #Each line is a new experiment. 
            lineVals = line.split() #All measurements in one experiment
            Nmeas = len(lineVals) #Each experiment has Nmeas measurements and is constant.       
            
            data_exp = [] #gets reset each time. 
            
            for v in lineVals: #all measurements in a single experiment
               val = float(v) #turns string into float
               data_exp.append(val) #each measurement gets fed into a temporary 1D array.
               
            data_0.append(data_exp) #feed in list of a single experiment into this list.
            
            Nexp += 1

    #Print out results to see if correct
    #print(data_0[0]) #First experiment
     
    print(f"Number of experiments: {Nexp}")
    print(f"Number of measurements/experiment: {Nmeas}")
    
    #log likelihood for a single experiment 
    current_exp = 0 #experiment 1
    
    def f(x):
        f = 0 #initialize value
        
        for d in data_0[current_exp]: #measurements in a single experiment
            f += np.log(1/Beta) - 1/Beta * d
        
        return -1 * f #need to return the negative in order to use minimization package.
    
    #analytical solution for maximum log likelihood
    x_an = Beta #Beta is the mean of the graph
    y_an = f(x_an) 
    
    print(f"Log likelihood is maximized at (x = {x_an}, y = {y_an}) for the analytical solution")

    #numerical solution for single experiment (experiment 1)
    result = optimize.minimize_scalar(f)
    
    print(f'Scipy minimization was successful: {result.success}') # check if solver was successful

    x_num = result.x #the numerical solution for the mean for a single experiment
    print(f'numerical x-value found to maximize log likelihood for experiment 1: {x_num}')
    
    num_result = -1 * f(x_num) #normalization factor for graph below
    
    #Log Likelihood curve
    x = np.linspace(0, 3.0, 100)
    y= []
    
    #true value
    x2 = []
    y2 = np.linspace(0, 3, 100)
    
    #Initializtion for error analysis
    yerrlo = 0.5
    yerrhi = 0.5
    xerrlo = 0.
    xerrhi = 0.
    
    for i in range(len(x)):
        y.append(f(x[i]) + num_result)
        
        x2.append(x_an) #need an array of all the same values to plot a vertical line on the graph.
        
        #find lower bound for 1 sigma error bar
        if x[i] < x_num:
            if np.abs(y[i] - 1./2.) < yerrlo:
                yerrlo = np.abs(y[i] - 1./2.)
                xerrlo = x[i]
        
        #find upper bound for 1 sigma error bar
        if x[i] > x_num:
            if np.abs(y[i] - 1./2.) < yerrhi:
                yerrhi = np.abs(y[i] - 1./2.)
                xerrhi = x[i]  

    #Numerical error bars on x for a single experiment 
    sig_num = (xerrhi - xerrlo)/2 
    
    #print(f'Uncertainty of numerical solution for experiment 1: {sig_num}')
    print(f'Numerical value of the Shape Parameter for experiment 1: {x_num} ± {sig_num}')
    print(f'68% CI of numerical solution for experiment 1: [{xerrlo}, {xerrhi}]')
    
    #plot of Log Likelihood for a single experiment 
    plt.plot(x, y, label = 'Numerical Evaluations')
    plt.plot(x2, y2, color = 'red', label = 'True Value')
    plt.errorbar(x_num, 0, xerr = sig_num, color = 'green', marker = 'v', label = '68% CI for Numerical Value')
    
    plt.xlabel('Shape Parameter')
    plt.ylabel('Normalized Log Likelihood')
    plt.title('Log Likelihood for Values of the Shape Parameter')
    
    plt.grid()
    plt.legend(loc = 'upper right')
    plt.show()
    
    #calculate Shape parameter and standard deviation of all experiments
    result_list = [] #list of all means 
    
    Mean_exp = 0
    Mean_exp_squared = 0
    
    for exp in range(0, Nexp):
        current_exp = exp
        result = optimize.minimize_scalar(f) #result for each experiment
        result_list.append(result.x) #append result to list
        
        Mean_exp += result.x
        Mean_exp_squared += result.x * result.x
      
    Mean_exp = Mean_exp/Nexp 
    Mean_exp_squared = Mean_exp_squared/Nexp
      
    Sigma_exp = np.sqrt(Mean_exp_squared - Mean_exp**2)

    print(f'Numerical Mean value of all experiments: {Mean_exp} ± {Sigma_exp}')
    
    #Histogram of all means
    data = np.asarray(result_list)
    n, bins, patches = plt.hist(data, 16, edgecolor = 'black', linewidth = 3, density = False, facecolor = 'orange', alpha=0.75)
    
    #plot Mean_exp and Sigma_Exp on histogram
    
    plt.xlabel('$\\beta$', fontsize = 15)
    plt.ylabel('Number of Experiments', fontsize = 15)
    plt.title('Measured Shape Parameter from Experiments', fontsize = 20)
    
    plt.grid(True)
    plt.show()   
    
    #Graph of how Sigma_exp changes as Nmeas increases
    
    
    
    
    
