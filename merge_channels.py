"""merge_channels.py
in HPLC-DAD you could get signals from different channels (or wavelengths). My
HPLC software returns me the data of each channel in independent .csv file. This
program merge multichannel data ina single .csv file. Also, the program can plot
each channel in the same chromatogram."""


import os
import matplotlib.pyplot as plt
import pandas as pd
import argparse


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

    # ADD A FUNCTION THAT RECOGNIZE IF THE FOLDERS ARE CREATED OR NOT

    ## create folder structure. Can't be changed
    origin_path = os.path.join(main_path, "original_data")
    out_data_path = os.path.join(main_path, "merged_data")
    # out_image_path = os.path.join(main_path, "images")

    os.mkdir(out_data_path)  # Create output data directory
    # os.mkdir(out_image_path)  # Create output images directory

    print(origin_path)

    # When you use photodiode array in chromatography, each chanell
    # has de same number of data points
    channels = os.listdir(origin_path)  # Get the channels names
    print(channels)

    # List of chromatogram names in first channel
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
    # Defining description adn epilogue of the program
    parser = argparse.ArgumentParser(
        description="Merged mutiple channel chromatogram into the same csv file for a group of chromatograms.",
        epilog=r"""The MAINPATH must contain a folder named \original_data which has subfolder identified with the wavelength of the 
        corresponding channel. For example: \original_data\260nm and  \original_data\215nm. Each channel folder has the same number 
        of chromatograms files with the same names, but the signal is different. Then, the signals of the channel are merged into a 
        single csv file stored in the folder \merged_data which is going to be used in further data processing.""",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Defining argument to use the program in Console Line Interface
    parser.add_argument(
        "-mp",
        "--mainpath",
        type=str,
        required=True,
        help="the path where the program shall run",
    )

    args = parser.parse_args()

    # main() function
    main(main_path=args.mainpath)
