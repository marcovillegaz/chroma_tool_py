import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.signal import find_peaks


def Extract_SingleWavelength(PDA_data, wavelength, time, wl_list):
    """This function extract the vector intensity at given wavelengths and
    store them in easy to work with dataframe.

    input:
        PDA_data: matrix that contains all the PDA data matrix
        wavelength: vector with the corresponding wavelengths of the PDA
        wl_list: list of wavelengths that you want to extract

    output:
        chroma_df: dataFrame with the intensity at the corresponding wavelengths"""

    column_names = [str(wl) + "nm" for wl in wl_list]
    index = np.where(np.isin(wavelength, wl_list))[0]
    chroma_df = pd.DataFrame(data=PDA_data[:, index], columns=column_names)

    print(chroma_df)
    return chroma_df


def peak_finder(chroma_df):
    """This function finds peaks in your chromatogram. First all the peaks in
    the chropmatogram are identified using find_peaks() function from scipy. The
    the peaks area filtered to intervals sleected by the user.

    Input:
        chroma_df: dataframe with the information of specified wavelengths
    Output:
        peaks_df: Dataframe with the index of beaks by wavelengths"""

    print("Peak finder".center(50, "="))
    channels = chroma_df.columns

    # Peak identification with scipy function
    all_arrays = []
    for channel in channels:
        # The configuration can be change here.
        peaks, _ = find_peaks(
            chroma_df[channel].to_numpy(),
            height=4000,  # [min,max]
            threshold=1,  # Threshold is basically the noise level
            distance=2,  # Horizontal distance >=1
            prominence=None,
            width=None,
            wlen=None,
            rel_height=0.5,
            plateau_size=None,
        )

        # stored peaks list in a bigger list
        all_arrays.append(peaks)
        print(channel + ":", peaks)

    # Find the maximum length among all inner lists
    max_length = max(len(lst) for lst in all_arrays)

    # Pad the arrays with np.nan values to make them of equal length
    padded_arrays = [
        np.concatenate([arr, np.full(max_length - len(arr), np.nan)])
        for arr in all_arrays
    ]

    # Store peaks indexes in a dataFrame
    peaks_df = pd.DataFrame()
    for i, channel in enumerate(channels):
        peaks_df[channel] = padded_arrays[i]

    print("\nPeaks index by wavelength:\n", peaks_df)

    return peaks_df


def plot_peaks(chroma_df, time, peaks_df, peaks_name="None"):
    """This function plot the channels and the peaks identified in each channel"""

    print("Plotting peaks".center(50, "="))

    fig, ax = plt.subplots(figsize=(10, 5))  # Creating figure,ax
    ax.set_ylabel("Intensity")
    ax.set_xlabel("Retention time [min]")
    ax.set_xlim(0, time[-1])
    ax.set_title("Chromatogram peaks")
    channels = chroma_df.columns
    for channel in channels:
        intensity = chroma_df[channel].to_numpy()
        ax.plot(time, intensity, label=channel)
        peaks_indexes = peaks_df[channel].dropna()

        for peak in peaks_indexes:
            x_peak = time[int(peak)]
            y_peak = intensity[int(peak)]
            ax.scatter(x_peak, y_peak, s=20, marker="x", color="red")

    # Add peak identification number (or name FUTURE)
    if peaks_name == "number":
        for i in range(0, len(x_peak)):
            plt.text(
                x_peak[i],
                y_peak[i] + 1000,
                str(i + 1),
                ha="center",
                va="center",
                rotation="horizontal",
            )

    plt.xticks(np.arange(time[0], time[-1], step=1))
    plt.legend()
    plt.show()
