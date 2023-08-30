"""chroma_plot3.py
This script creates a plot of the each individual measurement in the HPLC an 
then it saves them in a directory. Each plot has de corresponding wevelength. 
In my case, for each inyection, de PDA detector register the signal at 215nm 
and 260nm, so, each plot has those signal. This allows you to analize each 
sample and find the peak that you want"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def read_chromatogram(file_path):
    # This function opens a csv file that contains the chromatogram data and
    # return the data as numpy arrays.
    # Input:
    #   filename: path of the correpsonding csv file
    # Output:
    #   x: array of time (or number of data)
    #   y: intensity of signal

    print("\tOpening", file_path)
    # Reading .csv file with chromatogram data
    df = pd.read_csv(file_path, sep=";", decimal=",")
    # Transform data to numpy array
    y = df["Intensity"].to_numpy()
    x = list(range(0, len(y)))

    return x, y


def formatted_path(dir_path, file_name, extention=""):
    # For a folder that contain multiple files, this function  return the path
    # of the corresponding file in folder
    # Input:
    #   dir_path: string of the corresponding folder path
    #   Extention of the file (.csv,.png, etc.)
    # Output:
    #   file_path: string of the corresponding file path

    dir_path = dir_path + "\{}" + extention
    file_path = dir_path.format(file_name)

    return file_path


def get_chroma_name(full_name):
    # This function get the name of the chromatogram splitting the
    # the filename extention ex. <A0_01>.csv
    aux = full_name.split(".")
    chroma_name = aux[0]
    return chroma_name


def chroma_plot(
    data,
    save_path="None",
    ylabel="Intensity",
    xlabel="Retention time [min]",
    title="Example cromatogram",
):
    # Creating figure,ax
    fig, ax = plt.subplots(figsize=(10, 5))
    # Figure formatting
    ax.set_xlim(0, 4000)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title)

    # Loop of data stored in dictionary
    for key in data:
        # Extract data from dictionary
        x = data[key][0]
        y = data[key][1]
        # Plot data
        ax.plot(x, y, label=key)

    ax.legend()

    # Show or save imae
    if save_path == "None":
        plt.show()
    else:
        print("\tSaving in plot in", save_path)
        plt.savefig(image_path, dpi=100)

    plt.close()


# INPUT
# The two wevelength are stored in different paths and csv files has the same names.
dic_pda = {
    "215nm": r"path/to/data",
    "260nm": r"path/to/data",
}

save_path = r"path/to/data"

# ==============================================================================
print("The program has been started".center(79, "="))

# When you usen multichannels (or wavelenghts) in chromatography, each chanell
# has de same number of data points
channels = list(dic_pda.keys())
dir_list = os.listdir(dic_pda[channels[0]])


flag = "({}/" + str(len(dir_list)) + ")"
i = 0
# Loop of chromatograms
for file_name in dir_list:
    # Counter
    i = i + 1
    # Extract chromatogram name (get_chroma_name)
    chroma_name = get_chroma_name(file_name)
    image_path = formatted_path(save_path, chroma_name, ".png")

    print(flag.format(str(i)), "Processing chromatogram", chroma_name)

    chroma_data = {}  # Preallocation

    # Loop of wavelengths (in this case 215 and 260nm)
    for key in dic_pda:
        # Directory path to be read
        read_path = dic_pda[key]

        # Chromatogram path to be read
        chroma_path = formatted_path(read_path, file_name)

        x, y = read_chromatogram(chroma_path)
        chroma_data[key] = [x, y]

    chroma_plot(
        chroma_data,
        image_path,
        ylabel="Intensity",
        xlabel="Retention time [min]",
        title=chroma_name,
    )
