"""merge_channels.py
in HPLC-DAD you could get signals from different channels (or wavelengths). My
HPLC software returns me the data of each channel in independent .csv file. This
program merge multichannel data ina single .csv file. Also, the program can plot
each channel in the same chromatogram."""


import os
import matplotlib.pyplot as plt
import pandas as pd


def chroma_plot(chroma_df, save_path="None", xlim="None", ylim="None", title="None"):
    # Creating figure,ax
    ax = chroma_df.plot(figsize=(17, 7))

    # Set limits
    if ylim != "None":
        ax.set_ylim(ylim[0], ylim[1])
    if xlim != "None":
        ax.set_xlim(xlim[0], xlim[1])
    # Set title
    if title != "None":
        ax.set_title(title)

    ax.set_ylabel("Intensity")  # Set labels
    plt.grid()  # Turn grid on

    # Show or save image
    if save_path == "None":
        plt.show()
    else:
        print("\tSaving in plot in:")
        print("\t\t" + save_path)
        plt.savefig(save_path, dpi=300)

    plt.close()


def merge_data(data_paths, file_name, save_path="None"):
    # Inputs:
    #   data_paths: dictionary that allocate the directories paths were
    #   chromatogram data is stored
    #   file_name: name of chromatogram csv file (ex. "chromatograme.csv)"
    # Output:
    #   chroma_data: data frame that contains multiple channels data

    # Preallocation
    chroma_data = pd.DataFrame()
    # Dictionary loop
    for key in data_paths:
        print("\tReading", key, "data")
        # Get directory path to be read
        read_path = data_paths[key]
        read_path = read_path + "\{}"
        # Chromatogram path to be read
        chroma_path = read_path.format(file_name)
        # Read .csv file (time variable is omitted)
        chroma_data[key] = pd.read_csv(
            chroma_path, sep=";", decimal=",", usecols=["Intensity"]
        )

    if save_path != "None":
        print("\tSaving chromatogram dataframe in:")
        save_path = save_path + "\{}"
        print("\t\t" + save_path.format(file_name))
        chroma_data.to_csv(
            save_path.format(file_name),
            sep=";",
            header=True,
            index=False,
        )
    return chroma_data


def main(data_paths, output_data_path, output_image_path="None"):
    # Input:
    #    data_paths: dictionary that allocate the directories paths were
    #    output_data_path: directory to store arranged data
    #    output_image_path: directory to store chromatograms images (optional)

    print("The program has been started".center(79, "="))
    # When you usen multichannels (or wavelenghts) in chromatography, each chanell
    # has de same number of data points
    channels = list(dic_pda.keys())
    dir_list = os.listdir(dic_pda[channels[0]])

    counter = "({}/" + str(len(dir_list)) + ")"
    i = 0
    # Loop of chromatograms
    for file_name in dir_list:
        # Counter
        i = i + 1
        # Get chromatogram name without extention
        chroma_name = file_name.split(".")
        chroma_name = chroma_name[0]
        print(counter.format(str(i)), "Processing chromatogram", chroma_name)

        # Merge multichannel data
        chroma_data = merge_data(dic_pda, file_name, save_path=output_data_path)

        # Plot multichannel chromatograms (Optional)
        if output_image_path != "None":
            image_path = output_image_path + chroma_name + ".png"
            chroma_plot(chroma_data, save_path=image_path, title=file_name)


# INPUTS
dic_pda = {
    "215nm": r"path/to/data",
    "260nm": r"path/to/data",
}

output_data_path = r"path/to/data"
output_image_path = r"path/to/data"

# MAIN CODE
main(
    dic_pda,
    output_data_path,
)
