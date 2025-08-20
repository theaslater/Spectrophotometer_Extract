import pandas as pd
import argparse
import os
import sys
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

# Read in .ods file and convert to a pandas DataFrame
# Set up argument parser
parser = argparse.ArgumentParser(description='Process an .ods file.')
parser.add_argument('--SP_file', type=str, required=True, help='Path to the .ods file')
parser.add_argument('--PT_file', type=str, required=False, help='Path to the .ods file for participant data')

# Parse the arguments
args = parser.parse_args()
sp_file = args.SP_file
pt_ods_file = args.PT_file

# Error handling
if not os.path.exists(sp_file):
    print(f"Error: The file '{sp_file}' does not exist.")
    sys.exit(1)

if not os.path.exists(pt_ods_file):
    print(f"Error: The participant file '{pt_ods_file}' does not exist.")
    sys.exit(1)

if not sp_file.endswith('.ods'):
    print("Error: The file must have a '.ods' extension.")
    sys.exit(1)

try:
    # Read into pandas DataFrame
    data = pd.read_excel(sp_file, engine='odf')
    participant_data_df = pd.read_excel(pt_ods_file, engine="odf")
except Exception as e:
    print(f"Error: Failed to read the file. Details: {e}")
    sys.exit(1)


participant_data_df = participant_data_df[(
    participant_data_df["MRI_Scanned"] == True) & 
    (participant_data_df["Spectrophotometer"] == True) &
    (participant_data_df["DermaLab"] == True)][["Group"]]


# Swap rows and columns
transposed_data = data.transpose()
#reset the header to have a clean DataFrame
transposed_data.columns = transposed_data.iloc[0]
transposed_data = transposed_data[1:]



# Save the DataFrame as a CSV file in the same directory
csv_file_path = os.path.splitext(sp_file)[0] + '.csv'
try:
    transposed_data.to_csv(csv_file_path)
    print(f"Data successfully saved to '{csv_file_path}'.")
except Exception as e:
    print(f"Error: Failed to save the file as CSV. Details: {e}")
    sys.exit(1)

SCI_tests = np.array(['SCI_L', 'SCI_a', 'SCI_b'])
SCE_tests = np.array(['SCE_L', 'SCE_a', 'SCE_b'])
tests = np.concatenate((SCI_tests, SCE_tests))
sites = np.array(['Dorsal', 'Volar'])

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
for i, test in enumerate(tests):
    ax = axes[i // 3, i % 3]
    dorsal_column = f"D_{test}_2"
    volar_column = f"V_{test}_2"
    dorsal_data = pd.to_numeric(transposed_data[dorsal_column].dropna(), errors='coerce')
    volar_data = pd.to_numeric(transposed_data[volar_column].dropna(), errors='coerce')
    dorsal_data.header = dorsal_column
    volar_data.header = volar_column
    t_test_result = stats.ttest_rel(
        dorsal_data, 
        volar_data
    )
    for participant in transposed_data.index:
        ax.plot([0, 1], [dorsal_data[participant], volar_data[participant]], label=participant, alpha=0.5, color='grey')
    ax.plot([0, 1], [dorsal_data.mean(), volar_data.mean()], label='Mean', linewidth=2, color='red')
    # Add shaded area for standard deviation
    ax.fill_between([0, 1], 
                    [dorsal_data.mean() - dorsal_data.std(), volar_data.mean() - volar_data.std()],
                    [dorsal_data.mean() + dorsal_data.std(), volar_data.mean() + volar_data.std()],
                    color='gray', alpha=0.2, label='Std Dev')
    ax.set_title(f"{test}\nT-test p-value: {t_test_result.pvalue:.4f}")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Dorsal", "Volar"])
    ax.set_ylabel('Value')
plt.tight_layout()
plt.savefig(os.path.splitext(sp_file)[0] + '_comparison.png')