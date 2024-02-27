"""This script has different function to plot chromatograms"""


import os, shutil
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse


def channel_plot(chroma_data, save_path="None", show_time="False"):
    """This function plot multipp chananels data in a single plot. This is
    useful because some analites have peaks in different wavelength (channels)
    and can help you to identify them

    Input:
        chroma_data: dataFrame with channels data
        save_path: path where the image is goin to be saved
        show_time: boolean, if you want to plot residence time insted of integers
    """

    # Creating figure,ax
    fig, ax = plt.subplots()

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


def group_by_replicates(
    path,
):
    """This function return a dictionary with the chromatograms of the replicates
    grouped by sample simplified plotting."""

    chroma_list = os.listdir(path)  # Get filenames in PATH

    sample_names = ["None"] * len(chroma_list)  # Preallocation
    file_names = ["None"] * len(chroma_list)  # Preallocation

    # Create a dataframe with columns = ["sample","filename"]
    for i, chroma_name in enumerate(chroma_list):
        words = chroma_name.split()
        file_names[i] = chroma_name
        sample_names[i] = words[0]

    # Group by  replicates
    files_df = pd.DataFrame({"sample": sample_names, "filename": file_names})
    sample_names = files_df["sample"].drop_duplicates()

    grouped_files = files_df.groupby("sample")  # groupby() returns a dictionary

    return grouped_files


def plot_by_replicates(grouped_files, path, channel, save_path):
    """This function plot replicate of each sample in one figure and then save it"""

    for sample, content in grouped_files:
        print("\nPlotting sample:", sample)  # name is the name of the group (str)
        # print(content)  # content is a dataframe

        # Create axes
        _, ax = plt.subplots(figsize=(14, 7))

        # Loop of replicates
        for i, filename in enumerate(content["filename"]):
            # generate path to read
            chroma_path = os.path.join(path, filename)
            # read csv file
            chroma_data = pd.read_csv(
                chroma_path, sep=";", decimal=".", usecols=[channel]
            )
            # plot chromaotgram signal
            ax.plot(chroma_data.to_numpy(), label="repl" + str(i))

        # Plot configuration
        ax.set_title(sample + " replicates")
        ax.grid()
        ax.set_xlim(left=0)
        ax.set_ylabel("Intensity")
        ax.legend()

        # Save figure
        print("\tSaving ", sample + ".png")
        image_path = os.path.join(save_path, sample + ".png")
        plt.savefig(image_path, dpi=100)

        # plt.show()
        plt.close()


def main(main_path, channel):
    data_path = os.path.join(main_path, "merged_data")
    folder_list = os.listdir(main_path)

    # Condition for existing output folder
    if "plot_by_replicates" in folder_list:
        print("There is an existing \plot_by_replicates folder")
        answer = input("Do you want to overwrite? Type 'yes' or 'no'\n")

        if answer == "yes":  # Overwrite folder
            save_path = os.path.join(main_path, "plot_by_replicates")
            shutil.rmtree(save_path)  # remove existing folder
            os.mkdir(save_path)  # create empty folder

        elif answer == "no":  # Save images in other folder
            new_name = input("Write a new folder name to store images:\n")
            save_path = os.path.join(main_path, new_name)
            os.mkdir(save_path)

        else:
            print("No valid response. Program stopped")
            exit()
    else:
        save_path = os.path.join(main_path, "plot_by_replicates")
        os.mkdir(save_path)  # create empty folder

    grouped_files = group_by_replicates(data_path)
    plot_by_replicates(grouped_files, data_path, channel, save_path)


if __name__ == "__main__":
    # Defining description and epilogue of the program
    parser = argparse.ArgumentParser(
        description="Merged mutiple channel chromatogram into the same csv file for a group of chromatograms.",
        epilog=r"""The """,  # Continue here
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
    parser.add_argument(
        "-ch",
        "--channel",
        type=str,
        required=True,
        help="channel to analize",
    )

    # ADD A NEW ARGUMENT THAT LET SELECT BETWEEN DIFFRENT PLOTTING MODES
    #   BY REPLICATES ONE CHANNEL
    #   BY CHROMATOGRAM ALL CHANNELS
    #   BY CHROMATOGRAM ONE CHANNEL WITH PEAKS

    args = parser.parse_args()

    main(main_path=args.mainpath, channel=args.channel)
