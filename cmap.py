#!/usr/bin/env python3

# Import module packages
import os # Operating System
import sys # System Operations
import cv2 # OpenCV
import numpy as np # Numpy arrays

# Apply a color map to set of images
path = './dataset_001/cmap_images'

# Create the output folder
try:
    os.mkdir(path)
except OSError:
    print ('Creation of the directory %s failed' % path)
else:
    print ('Successfully created the directory %s' % path)

# Find all the tiff files
for file in os.listdir('./dataset_001/tiff_images/'):
    if file.endswith('.tiff'):
        inGRAY = cv2.imread(os.path.join('./dataset_001/tiff_images/',file))
        outCMAP = cv2.applyColorMap(inGRAY,cv2.COLORMAP_PARULA)
        cv2.imwrite(os.path.join(path,file),outCMAP)
