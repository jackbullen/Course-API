#!/usr/bin/env python

import json
import sys

def process_data(input_filenames, output_filename):
    # Process input files and generate output
    
    data = []
    for filename in input_filenames:
        # Open the JSON file and read its contents
        with open(filename, 'r') as json_file:
            json_data = json_file.read()

        # Parse the JSON data into the data list.
        data.append(json.loads(json_data))
    
    # Combine and process the data list
    output_data = dict()
    for courses in data:
        for course in courses['data']:
            output_data[course['id']] = course

    # Write data list to output file
    with open(output_filename, 'w') as f:
        json.dump(output_data, f, indent=4)

if __name__ == "__main__":
    
    if len(sys.argv) < 3:
        print("Usage: json_manage.py <output_filename> <input_file1> <input_file2> ...")
        sys.exit(1)
    
    output_filename = sys.argv[1]
    input_filenames = sys.argv[2:]
    print(output_filename)
    print(input_filenames)
    process_data(input_filenames, output_filename)
