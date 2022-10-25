#!/usr/bin/env python3

# Import Packages
import os
import json

# Write a JSON file from imported data
def writeJson(data,outputPath,outputFilename):
    # File Path
    outputfile = outputPath + outputFilename
    # Write the JSON file
    with open(outputfile,'w') as file:
        json.dump(data,file,indent=4)
    # Success
    print('[INFO][writeJSON]: Your Json file has been successfully generated...')
