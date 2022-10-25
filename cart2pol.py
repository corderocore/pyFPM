#!/usr/bin/env python3

# Import Packages
import numpy as np

# Input parameters
# XY = the frequency coordinate with pixel unit (not the frequency)
# m/2 + NA(illumination) / lambda * physical size of the object
#### or n/2 + NA(illumination) / lambda * physical size of the object
# And the origin is set at the top left
# XYmid = the middle coordinate of the image, that is [m/2, n/2]

# Output parameters
# R, Th = the distance and theta of circle center from center frequency (pixel, degrees)
# Theta = the distance of circle center from center frequency

# Distance of the center pixel to the center frequency
def radius(meshX,meshY):
    centerDistance = np.hypot(meshX,meshY) # Pixels
    return centerDistance

def theta(meshX,meshY):
    d_theta = np.arctan2(meshY,meshX) # Degrees
    return d_theta
