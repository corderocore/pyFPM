#!/usr/bin/env python3

# Import Packages
import os # Operating system
import sys # System operations
import math # Mathematics
import json # JSON parser
import getpass # Get user info
import datetime # Time and date

# LED System Parameters
outputPath = './dataset_004/'
outputfilename = 'LEDpositions.json'
spiral_direction = 'clockwise' # 'clockwise' or 'countercw'
first_step = 'down' # 'left', 'right', 'up', 'down'
LEDgap = 2.5 # Distance between adjacent LEDs (millimeters)
LEDheight = 49.81 # Distance between the LED panel and sample (millimeters)
arraySize = 17 # Total LEDs per row OR column
arrayTotal = arraySize**2 # Total LEDs in the array

# Program Parameters
counter = 0 # Sets the counter to zero
counterMax = arrayTotal - 1 # Total movement operations
#x_origin,y_origin = -7.44e-2,2.4e-3 # Translational misalignment of the origin
x_origin,y_origin = 0.000,0.000
center = int((arraySize - 1) / 2)
row,column = 0,0 # Starting rows/column

# Offsets for non-periodic LED boards
#### NOTE: These must be changed for a non-periodic LED board
offset_x = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0] # Left to Right (17 elements)
#offset_y = [0.1,1.3,0.4,0.6,-0.2,-0.6,0.0,-0.3,0.0,0.2,0.0,-0.7,-1.1,0.5,0.5,0.7,0.9] # Top to Bottom (17 elements)
offset_y = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

# Periodicity: LED layout
period_X = all(elem == 0 for elem in offset_x) # Check for non-zero elements
period_Y = all(elem == 0 for elem in offset_y) # Check for non-zero elements
if period_X == False or period_Y == False:
    pattern = 'nonperiodic'
else:
    pattern = 'periodic'

# Device data for the LED board
data = {}
data['board_specs'] = {}
data['board_specs']
data['board_specs']['board_designer'] = 'Thomas Karl'
data['board_specs']['file_creator'] = 'Cordero Core'
data['board_specs']['owner'] = 'Pathware Inc'
data['board_specs']['fileVersion'] = 1.0
data['board_specs']['modelNumber'] = 'Pi-4_4432_94V-0'
data['board_specs']['generation_date'] = datetime.datetime.now().strftime('%Y/%m/%d') # Year/Month/Day
data['board_specs']['generation_time'] = datetime.datetime.now().strftime('%H:%M:%S') # Hour/Min/Sec
data['board_specs']['username'] = getpass.getuser() # Username
data['board_specs']['board_layout'] = '17x17'
data['board_specs']['board_type'] = pattern
data['board_specs']['LEDgap'] = LEDgap
data['board_specs']['LEDheight'] = LEDheight
data['board_specs']['LEDtotal'] = arrayTotal
# First LED posistion
data['LEDlist'] = [{'LEDnum': '{:03d}'.format(counter),'x': x_origin,'y': y_origin,'z': LEDheight}]

# Determine the order of movements
if spiral_direction.lower() == 'clockwise' and first_step.lower() == 'up':
    print('[INFO]: Clockwise Spiral starting with an upward step...')
    for i in range(0,(arraySize + 1)): # Loop: 1 <= i < 'arraySize'
        if counter < ((arraySize**2) - 1): # If the counter is less than the 'arraySize - 1', then run...
            if i % 2 == 1 and i != arraySize: # If odd, then...
                for up in range(0,i):
                    row += 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
                for right in range(0,i):
                    column += 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
            if i % 2 == 0 and i != arraySize: # If even, then...
                for down in range(0,i):
                    row -= 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1
                for left in range(0,i):
                    column -= 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
            if i == arraySize: # Allows for indexing the "last column" of the image matrix
                for up in range(0,i-1):
                    row += 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
elif spiral_direction.lower() == 'clockwise' and first_step.lower() == 'down':
    print('[INFO]: Clockwise Spiral starting with a downward step...')
    for i in range(0,(arraySize + 1)): # Loop: 1 <= i < 'arraySize'
        if counter < ((arraySize**2) - 1): # If the counter is less than the 'arraySize - 1', then run...
            if i % 2 == 1 and i != arraySize: # If odd, then...
                for down in range(0,i):
                    row -= 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
                for left in range(0,i):
                    column -= 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
            if i % 2 == 0 and i != arraySize: # If even, then...
                for up in range(0,i):
                    row += 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
                for right in range(0,i):
                    column += 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
            if i == arraySize: # Allows for indexing the "last column" of the image matrix
                for down in range(0,i-1):
                    row -= 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
elif spiral_direction.lower() == 'clockwise' and first_step.lower() == 'left':
    print('[INFO]: Clockwise Spiral starting with a leftward step...')
    for i in range(0,(arraySize + 1)): # Loop: 1 <= i < 'arraySize'
        if counter < ((arraySize**2) - 1): # If the counter is less than the 'arraySize - 1', then run...
            if i % 2 == 1 and i != arraySize: # If odd, then...
                for left in range(0,i):
                    column -= 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
                for up in range(0,i):
                    row += 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
            if i % 2 == 0 and i != arraySize: # If even, then...
                for right in range(0,i):
                    column += 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
                for down in range(0,i):
                    row -= 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1
            if i == arraySize: # Allows for indexing the "last column" of the image matrix
                for left in range(0,i-1):
                    column -= 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
elif spiral_direction.lower() == 'clockwise' and first_step.lower() == 'right':
    print('[INFO]: Clockwise Spiral starting with a rightward step...')
    for i in range(0,(arraySize + 1)): # Loop: 1 <= i < 'arraySize'
        if counter < ((arraySize**2) - 1): # If the counter is less than the 'arraySize - 1', then run...
            if i % 2 == 1 and i != arraySize: # If odd, then...
                for right in range(0,i):
                    column += 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
                for down in range(0,i):
                    row -= 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1
            if i % 2 == 0 and i != arraySize: # If even, then...
                for left in range(0,i):
                    column -= 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
                for up in range(0,i):
                    row += 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
            if i == arraySize: # Allows for indexing the "last column" of the image matrix
                for right in range(0,i-1):
                    column += 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
elif spiral_direction.lower() == 'countercw' and first_step.lower() == 'up':
    print('[INFO]: Counter-clockwise Spiral starting with an upward step...')
    for i in range(0,(arraySize + 1)): # Loop: 1 <= i < 'arraySize'
        if counter < ((arraySize**2) - 1): # If the counter is less than the 'arraySize - 1', then run...
            if i % 2 == 1 and i != arraySize: # If odd, then...
                for up in range(0,i):
                    row += 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
                for left in range(0,i):
                    column -= 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
            if i % 2 == 0 and i != arraySize: # If even, then...
                for down in range(0,i):
                    row -= 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
                for right in range(0,i):
                    column += 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
            if i == arraySize: # Allows for indexing the "last column" of the image matrix
                for up in range(0,i-1):
                    row += 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
elif spiral_direction.lower() == 'countercw' and first_step.lower() == 'down':
    print('[INFO]: Counter-clockwise Spiral starting with a downward step...')
    for i in range(0,(arraySize + 1)): # Loop: 1 <= i < 'arraySize'
        if counter < ((arraySize**2) - 1): # If the counter is less than the 'arraySize - 1', then run...
            if i % 2 == 1 and i != arraySize: # If odd, then...
                for down in range(0,i):
                    row -= 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
                for right in range(0,i):
                    column += 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
            if i % 2 == 0 and i != arraySize: # If even, then...
                for up in range(0,i):
                    row += 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
                for left in range(0,i):
                    column -= 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
            if i == arraySize: # Allows for indexing the "last column" of the image matrix
                for down in range(0,i-1):
                    row -= 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
elif spiral_direction.lower() == 'countercw' and first_step.lower() == 'left':
    print('[INFO]: Counter-clockwise Spiral starting with a leftward step...')
    for i in range(0,(arraySize + 1)): # Loop: 1 <= i < 'arraySize'
        if counter < ((arraySize**2) - 1): # If the counter is less than the 'arraySize - 1', then run...
            if i % 2 == 1 and i != arraySize: # If odd, then...
                for left in range(0,i):
                    column -= 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
                for down in range(0,i):
                    row -= 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
            if i % 2 == 0 and i != arraySize: # If even, then...
                for right in range(0,i):
                    column += 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
                for up in range(0,i):
                    row += 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
            if i == arraySize: # Allows for indexing the "last column" of the image matrix
                for left in range(0,i-1):
                    column -= 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
elif spiral_direction.lower() == 'countercw' and first_step.lower() == 'right':
    print('[INFO]: Counter-clockwise Spiral starting with a rightward step...')
    for i in range(0,(arraySize + 1)): # Loop: 1 <= i < 'arraySize'
        if counter < ((arraySize**2) - 1): # If the counter is less than the 'arraySize - 1', then run...
            if i % 2 == 1 and i != arraySize: # If odd, then...
                for right in range(0,i):
                    column += 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
                for up in range(0,i):
                    row += 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
            if i % 2 == 0 and i != arraySize: # If even, then...
                for left in range(0,i):
                    column -= 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
                for down in range(0,i):
                    row -= 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    y = y - LEDgap + offsetY
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
            if i == arraySize: # Allows for indexing the "last column" of the image matrix
                for right in range(0,i-1):
                    column += 1
                    x = (column * LEDgap) + x_origin
                    y = (row * LEDgap) + y_origin
                    data['LEDlist'].append({'LEDnum': '{:03d}'.format(counter + 1),'x': x,'y': y,'z': LEDheight})
                    counter += 1 # Adds the total count
else:
    print('[INFO]: Check your direction and first step inputs. System exiting...')
    sys.exit()

# Non-Periodic Boards ONLY: Adds the offsets to the periodic board values
if data['board_specs']['board_type'] == 'nonperiodic':
    index_list = [] # List of previously used indices
    index_val = int(center) # First index in the list
    # Clockwise and Up
    if spiral_direction.lower() == 'clockwise' and first_step.lower() == 'up':
        print('Hello World')
    # Clockwise and Down
    elif spiral_direction.lower() == 'clockwise' and first_step.lower() == 'down':
        num = 2 # Number of initial steps
        direction = 1 # Direction in the offset list
        i = 0 # LED num
        # While loop
        while i < arrayTotal-1:
    #        for i in range(0,arrayTotal):
            # Previously used indices
            if index_val in index_list:
#                print('LEDnum: ',i,'index: ',index_val,'direction: ',direction,'loops: 1')
                data['LEDlist'][i]['x'] = data['LEDlist'][i]['x'] + offset_x[index_val]
                data['LEDlist'][i]['y'] = data['LEDlist'][i]['y'] + offset_y[index_val]
                i += 1 # Augment i by 1
                # Keep moving the same direction
                if direction > 0:
                    index_val += 1
                elif direction < 0:
                    index_val -= 1
            # Unused indicies
            elif index_val not in index_list and index_val < arraySize - 1:
                for j in range(0,num):
#                    print('LEDnum: ',i,'index: ',index_val,'direction: ',direction,'loops: ',num)
                    data['LEDlist'][i]['x'] = data['LEDlist'][i]['x'] + offset_x[index_val]
                    data['LEDlist'][i]['y'] = data['LEDlist'][i]['y'] + offset_y[index_val]
                    i += 1 # Augment i by 1
                index_list.append(index_val) # Add the current index to the used list
                direction = -direction # Change direction
                index_val = index_val + direction # Change the direction in the list
                num += 1
            # Last index
            elif index_val not in index_list and index_val == arraySize - 1:
                for j in range(0,arraySize):
                    data['LEDlist'][i]['x'] = data['LEDlist'][i]['x'] + offset_x[index_val]
                    data['LEDlist'][i]['y'] = data['LEDlist'][i]['y'] + offset_y[index_val]
                    i += 1
                    if i == arrayTotal:
                        break
                index_list.append(index_val) # Add the index to used list
                index_val -= 1 # Change the direction in the list
            # Sanity check
            else:
                print('[INFO]: Check your direction and first step inputs. System exiting...')
                sys.exit()
    # Clockwise and Left
    elif spiral_direction.lower() == 'clockwise' and first_step.lower() == 'left':
        print('Hello World')
    # Clockwise and Right
    elif spiral_direction.lower() == 'clockwise' and first_step.lower() == 'right':
        print('Hello World')
    # Counterclockwise and Up
    elif spiral_direction.lower() == 'countercw' and first_step.lower() == 'up':
        print('Hello World')
    # Counterclockwise and Down
    elif spiral_direction.lower() == 'countercw' and first_step.lower() == 'down':
        print('Hello World')
    # Counterclockwise and Left
    elif spiral_direction.lower() == 'countercw' and first_step.lower() == 'left':
        print('Hello World')
    # Counterclockwise and Right
    elif spiral_direction.lower() == 'countercw' and first_step.lower() == 'right':
        print('Hello World')
    # Sanity check
    else:
        print('[INFO]: Check your direction and first step inputs. System exiting...')
        sys.exit()

# File Path
outputfile = outputPath + outputfilename

# Write the JSON file
with open(outputfile,'w') as file:
    json.dump(data,file,indent=4)

# Success
print('Your JSON file has been generated...')
