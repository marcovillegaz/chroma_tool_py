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


def chroma_plot(x, y, image_path):
    fig, ax = plt.subplots(figsize=(10, 5))  # Creating figure,ax
    ax.set_xlim(0, 3500)
    ax.set_ylabel("Intensity")
    ax.set_xlabel("Retention time [min]")
    ax.set_title("Example cromatogram")
    ax.plot(x, y, label=file_name)
    ax.legend()

    print("saving in plot in", image_path)
    # plt.show()
    plt.savefig(image_path, dpi=600)
    plt.close()


dir_path = r"path/to/data"
save_path = r"path/to/data"

dir_list = os.listdir(dir_path)  # get name of files in directory

for file_name in dir_list:
    chroma_name = get_chroma_name(file_name)
    print(chroma_name)

    chroma_path = formatted_path(dir_path, file_name)
    image_path = formatted_path(save_path, chroma_name, ".png")
    print(image_path)

    x, y = read_chromatogram(chroma_path)

    chroma_plot(x, y, image_path)
    # Plotting chromatograms.
