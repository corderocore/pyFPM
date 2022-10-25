#!/usr/bin/env python3

# Import Packages
import cv2 # OpenCV
import readRaw # Load raw images
import numpy as np # NUMPY array
import matplotlib.pyplot as plt # Matplotlib plot

# Display a pre-loaded image (https://bit.ly/2mpKm62)
def display(image,bitDepth,title='Image',time=0):
    # Handles images larger than 8-bit
    if bitDepth > 8 and image.dtype == 'uint16':
        pRatio = 2**(bitDepth-8) # Pixel normalization ratio
        scaled_image = (image/pRatio).astype('uint8') # Generates a scaled image
        cv2.imshow(title, scaled_image)
        cv2.waitKey(time)
    # Display 8-bit images
    elif image.dtype == 'uint8':
        cv2.imshow(title, image)
        cv2.waitKey(time)
    else:
        print('[INFO][FPM][SHOWIMAGE]: Error in image display...')

# Load and display a SINGLE raw image
def idisplayRaw(imagePath,imageFilename,depth,yxDimension,figsize=(4,3)):
    # Image parameters
    bitDepth = readRaw.bit_depth(depth)
    maxPixel = readRaw.depth_norm(depth)
    image = readRaw.single_open(imagePath,imageFilename,bitDepth,maxPixel,yxDimension)
    # Generate plot
    fig = plt.imshow(image) # Show the image
    plt.axis('off') # Turn off the image axes
    fig.axes.get_xaxis().set_visible(False) # Remove x-axis border
    fig.axes.get_yaxis().set_visible(False) # Remove y-axis border
    plt.show(block=True) # Stops the program until the image is closed

# Load and display a SET of raw images
def idisplayRaws(imagePath,depth,yxDimension,figsize=(4,3)):
    # Image parameters
    bitDepth = readRaw.bit_depth(depth)
    maxPixel = readRaw.depth_norm(depth)
    # Load images
    imageStack = readRaw.multiple_open(imagePath,bitDepth,maxPixel,yxDimension)
    imageNum = len(imageStack)
    # Prepare Matplotlib window
    plt.ion() # Interactive mode = on (https://bit.ly/2l82O2z)
    plt.figure(figsize=figsize) # Set figure size (https://bit.ly/2mDJj2t)
    plt.plot() # Generate plot
    # Loop over the images
    for i in range(0,imageNum):
        # Generate plot
        fig = plt.imshow(imageStack[i]) # Show the image
        plt.axis('off') # Turn off the image axes
        fig.axes.get_xaxis().set_visible(False) # Remove x-axis border
        fig.axes.get_yaxis().set_visible(False) # Remove y-axis border
#        print('Image: {:03d}'.format(i))
        plt.pause(0.05)
