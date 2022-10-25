#!/usr/bin/env python3

# Calculates the Greatest Common (Even) Denominator

# Import Packages
import sys # System info
import math # Mathematics

# Calculate the factors of a number
def factors(num):
    num_factors = [] # Initiate an empty list
    for denominator in range(8,51): # Loop: denominator values from 25 to 50
        if num % denominator == 0 and denominator % 2 == 0: # Determines factors
            num_factors.append(denominator)
    if len(num_factors) == 0:
        print('[INFO]: No acceptable factors for {}. System exit.'.format(num))
        sys.exit()
    else:
        num_set = set(num_factors)
        return num_factors

# Calculate list of Common Factors (from 2 sets of numbers)
def common_factors(num1,num2):
    width = set(num1) # Convert the list to a set
    height = set(num2) # Convert the list to a set
    if (width & height):
        set_intersect = (width & height) # Calculate the intersection of 2 sets
        list_intersect = list(set_intersect) # Convert the set to a list
        return min(list_intersect) # Smallest value
    else:
        print('[INFO]: No common factors. System exit.') # No common factor
        sys.exit()
