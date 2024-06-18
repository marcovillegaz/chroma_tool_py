"""This script contain function to plot PDA data in different ways"""

import numpy as np
import matplotlib.pyplot as plt

from utils import info
from utils import extract


def pda_contour(
    cls,
    x_min=None,
    x_max=None,
    y_min=None,
    y_max=None,
    z_min=None,
    z_max=None,
    lvls=1000,
    save_path=None,
):
    print("Plotting PDA contour...")

    # Extract information necesarry to plot
    intensity = cls.PDA_DATA
    time = info.time(cls.INFO)
    wavelength = info.wavelenth(cls.INFO)

    # Rearrengning data
    X, Y = np.meshgrid(time, wavelength)
    Z = np.transpose(intensity)

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
        y_max = max(wavelength)

    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])
    cs.set_clim(vmin=z_min, vmax=z_max)

    fig.colorbar(cs)  # color bar
    plt.gca().invert_yaxis()
    # plt.subplots_adjust(left=0.2, right=0.8, bottom=0.0, top=1.1) # MODIFY

    # Save the plot if a save path is provided
    if save_path != None:
        print("\tSaving image in " + save_path)
        plt.savefig(save_path)
    else:
        plt.show()


def pda_2d(cls, wl_list):
    """This function plot the data Intensity vs Time of a chromatogram
    wavelength is a list of wavelength

    Plot chromatograme based on PDA information

    Args:
        PDA_data (numpy.array)  : matrix with the PDA surface
        wavelength (list)       : wevelength (nm) to plot

    Returns:
    """
    print("Plotting 2d chromatogram")

    # Extract information necesarry to plot
    time = info.time(cls.INFO)
    wavelength = info.wavelenth(cls.INFO)

    fig, ax = plt.subplots(figsize=(10, 7))

    # Extract data of multiple wavelengths
    for wl in wl_list:
        if wl <= wavelength[0] or wl >= wavelength[-1]:
            print(f"¡{wl}nm is not in range!")
        else:
            intensity = extract.by_wavelength(cls, wl)
            ax.plot(time, intensity, label=str(wl) + "nm")

    # Get and set limits
    ax.set_xlim(xmin=time[0], xmax=time[-1])
    ax.set_ylabel("Intensity")
    ax.set_xlabel("Time [min]")

    ax.grid()
    ax.legend()
    plt.show()


def pda_spectrum(cls, time_list):
    """This function plot Intensity vs Wavelength at a given times. This
    information correspon to the spectrum

    Args:
        cls (object): instance of Chromatogram class
        time_list (list)       : times to plot

    Returns:
    """
    print("Plotting spectrum")

    # Extract information necesarry to plot
    time_array = info.time(cls.INFO)
    wavelength = info.wavelenth(cls.INFO)

    fig, ax = plt.subplots(figsize=(10, 7))

    # Extract data of multiple wavelengths
    for time in time_list:
        if time <= time_array[0] or time >= time_array[-1]:
            print(f"¡{time}min is not in range!")
        else:
            intensity = extract.by_time(cls, time)
            ax.plot(wavelength, intensity, label=str(time) + "min")

    # Get and set limits
    ax.set_xlim(xmin=wavelength[0], xmax=wavelength[-1])
    ax.set_ylabel("Intensity")
    ax.set_xlabel("Wavelength [nm]")

    ax.grid()
    ax.legend()
    plt.show()
