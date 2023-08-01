"""This script is a test of plotting chromatogram data using matploplib"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Reading .csv file with chromatogram data
df1 = pd.read_csv(r"chrom-test1.csv", sep=";", decimal=",")
df2 = pd.read_csv(r"chrom-test2.csv", sep=";", decimal=",")
# print(df.head())

# Data frame to numpy array
rt1 = df1["min"].to_numpy()
int1 = df1["Intensity"].to_numpy()

rt2 = df2["min"].to_numpy()
int2 = df2["Intensity"].to_numpy()

# Plotting chromatograms.
fig, ax = plt.subplots(figsize=(10, 5))  # Creating figure,ax

ax.plot(rt1, int1, label="260 nm")
ax.plot(rt2, int2, label="215 nm")

ax.set_xlim(0, 10)
ax.set_ylabel("Intensity")
ax.set_xlabel("Retention time [min]")
ax.set_title("Example cromatogram")
ax.annotate(
    "PCB77 peak",
    xy=(6.430, 2e4),
    xytext=(6, 2.5e4),
)
ax.legend()
plt.show()
