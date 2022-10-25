#!/usr/bin/env python3

# Import Packages
import os # Operating system
import sys # System operations
import math # Mathematics
import getpass # Get user info
import datetime # Time and date
import numpy as np # NUMPY arrays
from readJson import loadJson # Parse Json files
from writeJson import writeJson # Write Json files

# Input parameters:
# x = LED x-coordinate
# y = LED y-coordinate
# LEDheight = LED z-coordinate
# n_glass = refractive index of glass (1.5)
# translation = LED board translation
# rotation = LED board rotation

# Calculate the corrected Kx and Ky values
def calculate(x0,y0,LEDheight,translation,n_glass):
    LED2origin = math.sqrt(x0**2 + y0**2) # Distance of LED from origin
    theta_LED2origin = math.atan2(y0,x0) # Angle of LED in x-y plane
    x_offset = 0 # Initial guess of where the beam enters the bottom of the slide
    theta_glass = -math.asin(LED2origin/math.sqrt(LED2origin**2 + LEDheight**2)/n_glass) # Get the angle of the beam in glass using Snell's Law
    x_length = translation * math.tan(theta_glass) # Find where the beam exits the top of the slide
    x_offset = x_offset - x_length # Modify the guess where the beam enters the bottom of the slide bby this amount
    # Repeat the above procedure until the beam exits the top of the slide within 1 micron of center
    while abs(x_length) > 0.001:
        theta_glass = -math.asin((LED2origin- x_offset)/math.sqrt((LED2origin - x_offset)**2 + LEDheight**2)/n_glass)
        x_length = x_offset + translation*math.tan(theta_glass)
        x_offset = x_offset - x_length
    # Angle under the glass and angle over the coverslip
    # FPM treats this as the angle in the sample, so it pretends the sample has a refractive index of 1.0
    theta = math.asin((LED2origin - x_offset)/math.sqrt((LED2origin - x_offset)**2 + LEDheight**2))
    NA_t = abs(math.sin(theta))
    Kx = NA_t * math.cos(theta_LED2origin)
    Ky = NA_t * math.sin(theta_LED2origin)
    # Return the following values
    return Kx,Ky,NA_t

# Convert the x,y positions to wavevector (Kx,Ky) data
def convert(x_length,y_length,LEDpos,n_glass,imageNum,path,outputKxKy):
    # Parse necessary LED data
    LEDpositions = LEDpos['LEDlist'] # LED positions
    LEDheight = LEDheight = LEDpos['board_specs']['LEDheight'] # Distance between the board and sample
    # Generate Json dictionary
    data = {}
    data['board_info'] = {}
    data['board_info']['fileVersion'] = LEDpos['board_specs']['fileVersion']
    data['board_info']['modelNumber'] = LEDpos['board_specs']['modelNumber']
    data['board_info']['generation_date'] = datetime.datetime.now().strftime('%Y/%m/%d') # Year/Month/Day
    data['board_info']['generation_time'] = datetime.datetime.now().strftime('%H:%M:%S') # Hour/Min/Sec
    data['board_info']['username'] = getpass.getuser() # Username
    data['board_info']['LEDheight'] = LEDpos['board_specs']['LEDheight']
    data['board_info']['LEDused'] = imageNum
    data['board_info']['Xcenter'] = x_length
    data['board_info']['Ycenter'] = y_length
    data['LEDdata'] = []
    # Collect x,y data
    translation,rotation = 0,0 # t,sita
    for num in range(0,imageNum):
        x0 = x_length + LEDpositions[num]['x']
        y0 = y_length + LEDpositions[num]['y']
        x1 = x0 * math.cos(rotation*math.pi/180) - y0*math.sin(rotation*math.pi/180)
        y1 = x0 * math.sin(rotation*math.pi/180) + y0*math.cos(rotation*math.pi/180)
        LEDheight = LEDpositions[num]['z']
        # Convert x,y positions to corrected Kx,Ky wavevectors
        Ky,Kx,NA_illumination = calculate(x1,y1,LEDheight,translation,n_glass)
        data['LEDdata'].append({'LEDnum': '{:03d}'.format(num),'Kx': Kx,'Ky': Ky,'NA_illumination': NA_illumination})
    # Write output Json file
    writeJson(data,path,outputKxKy)
    print('[INFO][CONVERT][KxKy]: Kx and Ky values were successfully generated...')
