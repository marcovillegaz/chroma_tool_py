"""chroma_plot2.py
This script create a plot of the each sample an then it saves them in a directory.
Each duplicate are plotted in the corresponding sample figure. This allows you to analize
the peaks of each replicate one by one"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# INPUT
dir_path = r"path/to/data"
save_path = r"path/to/data"
sample_list = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7"]

print("=" * 10, "The program has been started", "=" * 10)

dir_list = os.listdir(dir_path)  # name of files in directory

file_path = dir_path + "\{}"
save_path = save_path + "\{}" + ".png"

# Loop of samples
for flag in sample_list:
    print("Creating figure for " + flag + " sample ...")

    # Creating figure,ax
    fig, ax = plt.subplots(figsize=(20, 10))

    # Loop of csv files
    for i in range(0, len(dir_list)):
        sample_name = dir_list[i]
        sample_name = sample_name.split("_")

        # Only the names that match are plotted
        if sample_name[0] == flag:
            # Reading .csv file with chromatogram data
            df = pd.read_csv(file_path.format(dir_list[i]), sep=";", decimal=",")
            y = df["Intensity"].to_numpy()
            x = list(range(0, len(y)))
            # Plotting chromatograms.
            ax.plot(x, y, label=dir_list[i], linewidth=1.0)

    # Plot figure setup
    ax.set_xlim(0, 3500)
    ax.set_ylabel("Intensity")
    ax.set_title(flag + " sample chromatogram")
    ax.grid()
    ax.legend()

    plt.savefig(save_path.format(flag), dpi=600)  # Save figure
    print(flag + ".png", "has been saved in", save_path.format(flag), "\n")

    plt.cla()  # Clean current axes
    plt.clf()  # Clean current figure

print("=" * 10, "The program has been finished", "=" * 10)
