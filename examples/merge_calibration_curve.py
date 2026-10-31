"""
Calibration Curve Merge

This script takes the peak information of varios channels and rearrenges it
to a single excel file. The script also adds the concentration of the
analytes. The concentration is taken from a separate excel file.
"""

import os
import pandas as pd
from chroma_tool_py.utils import excel


# Function to get concentration based on Chromatogram Name and Peak Name
def get_concentration(row):
    chrom_name = row["Chromatogram Name"]  # e.g., 'B9'
    peak_name = row["Peak Name"]  # e.g., 'BPA'

    # Filter the concentration dataframe
    filtered_concentration = df_concentration[df_concentration["Analite"] == peak_name]

    if not filtered_concentration.empty:
        return filtered_concentration[chrom_name].values[
            0
        ]  # Extract concentration value

    return None  # If no match is found


# pass this to excel.py
def save_chromatogram_sheets(
    df_peaks, files_directory, filename="chromatogram_data.xlsx"
):
    """
    Saves a DataFrame into an Excel file, with each (CH, Peak Name) combination in a separate sheet.

    Parameters:
        df_peaks (pd.DataFrame): DataFrame containing chromatogram data.
        files_directory (str): Directory where the Excel file will be saved.
        filename (str): Name of the output Excel file (default: "chromatogram_data.xlsx").

    Returns:
        str: Full path of the saved Excel file.
    """
    # Ensure the directory exists
    os.makedirs(files_directory, exist_ok=True)
    # Define the full path for the Excel file
    output_filename = os.path.join(files_directory, filename)

    # Create an Excel writer
    with pd.ExcelWriter(output_filename, engine="openpyxl") as writer:
        # Iterate over unique CH-PeakName combinations
        for (ch, peak), group_df in df_peaks.groupby(["CH", "Peak Name"]):
            sheet_name = f"CH{ch}_{peak}"  # Format: CH1_BPA, CH1_4NP, etc.
            group_df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Excel file saved at: {output_filename}")
    return output_filename  # Return the path for reference


# -- Main script starts here --

# Directory containing the files to merge
files_directory = "path/to/Calibration_Curve_Data"  # data not included in repo
concentration_file = r"cc_concentrations.xlsx"
# List of files to merge (without extension)
channels = ["CH1", "CH9", "CH10", "CH11", "CH12", "CH13", "CH14", "CH15"]
# List of columns to extract from each file
extract_cols = ["Acquisition Date", "Chromatogram Name", "CH", "Peak Name", "Area"]

# Merge single channel data
df_peaks = excel.merge(files_directory, channels, extract_cols)
print(df_peaks)

# Read the concentration file
df_concentration = pd.read_excel(os.path.join(files_directory, concentration_file))
print(df_concentration.columns)

# Apply function to each row
df_peaks["Concentration"] = df_peaks.apply(get_concentration, axis=1)
print(df_peaks)

# Save the merged data to an Excel file
save_chromatogram_sheets(df_peaks, files_directory, filename="calibration_curves.xlsx")
print("NOW YOU MUST ANALYZE THE DATA MANUALLY TO ELIMINATE THE OUTLIERS")
