import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.datasets import electrocardiogram

df1 = pd.read_csv(r"chrom-test1.csv", sep=";", decimal=",")
df = pd.read_csv(r"chrom-test1.csv", sep=";", decimal=",")
df["Int SMA30"] = df["Intensity"].rolling(30).mean()

# Time interval where to search the peak (INPUT)
interval = np.array([4, 9])

# Selecting range in dataFrame
df_c = df[(df["min"] > interval[0]) & (df["min"] < interval[1])]

# DataFrame to narray
x = df_c["min"].to_numpy()
y = df_c["Int SMA30"].to_numpy()

# ******Peak Finding******
peaks, prop = find_peaks(
    y,
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

# ******Data Plotting******
plt.plot(df["min"], df["Int SMA30"])  # Plot complete signal
plt.scatter(x[peaks], prop["peak_heights"], color="r", label="Maxima")  # Plot peaks
plt.axhline(y=0, color="r", linestyle="-")  # Plot baseline at y = 0
plt.legend()
plt.grid()
plt.show()
