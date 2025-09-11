"""
Plot FL chromatograms.
Usage:
    python plot_fl.py --input <raw_folder> --output <output_folder>
"""

import os
import argparse
from chroma_tool_py.classes import Chromatogram
from chroma_tool_py.display import chroma_plot


def main():
    parser = argparse.ArgumentParser(description="Generate FL chromatogram plots from a batch of FL .csv files stored in a folder")
    parser.add_argument("--input", "-i", required=True, help="Folder containing FL .csv files")
    parser.add_argument("--output", "-o", required=True, help="Folder to save FL plots")

    args = parser.parse_args()
    input_folder = args.input
    output_folder = args.output

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # List .csv files
    files = [f for f in os.listdir(input_folder) if f.lower().endswith(".csv")]
    total_files = len(files)

    # Loop trough each file 
    for index, filename in enumerate(files, start=1):
        print(f"({index}/{total_files}) Processing: {filename}")
        file_path = os.path.join(input_folder, filename)

        try:
            chroma = Chromatogram.create_from_fl(file_path)
            print(f"\tChromatogram name: {chroma.NAME}")

            chroma_plot.fl_plot(chroma, output_folder)

        except Exception as e:
            print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    main()
