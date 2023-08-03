import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

df1 = pd.read_csv(r"chrom-test1.csv", sep=";", decimal=",")
df = pd.read_csv(r"chrom-test1.csv", sep=";", decimal=",")
df["Int SMA30"] = df["Intensity"].rolling(15).mean()

x = df["min"].to_numpy()
y = df["Int SMA30"].to_numpy()

# ******Peak Finding******
peaks = find_peaks(y, height=2, threshold=0.5, distance=2)
h = peaks[1]["peak_heights"]
pp = x[peaks[0]]
# ******Minima Finding******
# ******Data Plotting******
plt.plot(x, y)
plt.scatter(pp, h, color="r", label="Maxima")
plt.legend()
plt.grid()
plt.show()
