"""This script contain function to plot PDA data in different ways"""

import os
import numpy as np
import matplotlib.pyplot as plt

from utils import info
from utils import extract
from utils.extract import clip_pda


# PLOT 2D
def pda_2d(
    cls,
    wl_list,
    save_path=None,
):
    """Create a 2D chromatogram from your 3D PDA data

    This function takes the intensity of information for given wavelegenth to
    create a time vs intensity plot.

    Args:
        cls (chromaotgram instance)  : instance of Chromatogram class
        wavelength (list)       : list of wevelength (nm) to plot
    """

    print(f"Generating 2D chromatograms from {cls.NAME} data")

    # Extract information necesarry to plot
    time = info.time(cls.INFO)
    wavelength = info.wavelenth(cls.INFO)

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(10, 7))

    # Extract data of wavelength in list and plot them
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

    # ax.grid() # optional
    ax.legend()

    # Save the plot if a save path is provided
    if save_path != None:
        file_name = os.path.join(save_path, cls.NAME + "_2d.png")
        print("\tSaving " + file_name)
        plt.savefig(file_name, dpi=800)
    else:
        plt.show()


def pda_spectrum(cls, time_list):
    """Create a plot with the spectrum of a given residence time

    Args:
        cls (object): instance of Chromatogram class
        time_list (list)       : times to plot
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
            intensity = 100 * intensity / np.max(intensity)  # normalize
            ax.plot(wavelength, intensity, label=str(time) + "min")

    # Get and set limits
    ax.set_xlim(xmin=wavelength[0], xmax=wavelength[-1])
    ax.set_ylabel("Normalized Intensity")
    ax.set_xlabel("Wavelength [nm]")

    ax.grid()
    ax.legend()
    plt.show()


# PLOT 3D
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
    """Create a contour plot of your PDA data

    This function creates a contour plot based on your PDA data.

    Args:
        cls (chromaotgram instance)  : instance of Chromatogram class.
        x_min,x_max, ... (float): limit can be set by the user.
        levels (float): levels in the contour.
        save_path (str): folder where figure will be saved.
    """

    print(f"Generating PDA contour from {cls.NAME} data")

    # EXTRACT DATA FROM OBJECT
    x = info.time(cls.INFO)  # time
    y = info.wavelenth(cls.INFO)  # wavelength
    z = cls.PDA_DATA  # intesity

    # CLIP DATA BASED IN LIMITS GIVEN BY USER (optional)
    ## Set the limits of the x, y a z
    if x_min == None:
        x_min = min(x)
    if x_max == None:
        x_max = max(x)

    if y_min == None:
        y_min = min(y)
    if y_max == None:
        y_max = max(y)

    if z_min == None:
        z_min = z.min()
    if z_max == None:
        z_max = z.max()

    ## Clip the data based on max an min
    x_clipped, y_clipped, z_clipped = clip_pda(
        x,
        y,
        z,
        x_lim=(x_min, x_max),
        y_lim=(y_min, y_max),
    )

    # PREPARING DATA
    X, Y = np.meshgrid(x_clipped, y_clipped)

    Z = np.transpose(z_clipped)
    Z = np.clip(Z, z_min, z_max)  # clip Z with z limits

    # CONTOUR PLOT
    fig, ax = plt.subplots(figsize=(10, 4))
    cs = ax.contourf(
        X,
        Y,
        Z,
        levels=np.linspace(z_min, z_max, lvls),
        cmap=plt.cm.rainbow,
    )

    ## Plot adjustments
    ax.set_xlabel("Residence time [min]")
    ax.set_ylabel("Wavelength [nm]")
    ax.set_xlim([x_min, x_max])
    ax.set_ylim(ax.get_ylim()[::-1])
    cs.set_clim(vmin=z_min, vmax=z_max)
    fig.colorbar(cs)  # color bar
    plt.tight_layout()  # tight loyout

    # Save the plot if a save path is provided
    if save_path != None:
        file_name = os.path.join(save_path, cls.NAME + "_PDA.png")
        print("\tSaving " + file_name)
        plt.savefig(file_name, dpi=800)
    else:
        plt.show()


def pda_surface(
    cls,
    x_min=None,
    x_max=None,
    y_min=None,
    y_max=None,
    z_min=None,
    z_max=None,
    save_path=None,
):
    """Create a surface plot of your PDA data

    This function creates a surface plot based on your PDA data.

    Args:
        cls (chromaotgram instance)  : instance of Chromatogram class.
        x_min,x_max, ... (float): limit can be set by the user.
        save_path (str): folder where figure will be saved.
    """

    print(f"Generating surface plot from {cls.NAME}")

    # EXTRACT DATA FROM OBJECT
    x = info.time(cls.INFO)  # time
    y = info.wavelenth(cls.INFO)  # wavelength
    z = cls.PDA_DATA  # intensity

    """ print("Original X size (time): ", np.shape(x))
    print("Original Y size (wavelength): ", np.shape(y))
    print("Original Z size (intensity): ", np.shape(z)) """

    # CLIP DATA BASED IN LIMITS GIVEN BY USER (optional)
    ## Set the limits of the x, y a z
    if x_min == None:
        x_min = min(x)
    if x_max == None:
        x_max = max(x)

    if y_min == None:
        y_min = min(y)
    if y_max == None:
        y_max = max(y)

    if z_min is None:
        z_min = z.min()
    if z_max is None:
        z_max = z.max()

    ## Clip the data based on max an min
    x_clipped, y_clipped, z_clipped = clip_pda(
        x,
        y,
        z,
        x_lim=(x_min, x_max),
        y_lim=(y_min, y_max),
    )

    """ print("Clipped X size (time): ", np.shape(x_clipped))
    print("Clipped Y size (wavelength): ", np.shape(y_clipped))
    print("Clipped Z size (intensity): ", np.shape(z_clipped)) """

    # PREPARING DATA
    X, Y = np.meshgrid(x_clipped, y_clipped)

    Z = np.transpose(z_clipped)
    Z = np.clip(Z, z_min, z_max)  # Clip Z with z limits

    # SURFACE PLOT
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(
        X,
        Y,
        Z,
        cmap=plt.cm.rainbow,
    )

    ## Plot adjustments
    ax.set_xlabel("Residence time [min]")
    ax.set_ylabel("Wavelength [nm]")
    ax.set_xlim([x_min, x_max])
    ax.set_ylim(ax.get_ylim()[::-1])
    surf.set_clim(vmin=z_min, vmax=z_max)
    ax.set_box_aspect([2, 1, 1])  # Adjust aspect [X, Y, Z] aspect ratio
    plt.tight_layout()  # Tighten the layout

    # Save the plot if a save path is provided
    if save_path != None:
        file_name = os.path.join(save_path, cls.NAME + "_surf.png")
        print("\tSaving " + file_name)
        plt.savefig(file_name, dpi=800)
    else:
        plt.show()
