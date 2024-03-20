from plot_funcs import open_pda
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from utils.peaks import *
from plots.plot_peaks import *


# Methods: function of a class
# Atributtes: constants of a class
class Chromatogram:

    # This is a class attribute
    detector = "JASCO MD-4010"
    all = []

    def __init__(self, name, data, time, wavelength):
        # Run validation to reacive arguments
        assert type(name) is str, f"{name} must be a string!"
        assert type(data) is np.ndarray, f"{data} must be a numpy.array!"
        assert type(time) is np.ndarray, f"{time} must be a numpy.array!"
        assert type(wavelength) is np.ndarray, f"{wavelength} must be a numpy.array!"

        # Assign to self object (instance attributes)
        self.name = name
        self.data = data
        self.time = time  # [t_0,t_f]
        self.wavelength = wavelength  # [wl_0,wl_f]

        # Action to execute
        Chromatogram.all.append(self)

    # Return an unambiguous string representation of the object
    def __repr__(self) -> str:
        return f"Chromatogram('{self.name}')"

    ######################## CLASS METHODS ####################################
    @classmethod  # This is a decorator
    def open_pda(cls, file_path):
        """This class method opnes a single PDA file and create an instance using
        that data."""

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

        # Create the instance (important to return)
        return cls(
            name=name_list[0],
            data=PDA_data,
            time=time,
            wavelength=wavelength,
        )

    def find_peaks(self, wavelength, show=None):
        """This function find de corresponding peaks in single wavelength
        chromatogram (Time vs Intensity)"""
        # Rearrange data
        intensity = self.data
        time_array = np.linspace(self.time[0], self.time[1], intensity.shape[0])
        time_array = time_array.flatten()

        wave_length_array = np.linspace(
            self.wavelength[0], self.wavelength[1], intensity.shape[1]
        )

        # Inputs validation
        if wavelength in wave_length_array:
            print("The given wavelength is in range :)")
        else:  # In future add and error statement
            print("The given wavelength is not in range >:c")
            print("wave_length_array:\n", wave_length_array)

        # Generate chromatogram of single wavelength (Separated function?)
        index = np.where(wavelength == wave_length_array)[0]
        chroma_data = intensity[:, index].flatten()

        print(f"Chromatogram at {wavelength} (nm)\n", chroma_data.shape)
        peaks_data = peak_finder(chroma_data, time_array)

        if show == True:
            plot_results(chroma_data, time_array, peaks_data)

        return peaks_data

    # @classmethod
    # def open_multiple_pda(cls, folder_path):
    #    """This class method open multiple PDA files stored in a folder"""

    # @staticmethod  # Static methods are for utilities
    def extract_spectrum(self, residence_time):
        """This function verified if an object is a chromatogram with PDA"""
        intensity = self.data
        time_array = np.linspace(self.time[0], self.time[1], intensity.shape[0])
        wave_length_array = np.linspace(
            self.wavelength[0], self.wavelength[1], intensity.shape[1]
        )
        print("Shape:", intensity.shape)
        print("time_array:", time_array)
        print("wave_length_array:", wave_length_array)

    # PLOT multiple spectras with compounds names
    # fig, ax = plt.subplots(figsize=(10, 5))  # Creating figure,ax
    # ax.set_ylabel("Intensity")
    # ax.set_xlabel("wavelength [nm]")
    # ax.set_xlim(wavelength[0], wavelength[-1])
    # ax.set_title("Spectrum ")

    # for compound in spectra_df.columns:
    #  compound_spectrum = spectra_df[compound].to_numpy()
    #  ax.plot(wavelength, compound_spectrum, label=compound)

    # plt.legend()
    # plt.show()

    def description(self):
        print(
            f"The data from '{self.name}' was obtained in a {Chromatogram.detector} detector\n"
        )

    def pda_plot(
        self,
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
        time_array = np.linspace(self.time[0], self.time[1], self.data.shape[0])
        wavelength_array = np.linspace(
            self.wavelength[0], self.wavelength[1], self.data.shape[1]
        )

        X, Y = np.meshgrid(time_array, wavelength_array)
        Z = self.data.T

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
            x_min = min(time_array)
        if x_max == None:
            x_max = max(time_array)

        if y_min == None:
            y_min = min(wavelength_array)
        if y_max == None:
            y_max = max(wavelength_array)

        ax.set_xlim([x_min, x_max])
        ax.set_ylim([y_min, y_max])
        cs.set_clim(vmin=z_min, vmax=z_max)

        fig.colorbar(cs)  # color bar
        plt.gca().invert_yaxis()

        # Save the plot if a save path is provided
        if save_path != "None":
            print("\tSaving image in " + save_path)
            plt.savefig(save_path)
        else:
            plt.show()
