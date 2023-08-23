"""This script is a test of plotting chromatogram data using matploplib"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# INPUT
dir_path = r"path/to/data"
dir_list = os.listdir(dir_path)  # name of files in directory
print(len(dir_list))


n = 32  # number of chromatograms readed

file_path = dir_path + "\{}"

fig, ax = plt.subplots(figsize=(10, 5))  # Creating figure,ax
ax.set_xlim(0, 3500)
ax.set_ylabel("Intensity")
ax.set_xlabel("Retention time [min]")
ax.set_title("Example cromatogram")

for i in range(0, n):
    # Reading .csv file with chromatogram data
    print(file_path.format(dir_list[n]))
    df = pd.read_csv(file_path.format(dir_list[i]), sep=";", decimal=",")

    y = df["Intensity"].to_numpy()
    x = list(range(0, len(y)))

    # Plotting chromatograms.
    ax.plot(x, y, label=dir_list[i])


ax.legend()
plt.show()
