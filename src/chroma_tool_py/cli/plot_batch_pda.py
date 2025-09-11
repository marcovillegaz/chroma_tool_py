"""
Plot PDA chromatograms with surface and 2D plots.
Usage:
    python plot_pda.py  --input <raw_folder> 
                        --output <output_folder>
                        --mode <contour|2d|both>
                        --wavelengths 250,300
"""

import os
import argparse
from chroma_tool_py.classes import Chromatogram
from chroma_tool_py.display import chroma_plot


def main():
    parser = argparse.ArgumentParser(description="Generate PDA chromatogram plots.")
    # IO arguments
    parser.add_argument(
        "--input", "-i", required=True, help="Folder containing PDA .txt files"
    )
    parser.add_argument(
        "--output", "-o", required=True, help="Folder to save PDA plots"
    )
    # MODE argument
    parser.add_argument(
        "--mode", "-m",
        choices=["contour", "2d", "both"],
        default="both",
        help="Plot mode: contour, 2d, or both (default)"
    )
    # WAVELENGTH argument (only of for "2d" and "both" mode)
    parser.add_argument(
        "--wavelengths", "-w",
        default="250,300",
        help="Comma-separated wavelengths for 2D plots (default: 250,300)"
    )

    args = parser.parse_args()
    input_folder = args.input
    output_folder = args.output
    mode = args.mode
    # Convert comma-separated string to list of floats
    wavelengths = [float(w.strip()) for w in args.wavelengths.split(",")]
    
    # --- Initialization message ---
    print("ChromaToolPy PDA Plotting CLI".center(50,"="))
    print(f"Mode selected: {mode}")
    if mode in ["2d", "both"]:
        print(f"Wavelengths selected for 2D plots: {wavelengths}")
    print(f"Input folder: {input_folder}")
    print(f"Output folder: {output_folder}")
    print("="*50)

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # List .txt files
    files = [f for f in os.listdir(input_folder) if f.lower().endswith(".txt")]
    total_files = len(files)

    for index, filename in enumerate(files, start=1):
        print(f"({index}/{total_files}) Processing: {filename}")
        file_path = os.path.join(input_folder, filename)

        try:
            chroma = Chromatogram.create_from_pda(file_path)
            print(f"\tChromatogram name: {chroma.NAME}")

            if mode in ["contour", "both"]:
                chroma_plot.pda_contour(
                    chroma,
                    y_max=400,
                    z_min=-10000,
                    z_max=530000,
                    save_path=output_folder,
                )
            if mode in ["2d", "both"]:
                chroma_plot.pda_2d(
                    chroma,
                    wavelengths=wavelengths,
                    save_path=output_folder,
                )

        except Exception as e:
            print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    main()
