"""chroma_plot3.py
This script creates a plot of the each individual measurement in the HPLC an then it saves 
them in a directory. Each plot has de corresponding wevelength. In my case, for each 
inyection, de PDA detector register the signal at 215nm and 260nm, so, each plot has those
signal. This allows you to analize each sample and find the peak that you want"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# INPUT
# The two wevelength are stored in different paths and csv files has the same names.
paths = {
    "215nm": r"path/to/data",
    "260nm": r"path/to/data",
}

save_path = r"path/to/data"
sample_list = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7"]

print("=" * 10, "The program has been started", "=" * 10)

# MODIFY THIS PART IN THE FUTURE FOR POSSIBLE ERRORs
keys_list = list(paths.keys())  # paths keys list
dir_list = os.listdir(paths["215nm"])
print(dir_list)

save_path = save_path + "\{}" + ".png"

# Loop of chromatograms
for i in range(0, len(dir_list)):
    # Extract chromatogram name
    chroma_name = dir_list[i]
    chroma_name = chroma_name.split(".")
    chroma_name = chroma_name[0]
    print("Creating figure for " + chroma_name + " chromatogram:")

    # Creating figure,ax
    fig, ax = plt.subplots(figsize=(20, 10))

    # Loop of wavelengths (in this case 215 and 260nm)
    for key in paths:
        read_path = paths[key] + "\{}"  # path as a formatted string
        print("\tOpening", read_path.format(dir_list[i]))
        # Reading .csv file with chromatogram data
        df = pd.read_csv(read_path.format(dir_list[i]), sep=";", decimal=",")
        y = df["Intensity"].to_numpy()
        x = list(range(0, len(y)))
        # Plotting chromatograms.
        print("\tPlotting", chroma_name, "at", key)
        ax.plot(x, y, label=key, linewidth=1.0)

    # Plot figure setup
    ax.set_xlim(0, 3500)
    ax.set_ylabel("Intensity")
    ax.set_title(chroma_name + " chromatogram")
    ax.grid()
    ax.legend()

    plt.savefig(save_path.format(chroma_name), dpi=600)  # Save figure

    plt.cla()  # Clean current axes
    plt.clf()  # Clean current figure
    plt.close()

    print(
        "\t" + chroma_name[0] + ".png",
        "has been saved in",
        save_path.format(chroma_name[0]),
        "\n",
    )

print("=" * 10, "The program has been finished", "=" * 10)
