"""merge_channels.py
in HPLC-DAD you could get signals from different channels (or wavelengths). My
HPLC software returns me the data of each channel in independent .csv file. This
program merge multichannel data ina single .csv file. Also, the program can plot
each channel in the same chromatogram."""


import os
import sys
import matplotlib.pyplot as plt
import pandas as pd


def merge_data(origin_path, channels, chroma_name, save_path="None"):
    """This function take the data of multiple channels of one chromatogram
    and merge them in one dataframe. Then the dataFrame is saved in with the same
    chromatogram name but in a different folder.

    Inputs:
       data_paths: dictionary that allocate the directories paths were
       chromatogram data is stored
       file_name: name of chromatogram csv file (ex. "chromatograme.csv))

     Output:
       chroma_data: data frame that contains multiple channels data"""

    # Preallocation
    chroma_data = pd.DataFrame(columns=channels)

    # channels loop
    for channel in channels:
        print("\tReading", channel, "data")
        read_path = os.path.join(origin_path, channel, chroma_name + ".csv")

        # Read .csv file (time variable is omitted)
        chroma_data[channel] = pd.read_csv(
            read_path, sep=";", decimal=",", usecols=["Intensity"]
        )

    if save_path != "None":
        print("\tSaving chromatogram dataframe in:")
        print("\t\t" + os.path.join(save_path, chroma_name + ".csv"))
        chroma_data.to_csv(
            os.path.join(save_path, chroma_name + ".csv"),
            sep=";",
            header=True,
            index=False,
        )

    return chroma_data


def main(main_path):
    print("The program has been started".center(79, "="))
    print(sys.argv)
    ## Standard folder names. Can't be changed
    origin_folder = "original_data"
    out_data_folder = "merged_data"
    out_image_folder = "chromatogram_plot"

    origin_path = os.path.join(main_path, origin_folder)

    out_data_path = os.path.join(main_path, out_data_folder)

    out_image_path = os.path.join(main_path, out_image_folder)

    os.mkdir(out_data_path)  # Create output data directory
    # os.mkdir(out_image_path)  # Create output images directory

    print(os.path.join(main_path, origin_folder))

    # When you usen multichannels (or wavelenghts) in chromatography, each chanell
    # has de same number of data points
    channels = os.listdir(origin_path)
    print(channels)

    # List of chromatogram names
    chroma_list = os.listdir(os.path.join(origin_path, channels[0]))
    print(chroma_list)

    # Counter
    counter = "({}/" + str(len(chroma_list)) + ")"
    i = 0

    # Loop of chromatograms
    for chroma_name in chroma_list:
        # Counter
        i = i + 1

        # Get chromatogram name without extention
        chroma_name = chroma_name.split(".")
        chroma_name = chroma_name[0]
        print(counter.format(str(i)), "Merging data from chromatogram", chroma_name)

        # Merge multichannel data
        chroma_data = merge_data(
            origin_path, channels, chroma_name, save_path=out_data_path
        )

        # if image == "True":
        #    image_path = os.path.join(out_image_path, chroma_name + ".png")
        #    channel_plot(chroma_data, show_time="True", save_path=image_path)


if __name__ == "__main__":
    main(sys.argv[1])
