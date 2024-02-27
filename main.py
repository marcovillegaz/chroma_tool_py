from plot_funcs import open_pda
import matplotlib.pyplot as plt
import numpy as np

path = r"path/to/data"


# Methods: function of a class
# Atributtes: constants of a class
class chromatogram:

    # This is a class attribute
    detector = "JASCO MD-4010"
    all = []

    def __init__(self, path, name=None):
        # Run validation to reacive arguments
        assert type(path) is str, f"{path} must be a string!"

        # Extract PDA information from text file
        data, time, wavelength = open_pda(path)

        # Assign to self object (instance attributes)
        self.data = data
        self.time = time  # [t_0,t_f]
        self.wavelength = wavelength  # [wl_0,wl_f]

        if name == None:
            path_list = path.split("\\")
            name_list = path_list[-1].split(".")
            self.name = name_list[0]

        # Action to execute
        chromatogram.all.append(self)

    def __repr__(self) -> str:
        return f"chroma('{self.name}')"

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


# assign and instance to the corresponding information
chroma1 = chromatogram(
    r"path/to/data"
)
chroma2 = chromatogram(
    r"path/to/data"
)

for instance in chromatogram.all:
    print(instance)
    print(instance.name)

# Show chromatogram description
chroma1.description()  # class attribute

# Plot chromatogram data as surface
# chroma1.pda_plot()
# chroma2.pda_plot()
