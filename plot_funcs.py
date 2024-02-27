import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from basics_func import Extract_SingleWavelength, peak_finder, plot_peaks


def open_pda(file_path):
    """This function open the text file that contains the PDA information
    and return the data"""

    print("Openning PDA file...")

    # Open the .txt file
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Extract PDA information in .txt file (depend of HPLC software)
    PDA_data = []
    PDA_info = []
    for i, line in enumerate(lines):
        if i < 11:
            PDA_info.append(line)
        elif i > 11:
            row = list(map(int, line.split()))
            PDA_data.append(row)

    PDA_data = np.array(PDA_data)

    # Extract PDA info and save in dictionary
    data_dict = {}
    for item in PDA_info:
        item = item.replace("\n", "")
        item = item.replace(",", ".")
        key, value = item.split("\t")
        data_dict[key] = value

    # Start and end time
    time = np.array(
        [
            float(data_dict["START_TIME"].replace("min", "")),
            float(data_dict["END_TIME"].replace("min", "")),
        ]
    )
    # Start and end wavelength
    wavelength = np.array(
        [
            float(data_dict["START_WL"].replace("nm", "")),
            float(data_dict["END_WL"].replace("nm", "")),
        ]
    )

    return PDA_data, time, wavelength


def plot_pda(
    PDA_data,
    time,
    wavelength,
    x_min=None,
    x_max=None,
    y_min=None,
    y_max=None,
    z_min=None,
    z_max=None,
    lvls=None,
    save_path="None",
):
    print("Plotting PDA contour...")

    # Rearrengning data
    X, Y = np.meshgrid(time, wavelength)
    Z = PDA_data.T

    if lvls == None:
        lvls = 1000
    if z_min == None:
        z_min = Z.min()
    if z_max == None:
        z_max = Z.max()

    Z = np.clip(Z, z_min, z_max)

    # Create contour plot
    fig, ax = plt.subplots(figsize=(12, 4))
    cs = ax.contourf(
        X,
        Y,
        Z,
        levels=np.linspace(z_min, z_max, lvls),
        cmap=plt.cm.rainbow,
    )

    ax.set_xlabel("Residence time [min]")
    ax.set_ylabel("Wavelength [nm]")

    # Set the limits of the x and y axes
    if x_min == None:
        x_min = min(time)
    if x_max == None:
        x_max = max(time)

    if y_min == None:
        y_min = min(wavelength)
    if y_max == None:
        y_max = max(wavelength)

    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])
    cs.set_clim(vmin=z_min, vmax=z_max)

    fig.colorbar(cs)  # color bar
    plt.gca().invert_yaxis()
    # plt.subplots_adjust(left=0.2, right=0.8, bottom=0.0, top=1.1) # MODIFY

    # Save the plot if a save path is provided
    if save_path != "None":
        print("\tSaving image in " + save_path)
        plt.savefig(save_path)
    else:
        plt.show()
