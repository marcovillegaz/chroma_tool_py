import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.integrate import trapezoid


def read_chromatogram(file_path, channel):
    """This function opens a csv file that contains the chromatogram data and
    return the data as numpy arrays.

    Input:
      filename: path of the correpsonding csv file
      channel:
    Output:
      x: array of time (or number of data)
      y: intensity of signal"""

    # Reading .csv file with chromatogram data
    print("\tOpening file")
    df = pd.read_csv(file_path, sep=";", decimal=".")

    # dataFrame to one-dimensiolnal numpuy array
    y = df[channel].to_numpy()
    y = np.reshape(y, y.size)

    # Finite difference calculation
    print("\tComputing first derivative\n")
    dy = np.convolve(y, [1, -1]) / 1

    # Define new formatted DataFrame
    df_out = pd.DataFrame({channel: y, "First diff": dy[1:]})

    return df_out


def limits_search(dy, peaks_df, min_slope=1):
    """This function find the limits of specified peaks as indexes.

    Inputs
       dy: numpy array with with the finite derivative (slopes of signal)
       peaks_df: DataFrame with peaks information
       min_slope: minimum slope criteria for defining peak limits
    Output
       peaks_df: DataFrame with peaks information. Limits added to."""

    # x[a],x[b] are the limits of peak integration.
    dy = np.absolute(dy)
    peaks_idx = peaks_df["index"].to_numpy()

    # Peaks loop
    limits_slope = []  # Preallocation
    limits_idx = []
    for i, peak in enumerate(peaks_idx):
        limit_slope = ["None"] * 2
        limit_idx = ["None"] * 2
        # Forward slope finding
        for j in range(peak, len(dy)):
            if dy[j] < min_slope:
                limit_slope[1] = dy[j]
                limit_idx[1] = j
                break
        # Backward slope finding
        for j in reversed(range(0, peak)):
            if dy[j] < min_slope:
                limit_slope[0] = dy[j]
                limit_idx[0] = j
                break

        limits_idx.insert(i, limit_idx)  # Allocating integration limits
        limits_slope.insert(i, limit_slope)  # Allocating limits slops

    peaks_df["limits idx"] = limits_idx
    peaks_df["slope val"] = limits_slope

    print(peaks_df)
    return peaks_df


file_path = r"path/to/data"
channel = "215nm"
# Time interval where to search the peak (INPUT)
interval = [0, 2500]

data = read_chromatogram(file_path, channel)
print(data)


# PEAK FIND USING SCIPY
peaks, prop = find_peaks(
    data[channel].to_numpy(),
    height=5000,  # [min,max]
    threshold=1,  # Threshold is basically the noise level
    distance=2,  # Horizontal distance >=1
    prominence=None,
    width=None,
    wlen=None,
    rel_height=0.5,
    plateau_size=None,
)

print("peaks\n", peaks)
print("prop\n", prop)
print("peak height\n", prop["peak_heights"])

# Dataframe with peaks informations.
peaks_data = pd.DataFrame({"index": peaks, "height": prop["peak_heights"]})
print(peaks_data)
# Filter peaks in range set by user
peaks_data = peaks_data[
    (peaks_data["index"] > interval[0]) & (peaks_data["index"] < interval[1])
]
print("\tThere are", len(peaks_data), "peaks have been identified in", interval)


# IDENTIFY PEAKS LIMITS
peaks_data = limits_search(data["First diff"].to_numpy(), peaks_data, min_slope=5)

# PEAK INTEGRATION
# areas = []
# limits = peaks_data["limits idx"].to_list()
# for i, peak in enumerate(peaks_data):
#  limit = limits[i]
# integration_data = peaks_data[
#     (peaks_data["index"] > limit[0]) & (peaks_data["index"] < limit[1])
# ]
# area = trapezoid(integration_data["Intensity"], integration_data["index"])
# areas.insert(i, area)

# print("Area are:", areas)


# PLOT INTERVAL AN IDENTIFIED PEAK
fig, ax = plt.subplots(figsize=(10, 5))
ylabel = "Intensity"
xlim = 3000
plt.axvline(x=interval[0], color="r", linestyle="--")
plt.axvline(x=interval[1], color="r", linestyle="--")
data[channel].plot(label="Chromatogram")
data["First diff"].plot(label="First derivative")
plt.scatter(peaks_data["index"], peaks_data["height"], color="r", label="Maxima")

# Plot limits.
# limits = peaks_data["limits idx"].to_list()
# print(limits)
# plt.axvline(x=limits[0][0], color="g", linestyle="dotted")
# plt.axvline(x=limits[0][1], color="g", linestyle="dotted")

ax.legend()
plt.grid()
plt.show()
