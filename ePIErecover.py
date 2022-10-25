#!/usr/bin/env python3

# Import Packages
import cv2 # OpenCV
import math # Mathematics
import zernike # Zernike modes
import numpy as np # NUMPY arrays
import numpy.fft as fft # Fast Fourier Transform
from tabulate import tabulate # Tablulate data
import matplotlib.pyplot as plt # Matplotlib plotting
from custom_math import m_slicing # Custom Matlab functions

# Wavevector with angular components
def angvec(LEDcorr,wavelength):
    k0 = 2*np.pi/wavelength # Angular wavenumber (k) expressed in (radians/meter)
#    num = len(LEDcorr) # Number of corrected LEDs
    Kx,Ky = [],[] # Create empty Kx,Ky lists
#    for i in range(0,num):
#        kx.append(k0 * LEDcorr['LEDdata'][i]['Kx'])
#        ky.append(k0 * LEDcorr['LEDdata'][i]['Ky'])
    return k0,Kx,Ky

# KxKyKz meshgrid
def kMesh(kmax,k0,m,n):
    # Sizes of each KxKy slice
    kx2_slice = kmax/((n-1)/2)
    ky2_slice = kmax/((m-1)/2)
    # Meshgrid
    kxm,kym = np.mgrid[-kmax:kmax:kx2_slice,-kmax:kmax:ky2_slice]
    kzm = np.sqrt(k0**2 - np.square(kxm) - np.square(kym))
    return kxm,kym,kzm


# FPM iterative algorithm
def iterative_algorithm(iterations,arraysize,xROIstart,yROIstart,xROIend,yROIend,roiSizeX,roiSizeY,recon_length,recon_height,
                         dkx,dky,k0,kx_list,ky_list,pixel_ratio,CTF,imageStack,mode):
    # Debug/Development mode
    if mode == 'debug':
        # Display the current CTF
        display_current_ctf = np.zeros((roiSizeX,roiSizeY)) # Current CTF
        image = cv2.normalize(CTF,display_current_ctf,0,1,cv2.NORM_MINMAX)
        table = [] # Empty list for storing tabular data
        headers = ['Image\nNumber','dkx\n(constant)','dky\n(constant)','kx','ky','kxc','kyc','kxL','kyL','kxH','kyH'] # Table headers

    # Convert image size to pixel count
    xpixel = recon_length/pixel_ratio  # Number of pixels along the x-axis of the image
    ypixel = recon_height/pixel_ratio  # Number of pixels along the y-axis of the image

    # Image Recovery
    objectSource  = np.ones((recon_length,recon_height),dtype="int")
    objectRecover = np.asarray(objectSource,dtype="int")  # Initial object init_guess
    objectRecoverFFT = np.fft.fftshift(fft.fft2(objectRecover))

    # Number of iterations through the Fourier spectrum
    for iteration in range(0,iterations):
        if mode == 'debug':
            print('[INFO][ITERATIVE_ALGORITHM] Total Number of Iterations: {}'.format(iterations))
            print('[INFO][ITERATIVE_ALGORITHM]: Press [ANY KEY] to advance through the Fourier display images...')
        objectRecoverLast = np.copy(objectRecover)
        # Iterate through images
        for num in range(0,len(imageStack)):
            # objectArray = imageStack[num][xROIstart:xROIend,yROIstart:yROIend]
            objectArray = imageStack[num]

            # Orient wavevectors in 3D space
            kxc = round(((recon_length)/2 + (k0 * ky_list[num]) / (dkx))+1)
            kyc = round(((recon_height)/2 + (k0 * kx_list[num]) / (dky))-1)
            kxL = round(kxc - (xpixel / 2))
            kxH = round(kxc + (xpixel / 2))
            kyL = round(kyc - (ypixel / 2))
            kyH = round(kyc + (ypixel / 2))

            # Generate Developer Table of Values
            if mode == 'debug':
                table.append(['{:03d}'.format(num),dkx,dky,kx_list[num],ky_list[num],kxc,kyc,kxL,kyL,kxH,kyH])

            # Reconstruction algorithm
            lowResFT =  np.multiply(objectRecoverFFT[kxL:kxH,kyL:kyH],CTF)
            imLowRes = fft.ifft2(fft.ifftshift(lowResFT))
            imLowRes = (pixel_ratio)**2 * np.multiply(objectArray,(np.exp(np.angle(imLowRes) * 1j)))
            lowResFT = np.multiply(fft.fftshift(fft.fft2(imLowRes)),CTF)
            objectRecoverFFT[kxL:kxH,kyL:kyH] = np.add(np.multiply((1 - CTF),objectRecoverFFT[kxL:kxH,kyL:kyH]),lowResFT)

            # Fourier Debugging
            if mode == 'debug':
                # Prepare FFTs for display
                current_imgFFT = np.fft.fftshift(np.log(np.abs(np.fft.fft2(objectArray))+1))
                reconFFT = np.log(np.abs(objectRecoverFFT) + 1)

                # Initialize empty arrays
                display_currentFFT = np.zeros((256,256))
                display_reconFFT = np.zeros((1024,1024))

                # Normalize the images for display
                cv2.normalize(current_imgFFT, display_currentFFT, 0 ,1, cv2.NORM_MINMAX)
                cv2.normalize(reconFFT, display_reconFFT, 0, 1, cv2.NORM_MINMAX)
                # Print FFT information to the screen
                print('[INFO][ITERATIVE_ALGORITHM][IMAGE_NUM]: {:03d}'.format(num + 1))
                print('[INFO][ITERATIVE_ALGORITHM][DATATYPE]: {}'.format(type(display_reconFFT[0][0])))
                print('[INFO][ITERATIVE_ALGORITHM][MAX_VALUE]: {}'.format(display_reconFFT.max()))
                # Convert to 8-bit range for display
                display_currentFFT = display_currentFFT*255
                display_reconFFT = display_reconFFT *255
                display_currentFFT = display_currentFFT.astype('uint8')

                # Display images for debugging errors in the Fourier spectrum
                cv2.imshow("FPM Reconstruction", display_reconFFT.astype('uint8'))
                cv2.imshow("Current Image", objectArray)
                cv2.imshow("Current Image FFT", display_currentFFT.astype('uint8'))
                cv2.waitKey()

                # Print the contents of the FFT sub-region to the screen
                print('[INFO][ITERATIVE_ALGORITHM][SUB_REGION]: {}:{},{}:{}'.format(kxL,kxH,kyL,kyH))
                print(objectRecoverFFT)

        # Intermediate Recovered image
        objectRecover = fft.ifft2(fft.ifftshift(objectRecoverFFT))
        # Clear the table data
        if mode == 'debug':
            print('[INFO][ITERATION]: Iteration Number {:03d}'.format(iteration + 1))
            print(tabulate(table,headers,tablefmt='plain'))
            del table,headers
    # # Turn off images
    if mode == 'debug':
        plt.ioff()
    # Final Recovered Image
    return objectRecover


# FPM iterative algorithm with correction
def iterativeCorr(imageStack,recoveredImage):
    return recoveredImage

# ePIE FPM recovery algorithm
def ePIE(config,LEDcorr,imageStack,wavevectors,systemMag,kx,ky,mode):
    # Define UConn-specified parameters
    p = config['uconn_parameters']['p'] # Scaling factor
    pupil = config['uconn_parameters']['pupil']
    alpha = config['uconn_parameters']['alpha']
    astigx = config['uconn_parameters']['astigx']
    astigy = config['uconn_parameters']['astigy']
    # Patch parameters
    raw_image_size_x = config['image_parameters']['imageSize'][0] # Captured image X
    raw_image_size_y = config['image_parameters']['imageSize'][1] # Captured image Y
    roiSizeX = config['uconn_parameters']['roiSize'] # ROI x dimension
    roiSizeY = config['uconn_parameters']['roiSize'] # ROI y dimension
    z = LEDcorr

    # Image parameters
    pixel_ratio = config['camera_parameters']['pixel_ratio'] # Size ratio between FPM and captured images
    CCDsize = config['camera_parameters']['CCDsize'] # CCD/camera pixel size
    sub_pixel_size = CCDsize/systemMag # Sub-pixel size (post-FPM)
    image_pixel_size = sub_pixel_size/pixel_ratio # Original pixel size
    imageNum = config['image_parameters']['imageNum'] # Total number of images in imageStack
    recon_length = roiSizeX * pixel_ratio
    recon_height = roiSizeY * pixel_ratio
    # Sub-region image capture dimensions
    subImageSize = config['image_parameters']['imageSize'] # Sub-region image dimensions
    subImageSizeX = subImageSize[0] # Image length
    subImageSizeY = subImageSize[1] # Image height
    # ROI cropping
    xROIstart = config['uconn_parameters']['roiX_pixel']
    yROIstart = config['uconn_parameters']['roiY_pixel']
    xROIend = xROIstart + roiSizeX
    yROIend = yROIstart + roiSizeY
    # System parameters
    wavelength = config['fpm_parameters']['wavelength'] # Wavelength of LED array
    objectiveNA = config['fpm_parameters']['objectiveNA'] # Numerical aperture of the objective lens
    iterations = config['runtime_parameters']['maxIterations'] # Number of iterations for the iterative algorithm
    arraysize = config['fpm_parameters']['LEDx'] # LED arraysize***

    # Calculated reconstruction parameters
    # Image parameters
    # m = int(pixel_ratio * roiSizeX) # FPM reconstruction x size
    # n = int(pixel_ratio * roiSizeY) # FPM reconstruction y-size
    m = pixel_ratio * subImageSizeX
    n = pixel_ratio * subImageSizeY
    # Wavevector/pupil parameters
    k0,_,_ = angvec(wavevectors,wavelength) # New angular wavevectors
    kmax = np.pi * image_pixel_size # Maximum value for the wavevector (k)
    dkx = 2 * np.pi / (sub_pixel_size * roiSizeX) # Distance of the kx wavevector
    dky = 2 * np.pi / (sub_pixel_size * roiSizeY) # Distance of the ky wavevector
    kxm,kym,kzm = kMesh(kmax,k0,m,n) # Wavevector meshgrid values
    H2 = 1 # NOTE: Fix defocus distance later
    # Numerical aperture of Fourier illumination (NAfil)
    NAfilx = objectiveNA * (1/wavelength) * n * image_pixel_size
    NAfily = objectiveNA * (1/wavelength) * m * image_pixel_size
    # Initialize the FPM reconstructed image
    # recoveredImage = cv2.resize(imageStack[0][xROIstart:xROIend,yROIstart:yROIend],dsize=(m,n),interpolation=cv2.INTER_NEAREST)
    recoveredImage = cv2.resize(imageStack[0],dsize=(m,n),interpolation=cv2.INTER_NEAREST)
    recoveredFFT = np.fft.fftshift(np.fft.fft2(recoveredImage))
    Mmesh,Nmesh = np.meshgrid(m_slicing(1,roiSizeX,1),m_slicing(1,roiSizeY,1))
    # Zernike corrections
    zn = np.zeros((roiSizeX,roiSizeY)) # Fix for zernike modes later
    # Generate Optical Transfer Function (OTF) mask
    idealFFTMask = np.add(np.square((Nmesh-(roiSizeX+1)/2)/NAfily),np.square((Mmesh-(roiSizeY+1)/2)/NAfilx)) <= 1
    FFTmask = pupil * idealFFTMask

    # FPM reconstruction: Iterative algorithm
    recoveredImage = iterative_algorithm(iterations,arraysize,xROIstart,yROIstart,xROIend,yROIend,roiSizeX,roiSizeY,recon_length,recon_height,dkx,dky,k0,kx,ky,pixel_ratio,FFTmask,imageStack,mode)
    return recoveredImage
