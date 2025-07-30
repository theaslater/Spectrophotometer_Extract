import pandas as pd
import argparse
import os
import sys

# Read in .ods file and convert to a pandas DataFrame
# Set up argument parser
parser = argparse.ArgumentParser(description='Process an .ods file.')
parser.add_argument('-d', '--dir', type=str, required=True, help='Path to the .ods file')

# Parse the arguments
args = parser.parse_args()
file_path = args.dir

# Error handling
if not os.path.exists(file_path):
    print(f"Error: The file '{file_path}' does not exist.")
    sys.exit(1)

if not file_path.endswith('.ods'):
    print("Error: The file must have a '.ods' extension.")
    sys.exit(1)

try:
    # Read into pandas DataFrame
    data = pd.read_excel(file_path, engine='odf')
except Exception as e:
    print(f"Error: Failed to read the file. Details: {e}")
    sys.exit(1)

