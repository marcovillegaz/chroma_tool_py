"""
This script creates surface plots from PDA data for J. Vidal.
It processes all PDA files in a given folder.
"""

import os
from src.classes.chromatogram import Chromatogram
from src.chroma_display import chroma_plot

# Input and output folders
folder_path = r"path/to/data"
output_folder = (
    r"path/to/data"
)

# Ensure output directory exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through all .txt files in the input folder
for filename in os.listdir(folder_path):
    if filename.lower().endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        print(f"Processing: {filename}")

        try:
            # Create Chromatogram instance
            chroma = Chromatogram.create_from_pda(file_path)

            print(f"Chromatogram name: {chroma.NAME}")

            # Generate and save plots
            chroma_plot.pda_contour(
                chroma, y_max=400, z_min=-10000, z_max=530000, save_path=output_folder
            )

            chroma_plot.pda_2d(
                chroma,
                wavelengths=[250, 300],  # Modify as needed
                save_path=output_folder,
            )

        except Exception as e:
            print(f"Error processing {filename}: {e}")
