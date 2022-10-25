#!/usr/bin/env python3

# Import module packages
import os # Operating System
import sys # System Operations
import cv2 # OpenCV
import math # Arithmetic Math
import warnings # System warnings
import numpy as np # Numpy arrays
from tabulate import tabulate # Present tabular data
import matplotlib.pyplot as plt # Matplotlib Plotting

# Resize images: Does NOT preserve the aspect ratio
def imgResize(lowRes,recon):
    width = recon.shape[1] # New width
    height = recon.shape[0] # New height
    dimensions = (width,height) # New image dimensions
    lowRes = cv2.resize(lowRes,dimensions,interpolation=cv2.INTER_AREA) # Image resize
    return lowRes

# Display the
def compRecon(lowRes,recon):
    # Load images
    lowRes = cv2.imread(lowRes,0)
    recon = cv2.imread(recon,0)
    # Resize the lowRes image to match the dimensions of the reconstruction
    lowRes = imgResize(lowRes,recon)
    fig,axs = plt.subplots(1,2) # Generate sub-plot grid
    fig.subplots_adjust(hspace=0.5) # Add additional padding to the sub-plots
    axs[0].imshow(lowRes,cmap='gray') # Plot reference image
    axs[0].set_title('2x Monochrome Brightfield Image') # Add a title to the subplot
    axs[0].axis('off') # Turn off axis
    axs[1].imshow(recon,cmap='gray') # Plot new image
    axs[1].set_title('20x Monochrome Reconstruction') # Add a title to the subplot
    axs[1].axis('off') # Turn off axis
    plt.show()

if __name__ == '__main__':
    compRecon('./human_center.tiff','./human_center_reconstruction.tiff')
