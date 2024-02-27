import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


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
    image_path="None",
    ylabel="Intensity",
    xlabel="Retention time [min]",
    title="Example cromatogram",
):
    # Creating figure,ax
    fig, ax = plt.subplots(figsize=(10, 5))
    # Figure formatting
    ax.set_xlim(0, 100)
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
    if image_path == "None":
        plt.show()
    else:
        print("Saving in plot in", image_path)
        plt.savefig(image_path, dpi=600)

    plt.close()


dir_path = r"path/to/data"
save_path = r"path/to/data"

# Plot between -10 and 10 with .001 steps.
x1 = np.arange(0, 100, 0.01)

y1 = norm.pdf(x1, 30, 1)
y2 = norm.pdf(x1, 40, 4)
y3 = norm.pdf(x1, 45, 0.8)
y4 = norm.pdf(x1, 75, 1.3)


data = {
    # "prueba1": np.array([x1, y1]),
    # "prueba2": np.array([x1, y2]),
    # "prueba3": np.array([x1, y3]),
    # "prueba4": np.array([x1, y4]),
    "prueba5": np.array([x1, y1 + y2 + y3]),
}
print(data)


chroma_plot(data, image_path="None")


dir_list = os.listdir(dir_path)  # get name of files in directory

# for file_name in dir_list:
# chroma_name = get_chroma_name(file_name)
# print(chroma_name)

# chroma_path = formatted_path(dir_path, file_name)
# image_path = formatted_path(save_path, chroma_name, ".png")
# print(image_path)

# x, y = read_chromatogram(chroma_path)

# chroma_plot(x, y, image_path)
# Plotting chromatograms.
