"""This script has different function to plot chromatograms"""


import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def channel_plot(chroma_data, save_path="None", show_time="False"):
    """This function plot multipñe chananels data in a single plot. This is
    useful because some analites have peaks in different wavelength (channels)
    and can help you to identify them

    Input:
        chroma_data: dataFrame with channels data
        save_path: path where the image is goin to be saved
        show_time: boolean, if you want to plot residence time insted of integers
    """

    # Creating figure,ax
    fig, ax = plt.subplots()

    dt = 0.00333333  # time step
    if show_time == "True":
        chroma_data["time"] = np.arange(0, len(chroma_data)) * dt
        ax = chroma_data.plot(x="time", figsize=(17, 7))
        ax.set_xlabel("Time [min]")

    elif show_time == "False":
        chroma_data.plot(figsize=(17, 7))

    ax.set_ylabel("Intensity")  # Set labels
    ax.set_xlim(left=0)
    plt.grid()  # Turn grid on

    # Show or save image
    if save_path == "None":
        plt.show()
    else:
        print("\tSaving in plot in:")
        print("\t\t" + save_path)
        plt.savefig(save_path, dpi=300)

    plt.close("all")


image = ["merged channels", "by replicates", "BEAS corretction", "Peaks areas", "all"]
