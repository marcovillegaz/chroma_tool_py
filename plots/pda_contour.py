import numpy as np
import matplotlib.pyplot as plt


def pda_contour(
    PDA_data,
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

    intensity = PDA_data["Intensity"]
    time_array = np.linspace(
        PDA_data["Time"][0],
        PDA_data["Time"][1],
        intensity.shape[0],
    )
    wavelength_array = np.linspace(
        PDA_data["Wavelength"][0],
        PDA_data["Wavelength"][1],
        intensity.shape[1],
    )

    # Rearrengning data
    X, Y = np.meshgrid(time_array, wavelength_array)
    Z = np.transpose(intensity)

    print(X.shape)
    print(Y.shape)
    print(Z.shape)

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
    # plt.subplots_adjust(left=0.2, right=0.8, bottom=0.0, top=1.1) # MODIFY

    # Save the plot if a save path is provided
    if save_path != "None":
        print("\tSaving image in " + save_path)
        plt.savefig(save_path)
    else:
        plt.show()
