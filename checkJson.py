#!/usr/bin/env python3

# Import Packages
import os
import sys
import math
import custom_math
import numpy as np
from readJson import loadJson

# Scan your FPM Json files to make sure you don't have any errors before doing FPM

# Check your parameter file before beginning your FPM to issues
def config(file,mode):
    data = loadJson(file)
    # Check the values in your config file
    if mode == 'debug':
        print('[INFO][CHECK][CONFIG]: Your {} has been checked. No errors found. Ready for FPM...'.format(file))

# Check your parameter file before beginning your FPM to issues
def led(file,mode):
    if os.path.isfile(file):
        data = loadJson(file)
        totalLEDs = len(data['LEDlist'])
        LEDgap = data['board_specs']['LEDgap']
        LEDheight = data['board_specs']['LEDheight']
        # FOR LOOP: Check the values in your config file
        for i in range(0,totalLEDs):
            if data['LEDlist'][i]['LEDnum'] != '{:03d}'.format(i):
                print('[INFO][CHECK][LED]: LEDlist value: {:03d} is incorrect. Fix the LEDposition file. System exiting...'.format(i))
                sys.exit()
            if data['LEDlist'][i]['x'] % LEDgap != 0:
                print('[INFO][CHECK][LED]: LEDnum {:03d}: x value is incorrect. Fix the LEDposition file. System exiting...'.format(i))
                sys.exit()
            if data['LEDlist'][i]['y'] % LEDgap != 0:
                print('[INFO][CHECK][LED]: LEDnum {:03d}: y value is incorrect. Fix the LEDposition file. System exiting...'.format(i))
                sys.exit()
            if data['LEDlist'][i]['z'] % LEDheight != 0:
                print('[INFO][CHECK][LED]: LEDnum {:03d}: z value is incorrect. Fix the LEDposition file. System exiting...'.format(i))
                sys.exit()
        if mode == 'debug':
            print('[INFO][CHECK][LED]: Your {} has been checked. No errors found. Ready for FPM...'.format(file))
    else:
        print('[INFO][CHECK][LED]: The {} file does not exist. System exiting...'.format(file))
        sys.exit()

# Check your wavevector file
# file = wavevector Json, LEDpos = LED position file
def waveVec(file,LEDpos,mode):
    if os.path.isfile(file):
        data = loadJson(file)
        if data['board_info']['modelNumber'] != LEDpos['board_specs']['modelNumber']:
            return 'gen_waveVec'
        if data['board_info']['LEDheight'] != LEDpos['board_specs']['LEDheight']:
            return 'gen_waveVec'
        if mode == 'debug':
            print('[INFO][CHECK][WAVEVECTORS]: Wavevector file has been processed...')
    else:
        if mode == 'debug':
            print('[INFO][CHECK][WAVEVECTORS]: No wavevector file was found...')
        return 'gen_waveVec'
