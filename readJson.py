#!/usr/bin/env python3

# Read information from Json files and '.ini' configuration files

# Import Packages
import json # JSON file parser

# Load a JSON file
def loadJson(filename):
    with open(filename) as json_file: # Open the JSON
        data = json.load(json_file) # Load/parse the JSON
    return data
