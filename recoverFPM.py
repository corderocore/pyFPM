#!/usr/bin/env python3

# Import Packages
import os # Operating system
import sys # System operations
import cv2 # OpenCV
import math # Mathematics
import datetime # Datetime
import wavevector # Generate Kx,Ky data
import custom_math # Custom Matlab math functions
import numpy as np # NUMPY arrays
from ePIErecover import ePIE # expanded PIE method
from readJson import loadJson # Parse Json files
from checkJson import waveVec # Check the wavevector file
import matplotlib.pyplot as plt # Matplotlib plotting

# Recover phase and intensity images
def recover_phase_intensity(recovered_image,mode):
    # Extract image phase (imaginary)
    phase = np.angle(recovered_image)
    # Display the unwrapped (includes negative values) phase
    if mode == 'debug':
        print('[INFO][RECOVER][PHASE]: Press [ANY KEY] to advance...')
        cv2.imshow('Unwrapped Phase',phase)
        cv2.waitKey()
    # Extract image intensity (real)
    intensity = np.abs(recovered_image)
    # Dislay the raw (small dynamic range) intensity
    if mode == 'debug':
        print('[INFO][RECOVER][INTENSITY]: Press [ANY KEY] to advance...')
        cv2.imshow('Raw Intensity',np.uint8(intensity))
        cv2.waitKey()
    # Phase/Intensity dictionary
    return {"PHASE": phase, "INTENSITY": intensity}

# FPM recovery process
def recoverFPM(config,LEDpos,imageStack,mode,saveRecon,path):
    # Argument parsed parameters
    mode = mode
    saveRecon = saveRecon
    path = path

    # Define FPM parameters
    wavelength = config['fpm_parameters']['wavelength'] # LED wavelength
    systemMag = config['fpm_parameters']['systemMag'] # Total system magnification
    objectiveNA = config['fpm_parameters']['objectiveNA'] # Numerical aperture of the objective
    n_glass = config['fpm_parameters']['n_glass'] # Refractive index of glass

    # Define camera parameters
    CCDsize = config['camera_parameters']['CCDsize'] # CCD/camera pixel size
    pixel_ratio = config['camera_parameters']['pixel_ratio'] # Image pixel size
    sub_pixel_size = CCDsize/systemMag # Sub-pixel size (post-FPM)
    image_pixel_size = sub_pixel_size/pixel_ratio

    # Load LED parameters
    LEDpositions = LEDpos['LEDlist']
    LEDgap = config['fpm_parameters']['LEDgap'] # Distance between adjacent LEDs
    LEDx = config['fpm_parameters']['LEDx'] # Number of LEDs in the x-direction
    LEDy = config['fpm_parameters']['LEDy'] # Number of LEDs in the y-direction
    LEDheight = LEDpos['board_specs']['LEDheight'] # Distance between the board and sample
    LEDtotal = config['image_parameters']['imageNum'] # Total LEDs used in the reconstruction

    # Define the image stack parameters
    imageSize = config['image_parameters']['imageSize'] # Image dimensions
    ccdImageSizeX = config['image_parameters']['ccdImageSize'][0] # Image length (ccd_xsize)
    ccdImageSizeY = config['image_parameters']['ccdImageSize'][1] # Image height (ccd_ysize)
    subImageSizeX = config['image_parameters']['imageSize'][0] # Sub-region image dimensions
    subImageSizeY = config['image_parameters']['imageSize'][1] # Sub-region image dimensions
    imageNum = config['image_parameters']['imageNum'] # Total number of images in the stack
    bitDepth = config['image_parameters']['bitDepth'] # Image bit depth

    # Define UConn FPM parameters
    pupil = config['uconn_parameters']['pupil']
    alpha = config['uconn_parameters']['alpha']
    astigX = config['uconn_parameters']['astigx']
    astigY = config['uconn_parameters']['astigy']
    roiX_pixel = config['uconn_parameters']['roiX_pixel']
    roiY_pixel = config['uconn_parameters']['roiY_pixel']
    roiSize = config['uconn_parameters']['roiSize']

    # Output parameters
    outputKxKy = config['output_parameters']['outputKxKy'] # Output Kx,Ky filename

    # Runtime parameters
    method = config['runtime_parameters']['method'] # ePIE, rPIE, FFP
    showRecon = config['runtime_parameters']['showRecon'] # Show the reconstruction after each iteration
    saveRecon = config['runtime_parameters']['saveRecon'] # Save the final reconstruction
    posCorrect = config['runtime_parameters']['positionCorrection'] # Apply positional correction
    threshold = config['runtime_parameters']['threshold'] # Method for determining convergence
    if threshold == 'convergence':
        maxMSE = config['runtime_parameters']['maxMSE']
    else:
        maxIterations = config['runtime_parameters']['maxIterations']

    # Initialize FPM recovery process
    if threshold == 'iterations':
        if mode == 'debug':
            print('[INFO][FPM]: {} iterations will be used to perform FPM reconstruction via {}...'.format(maxIterations,method))
    elif threshold == 'convergence':
        if mode == 'debug':
            print('[INFO][FPM]: FPM reconstruction via {} will continue until a convergence of {} Mean squared error value is reached'.format(method,maxMSE))
    else:
        if mode == 'debug':
            print('[INFO][FPM][WARNING]: No convergence threshold was chosen, so 60 iterations (default) of FPM reconstruction via {} will be performed...'.format(method))
        threshold = 'iterations'
        maxIterations = 20

    # Calculate the patch in the FOV
    x_length = -(((2*roiX_pixel)+(roiSize - 1))/2 - (ccdImageSizeX/2)) # Horizontal length of the patch
    y_length = -(((2*roiY_pixel)+(roiSize - 1))/2 - (ccdImageSizeY/2)) # Vertical height of the patch
    roiY_shift = y_length * sub_pixel_size * 1000 # Y-shift between the center of the ROI and the center of the FOV
    roiX_shift = x_length * sub_pixel_size * 1000 # X-shift between the center of the ROI and the center of the FOV

    # Check to see if a wavevector file exists
    kxkyFile = path + outputKxKy
    if waveVec(kxkyFile,LEDpos,mode) == 'gen_waveVec':
        if mode == 'debug':
            print('[INFO][GENERATE][KxKy]: Generating a new Kx,Ky data file...')
        wavevector.convert(roiX_shift,roiY_shift,LEDpos,n_glass,imageNum,path,outputKxKy)
    # Load the wavevector Json
    wavevectors = loadJson(kxkyFile)
    if mode == 'debug':
        print('[INFO][LOAD][KxKy]: Kx,Ky values were successfully loaded...')

    # Updated runtime parameters
    Kxnew,Kynew,NA_illumination = [],[],[] # Create the new lists
    for i in range(0,len(wavevectors['LEDdata'])):
        Kxnew.append(wavevectors['LEDdata'][i]['Ky']) # Assign Kx to Kx
        Kynew.append(-(wavevectors['LEDdata'][i]['Kx'])) # Assign Ky to Ky
        NA_illumination.append(wavevectors['LEDdata'][i]['NA_illumination']) # Assign NA illumination

    z = 0 # Defocus distance

    # Position Correction (Far-Field Ptychography: FFP)
    if posCorrect == True:
        if mode == 'debug':
            print('[INFO][POSITION_CORRECTION]: FPM will be initiated using position correction...')
        # FPM methods with position correction
        if method == 'ePIE':
            # Display reconstruction during FPM (UNDER CONSTRUCTION)
            if mode == 'debug' or mode == 'prezi':
                recovered_im = ePIE(config,LEDpositions,imageStack,wavevectors,systemMag,Kxnew,Kynew,mode)
            # No reconstruction display
            else:
                recovered_im = ePIE(config,LEDpositions,imageStack,wavevectors,systemMag,Kxnew,Kynew,mode)
            if mode == 'debug' or mode == 'normal':
                print('[INFO][RECOVER][ePIE]: The ePIE FPM process was completed successfully...')
        elif method == 'FFP':
            print('[INFO][RECOVER][FFP]: This function is not currenty supported...')
            sys.exit()
            # if mode == 'debug' or mode == 'normal':
            #     print('[INFO][RECOVER][FFP]: The FFP FPM process was completed successfully...')
        else:
            print('[INFO][RECOVER]: The method is not properly defined. Check the configuration file. System exiting...')
            sys.exit()
    # FPM methods without position correction
    else:
        # FPM methods
        if method == 'ePIE':
            # Display reconstruction during FPM
            if mode == 'debug' or mode == 'prezi':
                recovered_im = ePIE(config,LEDpositions,imageStack,wavevectors,systemMag,Kxnew,Kynew,mode)
            # No reconstruction display
            else:
                recovered_im = ePIE(config,LEDpositions,imageStack,wavevectors,systemMag,Kxnew,Kynew,mode)
            if mode == 'debug' or mode == 'normal':
                print('[INFO][RECOVER][ePIE]: The ePIE FPM process was completed successfully...')
        elif method == 'FFP':
            print('[INFO][RECOVER][FFP]: This function is not currenty supported...')
            sys.exit()
            # if mode == 'debug' or mode == 'normal':
            #     print('[INFO][RECOVER][FFP]: The FFP FPM process was completed successfully...')
        else:
            print('[INFO][RECOVER]: The method is not properly defined. Check the configuration file. System exiting...')
            sys.exit()

    # Define output parameters
    if saveRecon != False:
        # Image recovery
        recovered_dict = recover_phase_intensity(recovered_im,mode=mode)

        # Phase recovery
        phase = recovered_dict["PHASE"]
        reconSize = roiSize * pixel_ratio # Output image size
        phaseOut = np.zeros((reconSize,reconSize)) # Initialize unwrapped phase array
        cv2.normalize(phase,phaseOut,0,255,cv2.NORM_MINMAX) # Normalize the phase
        # Display the unwrapped phase
        if mode == 'debug':
            cv2.imshow('Phase',np.uint8(phaseOut))
            cv2.waitKey()

        # Intensity recovery
        intensity = recovered_dict["INTENSITY"]
        intensityOut = np.zeros((reconSize,reconSize)) # Output image size
        cv2.normalize(intensity,intensityOut,0,255,cv2.NORM_MINMAX) # Normalize the intensity
        # Display the unwrapped phase
        if mode == 'debug':
            cv2.imshow('Intensity',np.uint8(intensityOut))
            cv2.waitKey()

        # Output filepaths
        outputPath = config['output_parameters']['results'] # Output path
        now = datetime.datetime.now() # Current datetime
        outputPhase = os.path.join(outputPath,'phase_{}.tiff'.format(now.strftime("%Y_%m_%d_%H_%M_%S")))
        outputIntensity = os.path.join(outputPath,'intensity_{}.tiff'.format(now.strftime("%Y_%m_%d_%H_%M_%S")))
        # Write the output images
        cv2.imwrite(outputPhase,np.uint8(phaseOut))
        cv2.imwrite(outputIntensity,np.uint8(intensityOut))
    # The reconstructed image will not be saved
    else:
        if mode == 'debug':
            print('[INFO][OUTPUT][MKDIR]: Your reconstruction will not be saved...')
        else:
            pass
