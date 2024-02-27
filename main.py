from plot_funcs import open_pda
import matplotlib.pyplot as plt
import numpy as np

path = r"path/to/data"


# Methods: function of a class
# Atributtes: constants of a class
class chromatogram:

    # This is a class attribute
    detector = "JASCO MD-4010"

    def __init__(self, data, time, wavelength):
        # Run validation to reacive arguments
        assert type(data) is np.ndarray, f"{data} must be a numpy array!"
        assert type(time) is np.ndarray, f"{time} must be a numpy array!"
        assert type(wavelength) is np.ndarray, f"{wavelength} must be a numpy array!"

        # This are instance attributes
        self.data = data
        self.time = time  # [t_0,t_f]
        self.wavelength = wavelength  # [wl_0,wl_f]

    def description(self):
        print(
            f"The chromatogram data was obtained in a {chromatogram.detector} detector\n"
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
            self.wavelength[0], self.wavelength[1], data.shape[1]
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
            print("\tSaving image in " + save_path)
            plt.savefig(save_path)
        else:
            plt.show()


# Extraction chromatogram information from text file
data, time, wavelength = open_pda(path)
# assign and instance to the corresponding information
chroma1 = chromatogram(data, time, wavelength)

# Difference between class and instance attributes
print(chroma1.__dict__)
print(chromatogram.__dict__)

# Show chromatogram description
chroma1.description()  # class attribute

chroma1.detector = "FP-4025"  # assign instance attribute
chroma1.description()


# Plot chromatogram data is surface
chroma1.pda_plot()
