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
    data = pd.read_excel(file_path, header=1, index_col=0, engine='odf')
except Exception as e:
    print(f"Error: Failed to read the file. Details: {e}")
    sys.exit(1)

# Only looking at the second reading on each sid eof the arm as those are the only complete data sets
filtered_data = data[data.index.str.endswith('2')]

print(filtered_data)
# Save the DataFrame as a CSV file in the same directory
csv_file_path = os.path.splitext(file_path)[0] + '.csv'
try:
    filtered_data.to_csv(csv_file_path)
    print(f"Data successfully saved to '{csv_file_path}'.")
except Exception as e:
    print(f"Error: Failed to save the file as CSV. Details: {e}")
    sys.exit(1)