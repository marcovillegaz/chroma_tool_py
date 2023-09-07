import ast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.signal import find_peaks
from scipy.integrate import simpson


def read_chromatogram(file_path, channel):
    """This function opens a csv file that contains the chromatogram merged data
    and return the data of the corresponding channel. The the first and second
    derivative are calcualted and stored in the same dataframe.

    Input:
        filename: path of the correpsonding csv file
        channel: channel to integrate
    Output:
        chroma_data: dataframe with the signal, first and second derivative"""

    print("Chromatogram reading".center(50, "="))

    # Reading .csv file with chromatogram data
    print("- Opening file:\n\t", file_path)
    df = pd.read_csv(file_path, sep=";", decimal=".")

    # dataFrame to one-dimensiolnal numpuy array
    y = df[channel].to_numpy()
    y = np.reshape(y, y.size)

    print("- Computing first and second derivative")
    # First derivative
    dy = np.convolve(y, [1, -1]) / 1
    # Second derivative (for future analysis)
    ddy = np.convolve(dy[1:], [1, -1]) / 1

    print("- Defining chromatogram Dataframe\n")
    # Define new formatted DataFrame
    df_out = pd.DataFrame({channel: y, "First diff": dy[1:], "Second diff": ddy[1:]})

    return df_out


def plot_derivatives(
    data,
    xlim,
    same_plot="True",
):
    """This function plots your chromatogram, the first derivative, and the
    second derivative. This funtion is for developing only"""

    colors = ["tab:blue", "tab:orange", "tab:green"]

    # Plot columns in data
    if same_plot == "True":
        fig, axes = plt.subplots(figsize=(10, 5))
        plt.xlim(xlim)

        for i, key in enumerate(data.keys()):
            data[key].plot(label=key, color=colors[i])

        plt.grid()
        plt.legend()

    elif same_plot == "False":
        fig, axes = plt.subplots(3, figsize=(15, 10), sharex=True)
        plt.xlim(xlim)
        plt.grid()

        for i, key in enumerate(data.keys()):
            data[key].plot(
                ax=axes[i], grid="True", ylabel="Intensity", label=key, color=colors[i]
            )
            axes[i].legend()

        plt.legend()

    plt.show()


def peak_finder(data, intervals):
    """This function finds peaks in your chromatogram. First all the peaks in
    the chropmatogram are identified using find_peaks() function from scipy. The
    the peaks area filtered to intervals sleected by the user.

    Input:
        chroma_data: DataFrame with chromatogram data.
        intervals: list with intevervals where the peak of interest are.
            ex. [[0,500],[1500,2000]]
            * The intervals can't be overlapped

    Output:
        peaks_data: Datafram with the index and intesity of peaks in intervals"""

    print("Peak identification".center(50, "="))

    # Peak identification with scipy function
    # The configuration can be change here.
    peaks, prop = find_peaks(
        data.iloc[:, 0].to_numpy(),
        height=4000,  # [min,max]
        threshold=1,  # Threshold is basically the noise level
        distance=2,  # Horizontal distance >=1
        prominence=None,
        width=None,
        wlen=None,
        rel_height=0.5,
        plateau_size=None,
    )

    # Dataframe with information of all peaks in the chromatogram
    all_peaks = pd.DataFrame({"index": peaks, "height": prop["peak_heights"]})
    print("All peaks identified in chromatogram:\n", all_peaks)

    # Filter peaks in intervals and store them in a dictionary

    peaks_data = pd.DataFrame()
    for i, interval in enumerate(intervals):
        filtered_peaks = all_peaks[
            (all_peaks.iloc[:, 0] > interval[0]) & (all_peaks.iloc[:, 0] < interval[1])
        ]

        peaks_data = pd.concat([peaks_data, filtered_peaks], ignore_index=True)

    print("Peaks filtered by intervals:\n", peaks_data)

    return peaks_data


def limits_finder(chroma_data, peaks_data, intervals, min_slope=1):
    """This function find the limits of specified peaks as indexes.

    Inputs
       chroma_data: DataFRame with signal, first and second derivative
       peaks_data: DataFrame with peaks index and height

    Output
       peaks_data: DataFrame with new columns 'limits_idx' and 'limits_val'"""

    width = 5

    print("Limits find".center(50, "="))

    # x[a],x[b] are the limits of peak integration.
    # Arreangement of data to evaluate derivatives
    y = chroma_data.iloc[:, 0].to_numpy()
    dy = chroma_data.iloc[:, 1].to_numpy()

    # Intervals loop for multiple intervals
    limits_idx = []
    limits_val = []
    for i in range(0, len(peaks_data)):
        peak_idx = peaks_data.iloc[:, 0].to_numpy()  # extract peak indexes

        limit_y = ["None"] * 2  # Preallocation of limits y values
        limit_x = ["None"] * 2  # Preallocation of limits x values

        # will it be necessary to add another noise reduction method? for
        # example moving avarange, or this one
        # https://stackoverflow.com/questions/37598986/reducing-noise-on-data

        # width  move de index in order to avoid selectin de same peak
        # as limits, because the first derivative is almost zero at the peak

        # Forward slope finding
        for j in range(peak_idx[i] + width, len(dy)):
            # Flag is for identification of lcoal minima between peaks
            # if flag < 0 there is a local minimun
            flag = dy[j] * dy[j + 1]  #
            if flag < 0:
                limit_x[1] = j + 1
                limit_y[1] = y[j + 1]
                break

            if abs(dy[j]) < min_slope:
                limit_x[1] = j
                limit_y[1] = y[j]
                break

        # Backward slope finding
        for j in reversed(range(0, peak_idx[i] - width)):
            # Flag is for identification of lcoal minima between peaks
            # if flag < 0 there is a local minimun
            flag = dy[j] * dy[j + 1]
            if flag < 0:
                limit_x[0] = j + 1
                limit_y[0] = y[j + 1]
                break

            if abs(dy[j]) < min_slope:
                limit_x[0] = j
                limit_y[0] = y[j]
                break

        limits_idx.insert(i, limit_x)  # Allocating integration limits
        limits_val.insert(i, limit_y)  # Allocating values

    # Allocation in peaks_data DataFrame
    peaks_data["limits idx"] = limits_idx
    peaks_data["limits val"] = limits_val

    print(peaks_data)

    return peaks_data


def peak_integration(chroma_data, peaks_data):
    """This function integrates each peak using simpson method for discrete data

    Inputs
       chroma_data: DataFrame with signal, first and second derivative
       peaks_data: DataFrame with columns [index,height,limits_idx,limit_val]

    Output
       peaks_data: DataFrame with column area added"""

    print("Peak integration".center(50, "="))

    # Extract chromatogram data
    points = chroma_data.iloc[:, 0]
    # Integration limits
    limits_list = peaks_data.iloc[:, 2].to_numpy()
    # Preallocation of areas
    areas = np.zeros((len(peaks_data), 1))
    # Integration of peaks
    for i, limit in enumerate(limits_list):
        y = points.iloc[limit[0] : limit[1]]
        x = range(limit[0], limit[1])

        areas[i] = simpson(y, x, dx=1.0, axis=-1, even=None)

    # Save areas in dataframe
    peaks_data["Area"] = areas
    print(peaks_data)

    return peaks_data


def plot_results(chroma_data, peaks_data, intervals="None"):
    """This function plot the resuls of this script like: intervals, peaks,
    limits,areas"""

    print("Plotting results".center(50, "="))

    fig, ax = plt.subplots(figsize=(14, 7))

    chroma_data.iloc[:, 0].plot(grid="True", ylabel="Intensity", label="chromatogram")
    chroma_data.iloc[:, 1].plot(grid="True", label="First derivative")

    # Get and set limits
    _, ymax = ax.get_ylim()

    # Plot intervals
    if intervals != "None":
        for i, interval in enumerate(intervals):
            plt.axvline(x=interval[0], color="tab:orange", linestyle="dotted")
            plt.axvline(x=interval[1], color="tab:orange", linestyle="dotted")

            # Add text to interval
            plt.text(
                interval[0],
                ymax * 0.5,
                "user interval " + str(i + 1),
                ha="center",
                va="center",
                rotation="vertical",
                backgroundcolor="white",
            )

    # Plot peaks
    x_peak = peaks_data.iloc[:, 0]
    y_peak = peaks_data.iloc[:, 1]
    plt.scatter(x_peak, y_peak, s=20, marker="x", color="red")

    # Add peak identification number
    for i in range(0, len(x_peak)):
        plt.text(
            x_peak.iloc[i],
            y_peak.iloc[i] + 4000,
            str(i + 1),
            ha="center",
            va="center",
            rotation="horizontal",
        )

    # Plot integration limits
    limits_idx = peaks_data.iloc[:, 2].to_numpy()
    limits_val = peaks_data.iloc[:, 3].to_numpy()

    for i in range(0, len(limits_idx)):
        x_ab = limits_idx[i]
        y_ab = limits_val[i]
        plt.scatter(x_ab, y_ab, s=20, marker="x", color="green")

    # Plot integrated areas
    for limit in limits_idx:
        a = limit[0]
        b = limit[1]

        y = chroma_data.iloc[a : b + 1, 0]
        iy = y.values
        ix = list(range(a, b + 1))

        verts = [(a, 0), *zip(ix, iy), (b, 0)]
        poly = Polygon(verts, facecolor="0.9", edgecolor="0.5")
        ax.add_patch(poly)

    plt.legend()
    plt.show()


def main(file_path, channel, intervals, image="True"):
    # Read chromatogram and computes the first and secon dderivatives
    chroma_data = read_chromatogram(file_path, channel)

    # Visualizaing derivatives
    # plot_derivatives(chroma_data, same_plot="True", xlim=[0, 3000])

    # Find peaks in specified intervals
    peaks_data = peak_finder(chroma_data, intervals)

    # Find integration limits of peaks
    peaks_data = limits_finder(chroma_data, peaks_data, intervals, min_slope=5)

    # Integration of peaks
    peaks_data = peak_integration(chroma_data, peaks_data)

    # Plot results
    if image == "True":
        plot_results(chroma_data, peaks_data, intervals)


# INPUTS
file_path = r"path/to/data"
channel = "215nm"
# Time interval where to search the peak (INPUT)
intervals = [[100, 600], [1000, 1500], [2360, 2966]]

main(file_path, channel, intervals, image="True")
