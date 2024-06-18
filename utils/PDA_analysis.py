import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from basics_func import Extract_SingleWavelength, peak_finder, plot_peaks


def open_PDA(file_path):
    print("Openning PDA file...")

    # Open the file and read its contents
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

    # Save useful information of the PDA
    useful_dic = {}
    useful_dic["START_TIME"] = float(data_dict["START_TIME"].replace("min", ""))
    useful_dic["END_TIME"] = float(data_dict["END_TIME"].replace("min", ""))
    useful_dic["START_WL"] = float(data_dict["START_WL"].replace("nm", ""))
    useful_dic["END_WL"] = float(data_dict["END_WL"].replace("nm", ""))
    print("\t", useful_dic)

    PDA_shape = PDA_data.shape
    print("\tPDA shape: ", PDA_shape)
    time = np.linspace(useful_dic["START_TIME"], useful_dic["END_TIME"], PDA_shape[0])
    print("\ttime shape: ", time.shape)
    wavelength = np.linspace(useful_dic["START_WL"], useful_dic["END_WL"], PDA_shape[1])
    print("\twavelength shape: ", wavelength.shape)

    return PDA_data, wavelength, time


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
    print("plot_pda...")

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
    
    # Save the plot if a save path is provided
    if save_path != "None":
        plt.savefig(save_path)
    else:
        plt.show()


def plot_by_wavelength(PDA_data, time, wl_list):
    fig, ax = plt.subplots(figsize=(10, 5))  # Creating figure,ax
    ax.set_xlim(left=0)
    ax.set_ylabel("Intensity")
    ax.set_xlabel("Retention time [min]")

    for wl in wl_list:
        index = np.where(wavelength == wl)[0]
        chroma_data = PDA_data[:, index]
        ax.plot(time, chroma_data, label=str(wl) + "nm")

    plt.xticks(np.arange(time[0], time[-1], step=1))
    plt.legend()
    plt.grid()
    plt.show()


def mix_plot(PDA_data, time, wl_list):
    fig, (ax1, ax2) = plt.subplots(
        2, sharex=True, figsize=(10, 8), gridspec_kw={"height_ratios": [2, 1]}
    )

    ax1.set_ylabel("Intensity")
    ax1.set_xlabel("Retention time [min]")

    for wl in wl_list:
        index = np.where(wavelength == wl)[0]
        chroma_data = PDA_data[:, index]
        ax1.plot(time, chroma_data, label=str(wl) + "nm")

    ax1.legend()

    # PDA PLOT
    X, Y = np.meshgrid(time, wavelength)
    Z = PDA_data.T
    levels = np.linspace(Z.min(), Z.max(), 1000)

    ax2.set_xlabel("Retention time [min]")
    ax2.set_ylabel("Wavelength [nm]")
    cs = ax2.contourf(
        X,
        Y,
        Z,
        levels=levels,
        cmap=plt.cm.rainbow,
    )  # contour plot
    ax2.invert_yaxis()

    # SHOW PLOT
    plt.show()


################################################################################
# Define the file path
file_path = r"path/to/data"

PDA_data, wavelength, time = open_PDA(file_path)


# PLOT: wavelenthg vs time
# plot_by_wavelength(PDA_data, time, wl_list=[216, 260])

# PLOT: PDA surface
plot_pda(
    PDA_data,
    time,
    wavelength,
    x_min=0,  # min retention time
    # x_max=5,    # max retention time
    y_min=200,  # min wavelength
    y_max=400,  # max wavelength
    z_min=-5000,  # min intesity
    z_max=50000,  # max intesity
    lvls=30,  # levels of the counter plot
)


# MIX PLOT: (wavelenthg vs time + PDA surface)
# mix_plot(PDA_data, time, wl_list=[260])

""" chroma_df = Extract_SingleWavelength(
    PDA_data, wavelength, time, wl_list=[260, 280, 300]
)

peaks_df = peak_finder(chroma_df)
# plot_peaks(chroma_df, time, peaks_df)
comp_name = ["comp1", "comp2", "comp3"]
spectra_df = pd.DataFrame()
peak_list = peaks_df["260nm"]
for i, peak_index in enumerate(peak_list):
    print(i)
    spectra_df[comp_name[i]] = PDA_data[int(peak_index), :]

print(spectra_df)

# PLOT multiple spectras with compounds names
fig, ax = plt.subplots(figsize=(10, 5))  # Creating figure,ax
ax.set_ylabel("Intensity")
ax.set_xlabel("wavelength [nm]")
ax.set_xlim(wavelength[0], wavelength[-1])
ax.set_title("Spectrum ")

for compound in spectra_df.columns:
    compound_spectrum = spectra_df[compound].to_numpy()
    ax.plot(wavelength, compound_spectrum, label=compound)

plt.legend()
plt.show()
 """

# create a function to extract spectrum
# Input (peak index o time)
# Extract row from PDA

# def spectrum():
# def plot_spectra():
