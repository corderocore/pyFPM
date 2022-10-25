#!/usr/bin/env python3

# Import Packages
import os # Operating system
import math # Mathematics
import numpy as np # NUMPY arrays
from skimage.measure import compare_ssim as ssim

# MSE = uses the input image arrays to calculate the average difference in pixel intensity
#### Mean Square Error (MSE) = tells you how close a regression line is to a set of points. It does this by taking the distances from the points
####    to the regression line (these distances are the “errors”) and squaring them
####    The squaring is necessary to remove any negative signs.; it also gives more weight to larger differences
# NOTE: The MSE will be used to calculate the differences between images (creating a threshold and ensuring convergence)
def MSE(ref_img,new_img): # 'ref_img' = reference image, 'new_img' = altered image (Both images must already by NUMPY arrays)
    return abs(np.square(ref_img - new_img).mean()) # https://goo.gl/688J2D

# Peak Signal-to-Noise Ratio (PSNR)
def PSNR(MSE,max_signal): # https://goo.gl/AdUTVn
    if MSE == 0:
        return 100 # Perfect PSNR value expressed in (dB)
    else:
        psnr = 20 * math.log10(max_signal/math.sqrt(MSE)) # https://goo.gl/gbUAxJ
        return psnr # PSNR value expressed in (dB)

# Structural Similarity Index (SSIM)
def SSIM(ref_img,new_img): # https://goo.gl/dHXpjz
    ref_img = np.abs(ref_img)
    new_img = np.abs(new_img)
    return ssim(ref_img,new_img)
