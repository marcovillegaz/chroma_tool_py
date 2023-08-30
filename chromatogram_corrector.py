import os
import pybeads as be
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams["figure.facecolor"] = "w"


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1 :] / n


def read_chromatogram(file_path):
    # This function opens a csv file that contains the chromatogram data and
    # return the data as numpy arrays.
    # Input:
    #   filename: path of the correpsonding csv file
    # Output:
    #   x: array of time (or number of data)
    #   y: intensity of signal

    print("\tOpening", file_path)
    # Reading .csv file with chromatogram data
    df = pd.read_csv(file_path, sep=";", decimal=",")
    # Transform data to numpy array
    y = df["Intensity"].to_numpy()
    x = list(range(0, len(y)))

    return x, y


def formatted_path(dir_path, file_name, extention=""):
    # For a folder that contain multiple files, this function  return the path
    # of the corresponding file in folder
    # Input:
    #   dir_path: string of the corresponding folder path
    #   Extention of the file (.csv,.png, etc.)
    # Output:
    #   file_path: string of the corresponding file path

    dir_path = dir_path + "\{}" + extention
    file_path = dir_path.format(file_name)

    return file_path


def get_chroma_name(full_name):
    # This function get the name of the chromatogram splitting the
    # the filename extention ex. <A0_01>.csv
    aux = full_name.split(".")
    chroma_name = aux[0]
    return chroma_name


def chroma_plot(
    data_old,
    data_new,
    save_path="None",
    xlimit="None",
):
    # Creating figure
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 7), sharex=True)

    data_old.plot(
        ax=axes[0],
        title="Raw chromatogram",
        grid="True",
        ylabel="Intensity",
        xlim=xlimit,
    )
    data_new.plot(
        ax=axes[1],
        title="Corrected with BEADS",
        grid="True",
        ylabel="Intensity",
        xlim=xlimit,
    )

    # Show or save image
    if save_path == "None":
        plt.show()
    else:
        print("\tSaving in plot in:")
        print("\t\t" + save_path)
        plt.savefig(save_path, dpi=300)

    plt.close()


def beads_correction(y):
    # BEADS ALGORITHM PARAMETERS
    fc = 0.006
    d = 1
    r = 6
    amp = 0.8
    lam0 = 0.5 * amp
    lam1 = 5 * amp
    lam2 = 4 * amp
    Nit = 15
    pen = "L1_v2"

    # BEADS algortihm to reduce noise and correct baseline
    signal_est, bg_est, cost = be.beads(
        y, d, fc, r, Nit, lam0, lam1, lam2, pen, conv=None
    )
    return signal_est, bg_est, cost


def main(
    main_dir_path,
    input_data_path,
    output_data_path,
    output_image_path="None",
    exception_path="None",
):
    print("The program has been started".center(79, "="))

    # Get files in input_path
    dir_list = os.listdir(input_data_path)

    intervals = pd.DataFrame(
        {"Chromatogram": dir_list, "Intervals": [None] * len(dir_list)}
    )

    intervals.to_csv(
        main_dir_path + "\Intervals.csv",
        sep=";",
        header=True,
        index=False,
    )

    # Read exception to BEADS correction
    if exception_path != "None":
        exceptions = pd.read_csv(exception_path)
        exceptions = exceptions["Exception"].tolist()
    else:
        exceptions = []

    # Formated strings
    counter = "({}/" + str(len(dir_list)) + ")"
    chroma_path = input_data_path + "\{}"
    save_data_path = output_data_path + "\{}"
    save_image_path = output_image_path + "\{}.png"

    i = 0
    # Loop of chromatograms
    for file_name in dir_list:
        # Counter
        i = i + 1
        # Extract chromatogram name (get_chroma_name)
        chroma_name = file_name.split(".")
        chroma_name = chroma_name[0]
        print(counter.format(str(i)), "Processing chromatogram", chroma_name)

        print("\tReading data...")
        chroma_data = pd.read_csv(chroma_path.format(file_name), sep=";", decimal=".")

        # BEADS correction
        new_chroma_data = pd.DataFrame()
        if chroma_name in exceptions:
            print("\tThis chromatogram is and exception to BEADS algorthim")
            new_chroma_data = chroma_data
        else:
            print("\tApplaying BEADS algorthim")
            for key in chroma_data:
                # Datafram to numpy array
                signal = chroma_data[key].to_numpy()
                # BEADS function
                signal_est, bg_est, cost = beads_correction(signal)
                # numpy array to Dataframe
                new_chroma_data[key] = signal_est

        print("\tSaving in corrected signals in:")
        print("\t\t" + save_data_path.format(file_name))
        chroma_data.to_csv(
            save_data_path.format(file_name),
            sep=";",
            header=True,
            index=False,
        )

        # Plot raw and correct chromatograms for comparisson
        if output_image_path != "None":
            chroma_plot(
                chroma_data,
                new_chroma_data,
                save_path=save_image_path.format(chroma_name),
                xlimit=[0, 3000],
            )


# INPUT
# \MainDirectory
#   \Data (Chromatogram data)
#   \Image (Chromatogram images)
#   Intervals.csv
#   Results.csv

# Main directory path were the subfolders are stored
main_dir_path = (
    r"path/to/data"
)
# Directory path were raw chromatograms are stored
input_data_path = r"path/to/data"
# Directory path to store corrected chromatograms
output_data_path = (
    r"path/to/data"
)
# Directory path to store images that compare raw and corrected chromatograms
output_image_path = (
    r"path/to/data"
)

# You can first run the code with out exceptions, then anailze the images to
# discard chromatogramas that has a bad correction and write them in
# exceptions.txt
exception_path = r"path/to/data"

main(
    main_dir_path, input_data_path, output_data_path, output_image_path, exception_path
)


# IN FUTURE APLY os.path.join() to add paths more intelligently
