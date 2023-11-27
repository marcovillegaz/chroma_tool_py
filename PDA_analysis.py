import numpy as np
import matplotlib.pyplot as plt


def open_PDA(file_path):
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

    # Print the resulting dictionary
    # print(data_dict)

    # Save useful information of the PDA
    useful_dic = {}
    useful_dic["START_TIME"] = float(data_dict["START_TIME"].replace("min", ""))
    useful_dic["END_TIME"] = float(data_dict["END_TIME"].replace("min", ""))
    useful_dic["START_WL"] = float(data_dict["START_WL"].replace("nm", ""))
    useful_dic["END_WL"] = float(data_dict["END_WL"].replace("nm", ""))
    print(useful_dic)

    PDA_shape = PDA_data.shape
    time = np.linspace(useful_dic["START_TIME"], useful_dic["END_TIME"], PDA_shape[0])
    wavelength = np.linspace(useful_dic["START_WL"], useful_dic["END_WL"], PDA_shape[1])

    return PDA_data, time, wavelength


def plot_pda(PDA_data, time, wavelength, save_path="None"):
    X, Y = np.meshgrid(time, wavelength)
    Z = PDA_data.T
    levels = np.linspace(Z.min(), Z.max(), 1000)

    fig, ax = plt.subplots(figsize=(12, 4))

    ax.set_xlabel("Residence time [min]")
    ax.set_ylabel("Wavelength [nm]")
    cs = ax.contourf(
        X,
        Y,
        Z,
        levels=levels,
        cmap=plt.cm.rainbow,
    )  # contour plot
    fig.colorbar(cs)  # color bar
    plt.gca().invert_yaxis()
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
PDA_data, time, wavelength = open_PDA(file_path)


# plot by wavelength
# plot_by_wavelength(PDA_data, time, wl_list=[200, 260, 350])

# PLOT PDA
# plot_pda(PDA_data, time, wavelength)

mix_plot(PDA_data, time, wl_list=[200, 246, 270])
