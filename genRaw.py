#!/usr/bin/env python3

# For '.raw' files with no header
# Exchangeable Image File Format (EXIF) = metadata (https://bit.ly/2q1FDcn)

# Import Packages
import os # Operating system
import cv2 # OpenCV
import math # Mathematics
import json # JSON parser
import numpy as np # NUMPY arrays
from warnings import warn # User Warnings
from PIL import Image,ExifTags # Image Processing/EXIF data

# Single files
def single_save(path,filename):
    # Open the image file
    filePath = os.path.join(path,filename) # Absolute file path
    image = Image.open(filePath) # Open the file using PIL
    # Identify and remove the EXIF (metadata)
    data = list(image.getdata()) # Get all image data (EXIF and pixel)
    imageNoExif = Image.new(image.mode, image.size) # Separate the EXIF and pixel data
    imageNoExif.putdata(data) # Put the metadata free data into the image
    rawImage = np.asarray(imageNoExif) # Convert the new image to a NUMPY array
    # Output raw image file
    rawPath = os.path.join(path,'raw_images/') # Absolute path to raw directory
    if not os.path.exists(rawPath): # If the raw image folder does not already exist
        os.mkdir(rawPath) # Generate a new raw image folder
    fname = os.path.join(rawPath,filename)
    base,_ = os.path.splitext(fname) # Base filename without an extension
    rawFile = base + '.raw' # New raw filename
    rawImage.tofile(rawFile) # Write the array data into a binary file
    # Output metadata
    info = image.getexif()
    exif = {}
    exif['image_file'] = {}
    exif['image_file']['original'] = filename
    exif['image_file']['raw'] = os.path.basename(rawFile)
    exif['image_file']['imageSize'] = image.size
    exif['image_exif'] = [ExifTags.TAGS] # Metadata from the image
    # Metadata JSON file
    rawJson = base + '.json' # New raw filename
    with open(rawJson,'w') as outputfile:
        json.dump(exif,outputfile,indent=4)
    print('[INFO]: Your Json file has been successfully generated...')
    print('[INFO]: {} was successfully converted to {}...'.format(filename,os.path.basename(rawFile)))

# Multiple files
def multiple_save(path,ext):
    # Output raw image file
    rawPath = os.path.join(path,'raw_images/') # Absolute path to raw directory
    if not os.path.exists(rawPath): # If the raw image folder does not already exist
        os.mkdir(rawPath) # Generate a new raw image folder
    # Files to find
    ext = '.' + ext.lower() # Prepares the extension
    # Find all files in a directory with a given extension
    for file in os.listdir(path):
        if file.endswith(ext):
            # Open the image file
            filePath = os.path.join(path,file) # Absolute file path
            image = Image.open(filePath) # Open the file using PIL
            # Identify and remove the EXIF (metadata)
            data = list(image.getdata()) # Get all image data (EXIF and pixel)
            imageNoExif = Image.new(image.mode, image.size) # Separate the EXIF and pixel data
            imageNoExif.putdata(data) # Put the metadata free data into the image
            rawImage = np.asarray(imageNoExif) # Convert the new image to a NUMPY array
            fname = os.path.join(rawPath,file)
            base,_ = os.path.splitext(fname) # Base filename without an extension
            rawFile = base + '.raw' # New raw filename
            rawImage.tofile(rawFile) # Write the array data into a binary file
            # Output metadata
            info = image.getexif()
            exif = {}
            exif['image_file'] = {}
            exif['image_file']['original'] = file
            exif['image_file']['raw'] = os.path.basename(rawFile)
            exif['image_file']['imageSize'] = image.size
            exif['image_exif'] = [ExifTags.TAGS] # Metadata from the image
            # Metadata JSON file
            rawJson = base + '.json' # New raw filename
            with open(rawJson,'w') as outputfile:
                json.dump(exif,outputfile,indent=4)
    # Successful completion
    print('[INFO]: All files were successfully converted...')
