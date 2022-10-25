#!/usr/bin/env python3

# Import Packages
import os # Operating system
import sys # System information
import math # Mathematics
import readRaw # Read in headerless raw images
import argparse # Argument Parser
import numpy as np # NUMPY arrays
import readJson as rjson # Read JSON files
import matplotlib.pyplot as plt # Matplotlib plots
from recoverFPM import recoverFPM # FPM reconstruction
from checkJson import led as checkLED # Check your LED position files
from checkJson import config as checkCONFIG # Check your LED position files

# Construct the argument parser
ap = argparse.ArgumentParser()
ap.add_argument('-path','--folder',default='./',type=str,required=False,help='Folder containing the dataset')
ap.add_argument('-mode','--Mode',default='normal',type=str,required=False,help='prezi,debug, or normal mode (Default: normal)')
ap.add_argument('-save','--saveRecon',default=True,type=bool,required=False,help='Save the reconstructed image (T/F) (Default: True)')
args = vars(ap.parse_args())

# Parse mode/save information
# Prezi mode: Display imageStack and center vs reconstructed images
if args['Mode'].lower() == 'prezi':
    mode = 'presentation'
    saveRecon = True
    print('[INFO]: Presentation mode will be used...')
# Debug/Dev mode: Enable display of all images
elif args['Mode'].lower() == 'debug':
    mode = 'debug'
    saveRecon = True
    print('[INFO]: Debugger mode will be used, and developer tools will be enabled...')
# Normal mode: Only display the final reconstruction
else:
    mode = 'normal'
    try:
        if args['saveRecon'] == True:
            saveRecon = True
            print('[INFO]: The reconstructed image will be saved...')
        elif args['saveRecon'] == False:
            saveRecon = False
            print('[INFO]: The reconstructed image will not be saved...')
    except NameError:
        saveRecon = False
        print('[INFO]: The reconstructed image will not be saved...')
    print('[INFO]: Normal Mode will be used...')

# File location parsing
path = args['folder']
configFile = path + 'config.json'
LEDposFile = path + 'LEDpositions.json'

# Initializing FPM process
print('[INFO]: Initializing the FPM process...')
# Check your configuration file for errors
checkCONFIG(configFile,mode)
# Check your LED position file for errors
checkLED(LEDposFile,mode)

# Load FPM parameters
config = rjson.loadJson(configFile)
if mode == 'debug':
    print('[INFO][CONFIG]: FPM system parameters were successfully loaded...')

# Read in the LED positions
LEDpos = rjson.loadJson(LEDposFile)
if mode == 'debug':
    print('[INFO][LEDpositions]: LED positions were successfully loaded...')

# Load the image stack
imagePath = os.path.join(path,'raw_images/') # Folder for finding the imageStack
# Full sensor image capture dimensions
ccdImageSize = config['image_parameters']['ccdImageSize'] # FOV image dimensions
ccdImageSizeX = ccdImageSize[0] # Image length
ccdImageSizeY = ccdImageSize[1] # Image height
# Sub-region image capture dimensions
subImageSize = config['image_parameters']['imageSize'] # Sub-region image dimensions
subImageSizeX = subImageSize[0] # Image length
subImageSizeY = subImageSize[1] # Image height
# Define the image stack dimensions
if ccdImageSizeX == subImageSizeX and ccdImageSizeY == subImageSizeY:
    imageX,imageY = ccdImageSizeX,ccdImageSizeY # Set the dimensions to the full sensor
else:
    imageX,imageY = subImageSizeX,subImageSizeY # Set the dimensions to the full sensor
# Load the image stack
bitDepth = config['image_parameters']['bitDepth'] # Image bit depth
bitType = readRaw.bit_depth(bitDepth) # uint8 or uint16
bitMax = readRaw.depth_norm(bitDepth) # Maximum pixel value
imageStack = readRaw.multiple_open(imagePath,bitType,bitMax,(imageX,imageY))
if mode == 'debug':
    print('[INFO][LOAD][IMAGES]: Image stack was loaded successfully...')

# Define output parameters
config['output_parameters']['results'] = os.path.join(path,'results') # Add the output path to the config dictionary
outputPath = config['output_parameters']['results']

# Try generating a results directory
if not os.path.exists(outputPath):
    try: # Try making the results folder
        os.mkdir(outputPath,mode=0o777) # Generates a new results folder
    except OSError: # The results folder did not generate properly
        print('[INFO][OUTPUT][MKDIR]: The results folder was not successfully generated. System exiting...')
        sys.exit()
    else: # Prints upon successful folder generation
        if mode == 'debug' or mode == 'normal':
            print('[INFO][OUTPUT][MKDIR]: The results folder was successfully generated...')
# Results folder already exists
else: # If you already have a results folder
    if mode == 'debug' or mode == 'normal':
        print('[INFO][OUTPUT][MKDIR]: The results folder already exists...')

# Presenatation and debug/developer modes
if mode == 'presentation' or mode == 'debug':
    plt.ion() # Interactive mode = on
    plt.plot() # Generates the plot
    # Iterate through the imageStack
    for i in range(0,len(imageStack)):
        # Generate plot
        image = imageStack[i]
        fig = plt.imshow(image) # Show the image
        plt.axis('off') # Turn off the image axes
        fig.axes.get_xaxis().set_visible(False) # Remove x-axis border
        fig.axes.get_yaxis().set_visible(False) # Remove y-axis border
        if mode == 'presentation':
            plt.pause(0.05)
        else:
            plt.pause(0.05)
        # Clear the current image from the memory
        plt.clf()
        del image
        # Only close the window after the last image is displayed
        if i == len(imageStack):
            plt.ioff()
    plt.close('all') # Close all open figures

# FPM reconstruction
recoverFPM(config,LEDpos,imageStack,mode=mode,saveRecon=saveRecon,path=path)

# Process completed
print('[INFO][FPM]: FPM reconstruction has been completed...')
