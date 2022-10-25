#!/usr/bin/env python3

# For '.raw' files with no header

# Import Packages
import os # Operating system
import math # Mathematics
import numpy as np # NUMPY arrays
from PIL import Image # Image Processing
from warnings import warn # User Warnings

# Determine data type for a given bit depth
def bit_depth(pixel_depth):
    if pixel_depth != int(pixel_depth):
        print('[INFO]: Bit depth must be an integer. Please check your configuration file. System exiting...')
        sys.exit()
    if pixel_depth >= 1 and pixel_depth <= 8:
        return 'uint8' # 8-bit depth
    elif pixel_depth >= 9 and pixel_depth <= 16:
        return 'uint16' # 16-bit depth
    else:
        print('[INFO]: Unsupported image (unacceptable bit depth). System exiting...')
        sys.exit()

# Calculates the maximum pixel value for a given bit depth
def depth_norm(pixel_depth):
    return int(2**pixel_depth - 1) # Ex. 2^10 - 1 --> 1023

# SINGLE FILE: Open only
def single_open(path,filename,depth,max_pixel,imageShape):
    file = os.path.join(path,filename) # Input '.raw' file
    npimage = np.fromfile(file,dtype=depth) # Convert the raw to an array
    npimage = npimage.reshape(imageShape) # Reshapes the raw data into an array
    return npimage

# MULTIPLE FILES: Open only (https://bit.ly/2krjvGa & https://bit.ly/2q8XvOS)
def multiple_open(path,depth,max_pixel,imageShape):
    iFFTimages = []
    directoryFiles = os.listdir(path)
    directoryFiles.sort() # Good initial sort but does NOT sort numerically very well
    sorted(directoryFiles) # Numerical sort (ascending order)
    for file in directoryFiles: # List all files in the filepath
        if file.endswith('.raw'): # Keep only the '.raw' files
            inputFilename = os.path.join(path,file) # Input '.raw' file
            npimage = np.fromfile(inputFilename,dtype=depth) # Convert the raw to an array
            npimage = npimage.reshape(imageShape) # Reshapes the raw data into an array
            iFFTimages.append(npimage) # Creates a list of the raw images
    return iFFTimages
