#!/usr/bin/env python3

# Import Packages
import sys
import math
import cart2pol
import numpy as np

# Input data types
# n = list
# m = list
# r = np.array
# theta = np.array

# Check and prepare the inputs
def check(n,m,r,theta,norm=True):
    # n and m must be lists (or vectors)
    if len(n) == 1 or len(m) == 1:
        print('[INFO][ZERNIKE]: n and m must be lists with more than 1 element. System exiting...')
        sys.exit()
    # n and m must be the same length
    if len(n) != len(m):
        print('[INFO][ZERNIKE]: n and m must be lists of the same length. System exiting...')
        sys.exit()
    # n and m must differ by multiples of 2
    modulus = list(((n - m) % 2 for n,m in zip(n,m)))
    if all(num % 2 != 0 for num in modulus):
        print('[INFO][ZERNIKE]: n and m must differ by multiples of 2 (including 0). System exiting...')
        sys.exit()
    # m must be less than or equal to its corresponding n value
    if m > n:
        print('[INFO][ZERNIKE]: Each m must be less than or equal to its corresponding n-value. System exiting...')
        sys.exit()
    # All r-values must be between 0 and 1
    if np.any(r < 0) or np.any(r > 1):
        print('[INFO][ZERNIKE]: All r-values must be between 0 and 1. System exiting...')
        sys.exit()
    # r and theta must be lists (or vectors)
    if len(r) == 1 or len(theta) == 1:
        print('[INFO][ZERNIKE]: r and theta must be lists with more than 1 element. System exiting...')
        sys.exit()
    # r and theta must be the same length
    if len(r) != len(theta):
        print('[INFO][ZERNIKE]: r and theta must be lists of the same length. System exiting...')
        sys.exit()
    # Check normalization parameter
    if norm is not True or False:
        print('[INFO][ZERNIKE]: Unrecognized normalization flag. System exiting...')
        sys.exit()
    print('[INFO][ZERNIKE]: Zernike Parameter were successfully checked...')

# Determine the required powers of r
def powers_of_r(n,m):
    abs_m = (list(abs(val) for val in m)) # Converts the m values to absolute values
    r_powers = np.array([],dtype=int) # Create an empty list for the powers of r
    for j in range(0,len(n)):
        r_powers = np.append(np.linspace(m[j],n[j],2,dtype=int),r_powers)
    r_powers = np.unique(r_powers) # Keeps only the unique values in the array
    print('[INFO][ZERNIKE]: Unique powers of r were determined...')
    return r_powers

# Pre-compute the values of r raised to the required powers and compile them in a matrix
def compile(rpowers,r):
    r_powers_list = list(rpowers) # Convert the array to a list
    columns,rows = r.shape[0],len(r_powers_list) # Calculat the number of rows in the final array
    # Check to see if the first element of the 'r_powers_list' is 0, then skip it
    if r_powers_list[0] == 0:
        r_powers_n = np.ones((1,columns))
        if rows > 1: # Greater than 2 'r_powers_list' elements
            for i in range(1,rows):
                next_row = r**r_powers_list[i]
                r_powers_n = np.vstack((r_powers_n,next_row))
    # Otherwise, use all the elements of the 'r_powers_list'
    else:
        r_powers_n = np.array(r**r_powers_list[0])
        if rows > 1: # Greater than 2 'r_powers_list' elements
            for i in range(1,rows):
                next_row = r**r_powers_list[i]
                r_powers_n = np.vstack((r_powers_n,next_row))
    print('[INFO][ZERNIKE]: The required r-values to all r-powers have been pre-compiled...')
    return r_powers_n

# Compute the values of the polynomials
def polynomials(n,m,r_powers,r_powers_n,norm=True):
    abs_m = (list(abs(val) for val in m)) # Converts the m values to absolute values
    for j in range(0,len(n)):
        if len(n) == 1:
            s = [0]
        else:
            s = list(((n-abs_m)/2 for n,abs_m in zip(n,abs_m)))
            s = list(np.int_(np.unique(s)))
        powers = np.array([],dtype=int) # Create an empty list for the powers
        for j in range(0,len(n)):
            powers = np.append(np.linspace(n[j],m[j],2,dtype=int),powers)
            powers = np.unique(powers) # Keeps only the unique values in the array
            powers = list(powers) # Convert the array to a list
            powers.reverse() # Reverse the list order to correct for the -2 needed in the linspace
        for k in range(len(s),0,-1):
            k -= 1 # Used to identify the correct element in the lists
            p = (1-2*(s[k] % 2)) * math.factorial((n[j]-s[k])) / math.factorial(s[k]) / math.factorial(((n[j] - abs_m[j]) / 2-s[k])) / math.factorial(((n[j] + abs_m[j]) / 2-s[k])) # Calculate a new p-value
            idx = (powers == list(r_powers)) # Boolean: Are the 2 lists the same?
            z = p*r_powers_n # Calculation of z
        if norm == True:
            z = z * math.sqrt((1+(m[j] != 0)) * (n[j] + 1)/math.pi)
            print('[INFO][ZERNIKE]: Zernike normalization was successfully performed...')
        else:
            print('[INFO][ZERNIKE]: Zernike normalization was not performed, but processing will continue...')
    print('[INFO][ZERNIKE]: Zernike polynomials were successfully calculated...')
    return z

# Compute the Zernike functions
def zernike(m,z,theta):
    abs_m = (list(abs(val) for val in m)) # Converts the m values to absolute values
    idx_positive = list(i > 0 for i in m) # Positive indices
    idx_negative = list(i < 0 for i in m) # Negative indices
    z = np.where(z>0,z*math.cos(np.asmatrix(theta*abs_m).getH()),z*math.sin(np.asmatrix(theta*abs_m).getH())) # Evaluate only positive terms, else evaluate negative
    print('[INFO][ZERNIKE]: The Zernike function was successfully calculated...')
    print(type(z))
    print('Z should be an array and not a matrix. If it is, I need to fix...')
    return z

# Generate different Zernike modes
def generate_zmodes(n,m,r,theta,total_pixels,NA_pixels):
    x = np.linspace(-total_pixels/NA_pixels,total_pixels/NA_pixels,total_pixels)
    X,Y = np.meshgrid(x,x)
    r = cart2pol.radius(X,Y)
    theta = cart2pol.theta(X,Y)
    idx = (r <= 1)
    check(n,m,r,theta,norm=False)
    r_powers = powers_of_r(n,m)
    r_powers_n = compile(r_powers,r)
    polyZ = polynomials(n,m,r_powers,r_powers_n,norm=False)
    z = zernike(m,polyZ,theta)
    print('[INFO][ZERNIKE]: All Zernike modes were successfully generated...')
    return z
