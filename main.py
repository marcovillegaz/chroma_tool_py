import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
from scipy.signal import find_peaks
from scipy.integrate import trapezoid


# Compute central difference derivative for numpy arrays
def central_diff(x, y):
    # Preallocation
    y_diff = np.empty([len(x)])
    y_diff[:] = np.nan
    # Computing central finite difference
    delta_x = x[2:] - x[:-2]
    delta_y = y[2:] - y[:-2]
    y_diff[1 : len(x) - 1] = delta_y / delta_x

    return y_diff


def limits_search(dy, peaks, min_slope=0.8):
    # This function finf the limits of specified peaks as indexes
    # Inputs
    #   dy: narray with with the finite derivative (slopes of signal)
    #   peaks: narray with peaks position index
    #   min_slope: minimun slope criteria for defining peak limits
    # Output
    #   peaks_df: data fram with indexs information

    # x[a],x[b] are the limits of peak integration.
    a = np.zeros(len(peaks))
    b = np.zeros(len(peaks))
    dy = np.absolute(dy)

    # Peaks loop
    for i in range(0, len(peaks)):
        # Forward lope finding
        for j in range(peaks[i], len(dy)):
            if dy[j] < min_slope:
                b[i] = j
                break
        # Backward slope finding
        for j in reversed(range(0, peaks[i])):
            if dy[j] < min_slope:
                a[i] = j
                break

    peaks_data = {"peak idx": peaks, "a idx": a, "b idx": b}
    peaks_df = pd.DataFrame(peaks_data)
    return peaks_df


# Importing data of one csv
df = pd.read_csv(r"chrom-test1.csv", sep=";", decimal=",")
print("=" * 50 + "\n", df)

# Unit change minutes to seconds
df["sec"] = df["min"] * 60
print("=" * 50 + "\n", df)

# Noise reduction with moving means
df["Int SMA30"] = df["Intensity"].rolling(30).mean()
df.dropna(inplace=True)
print("=" * 50 + "\n", df)

# Central finite difference fo the first derivative[Int/sec]
df["first diff"] = central_diff(df["sec"].to_numpy(), df["Int SMA30"].to_numpy())
df.dropna(inplace=True)
print("=" * 50 + "\n", df)


# ******Peak Finding******
# Time interval where to search the peak (INPUT)
interval = np.array([0, 9])

# Selecting range in dataFrame
df_pf = df[(df["min"] > interval[0]) & (df["min"] < interval[1])]
print("=" * 50 + "\n", df_pf)

# find_peak() function
y = df_pf["Int SMA30"].to_numpy()
x = df_pf["min"].to_numpy()

peaks, prop = find_peaks(
    y,
    height=5000,  # [min,max]
    threshold=0.05,  # Threshold is basically the noise level
    distance=2,  # Horizontal distance >=1
    prominence=None,
    width=0,
    wlen=None,
    rel_height=0.5,
    plateau_size=None,
)
print("=" * 50 + "\n", prop.keys())
print("=" * 50 + "\n", prop["left_ips"])
print("=" * 50 + "\n", prop["right_thresholds"])

# dy = df_pf["first diff"].rolling(30).mean()
dy = df_pf["first diff"].to_numpy()  # slope of signal as narray
peaks_df = limits_search(dy, peaks, min_slope=0.8)

print("=" * 50)
print("Peaks index information\n", peaks_df)


# ******Integration in range****** ARREGLR ESTA ÁPRTE

a = int(peaks_df["a idx"].tolist())
b = int(peaks_df["a idx"].tolist())
area = np.zeros(len(peaks))
print(y[a[0]])
for i in range(0, len(peaks)):
    alim = a[i]
    blim = b[i]
    area[i] = trapezoid(y[alim:blim], x[alim:blim])

print(area)


# print("area:", area)

# ******Data Plotting******
fix, ax = plt.subplots()
ax.plot(df["min"], df["Int SMA30"])  # Plot complete signal
# plt.plot(df["min"], df["first diff"])  # Plot complete signal
ax.plot(x, dy)
ax.scatter(
    df_pf["min"].to_numpy()[peaks], prop["peak_heights"], color="r", label="Maxima"
)  # Plot peaks

ax.axhline(y=0, color="r", linestyle="-")  # Plot baseline at y = 0


# Make the shaded region
# verts = [(x[a], 0), *zip(x[a:b], y[a:b]), (x[b], 0)]
# poly = Polygon(verts, facecolor="0.9", edgecolor="0.5")
# ax.add_patch(poly)

plt.legend()
plt.grid()
plt.show()
