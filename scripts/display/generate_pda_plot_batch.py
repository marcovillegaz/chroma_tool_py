"""
This script creates surface plots from PDA data for J. Vidal.
It processes all PDA files in a given folder.
"""

from src.classes.chromatogram import Chromatogram
from src.display import chroma_plot
import os

# Input and output folders
RAW_PDA_FOLDER_PATH = r"path/to/data"
RAW_FL_FOLDER_PATH = r"path/to/data"
PDA_OUTPUT_FOLDER = r"path/to/data"
FL_OUTPUT_FOLDER = r"path/to/data"

# Ensure output directory exists
if not os.path.exists(PDA_OUTPUT_FOLDER):
    os.makedirs(PDA_OUTPUT_FOLDER)

# Loop through all .txt files in the input folder
total_files = len(os.listdir(RAW_PDA_FOLDER_PATH))

for index, filename in enumerate(os.listdir(RAW_PDA_FOLDER_PATH), start=1):
    print(f"({index}/{total_files}) Processing: {filename}")

    if filename.lower().endswith(".txt"):
        pda_file_path = os.path.join(RAW_PDA_FOLDER_PATH, filename)

        try:
            # Create Chromatogram instance
            chroma = Chromatogram.create_from_pda(pda_file_path)
            print(f"\tChromatogram name: {chroma.NAME}")

            # Generate and save plots
            chroma_plot.pda_contour(
                chroma,
                y_max=400,
                z_min=-10000,
                z_max=530000,
                save_path=PDA_OUTPUT_FOLDER,
            )
            chroma_plot.pda_2d(
                chroma,
                wavelengths=[250, 300],  # Modify as needed
                save_path=PDA_OUTPUT_FOLDER,
            )

        except Exception as e:
            print(f"Error processing {filename}: {e}")


# Loop through all .csv files in the input FL folder
total_files = len(os.listdir(RAW_FL_FOLDER_PATH))

for index, filename in enumerate(os.listdir(RAW_FL_FOLDER_PATH), start=1):
    print(f"({index}/{total_files}) Processing: {filename}")

    if filename.lower().endswith(".csv"):
        fl_file_path = os.path.join(RAW_FL_FOLDER_PATH, filename)

        try:
            # Create Chromatogram instance
            chroma = Chromatogram.create_from_fl(fl_file_path)
            print(f"\tChromatogram name: {chroma.NAME}")

            # Generate and save plots
            chroma_plot.fl_plot(chroma, FL_OUTPUT_FOLDER)

        except Exception as e:
            print(f"Error processing {filename}: {e}")
