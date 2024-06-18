import os
import pybeads as be
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams["figure.facecolor"] = "w"


def moving_average(a, n=20):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1 :] / n


def chroma_plot(old_chroma_data, new_chroma_data):
    # Creating figure
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 7), sharex=True)

    old_chroma_data.plot(
        ax=axes[0],
        title="Raw chromatogram",
        grid="True",
        ylabel="Intensity",
    )
    new_chroma_data.plot(
        ax=axes[1],
        title="Corrected with BEADS",
        grid="True",
        ylabel="Intensity",
    )

    print("\tWhen you are ready, close de window containing the figure.")
    plt.show()


def beads_correction(y):
    # Sigmoid function
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

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


def main(main_path):
    print("The program has been started".center(79, "="))

    # Get files in input_path
    data_path = os.path.join(main_path, "merged_data")
    dir_list = os.listdir(data_path)

    # Create intervals files for future integration
    intervals = pd.DataFrame(
        {"Chromatogram": dir_list, "Intervals": [None] * len(dir_list)}
    )

    # Formated strings
    counter = "({}/" + str(len(dir_list)) + ")"
    # Loop of chromatograms
    for i, chroma_name in enumerate(dir_list):
        # Path of chromatogram i
        chroma_path = os.path.join(data_path, chroma_name)

        # Counter
        i = i + 1

        # Extract chromatogram name (get_chroma_name)
        print(counter.format(str(i)), "Processing chromatogram", chroma_name)

        print("\tReading data...")
        old_chroma_data = pd.read_csv(chroma_path, sep=";", decimal=".")

        # BEADS correction
        beads_chroma_data = pd.DataFrame()
        print("\tApplaying BEADS algorthim...\n")
        for key in old_chroma_data:
            # Datafram to numpy array
            signal = old_chroma_data[key].to_numpy()
            # BEADS function
            signal_est, bg_est, cost = beads_correction(signal)
            # numpy array to Dataframe
            beads_chroma_data[key] = signal_est

        #        print("old_data\n", old_chroma_data)
        #       print("new_data\n", new_chroma_data)

        chroma_plot(old_chroma_data, beads_chroma_data, mv:)

        print("\tyes: overwarite data corrected with BEAD algorithm")
        print("\tno: don't apply any correction")
        print("\tmv: denoisingt with moving avarage")

        answer = input("\ntype oyour answer")

        if answer == "yes":
            print("Overwriting new data in: ", chroma_name)
            new_chroma_data.to_csv(chroma_path, sep=";", header=True, index=False)

        elif answer == "mv":
            print("Applaying moving average denoising...")

            new_chroma_data = pd.DataFrame()
            for key in old_chroma_data:
                data = old_chroma_data[key].to_numpy()
                new_chroma_data[key] = moving_average(data, n=20)

            print(old_chroma_data)

        # Over write corrected data
        # if answer == "yes":
        # Close plot window

        # Over write information in the same file
        #   print("\tSaving in corrected signals in:")

        #


# INPUT
# \MainDirectory
#   \Data (Chromatogram data)
#   \Image (Chromatogram images)
#   Intervals.csv
#   Results.csv

# Main directory path were the subfolders are stored
main_path = r"path/to/data"

# You can first run the code with out exceptions, then anailze the images to
# discard chromatogramas that has a bad correction and write them in
# exceptions.txt
exception_path = r"path/to/data"

main(main_path)


# IN FUTURE APLY os.path.join() to add paths more intelligently
