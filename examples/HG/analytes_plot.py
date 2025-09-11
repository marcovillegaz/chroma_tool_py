"""Thhis script generates a plot of the corresponding chromatograms for the
sample analysis of HG."""

import os

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import pandas as pd

from src.utils import extract, info
from src.utils.peak_finder import peak_finder

from src.classes.chromatogram import Chromatogram
from src.display import chroma_plot


# file of the chromatogram with the 10 analytes
analytes_pda_path = r"path/to/data"
analytes_fl_path = r"path/to/data"

# file of the blank chromatogram
blank_pda_path = r"path/to/data"
blank_fl_path = r"path/to/data"

# SCRIPT PARAMETERS
## Define the sample filter (e.g., 'M3') and the experiment filter (e.g., '4hrs')
wavelength = 280
off_set = 20000  # OFFSET for chromatogram

pda_peak_names = ["ACTN", "CAF", "TMP", "MeP", "BPA", "TCS", "OC", "DEHP"]
fl_peak_names = ["BPA", "4NP"]

# ------------------------------------------------------------------------------
# INSTANCIATING CHROMATOGRAMS
## Chromatogram for analites (from calibration curve)
analytes = Chromatogram.create_from_pda(analytes_pda_path)
analytes.add_FL(analytes_fl_path, "CH1")
## Chromatogram from blank sample
blank = Chromatogram.create_from_pda(blank_pda_path)
blank.add_FL(blank_fl_path, "CH1")

# PEAK FINDING
## Find peaks in PDA pd chromatogram
analytes_pda_peaks = peak_finder(
    extract.by_wavelength(analytes, wavelength),
    info.time(analytes.INFO),
)
analytes_pda_peaks = analytes_pda_peaks.drop(labels=[6, 7, 10, 11, 12, 13], axis=0)
analytes_pda_peaks.reset_index(inplace=True)
analytes_pda_peaks["name"] = pda_peak_names

## Find peaks in FL chromatogram
analytes_fl_peaks = peak_finder(
    analytes.FL_DATA["CH1"],
    analytes.FL_DATA["time"],
)
analytes_fl_peaks = analytes_fl_peaks.drop(labels=[0, 1, 3, 4, 6], axis=0)
analytes_fl_peaks.reset_index(inplace=True)
analytes_fl_peaks["name"] = fl_peak_names
print(analytes_pda_peaks)

""" # FIGURE CREATION
fig, ax = plt.subplots(2, figsize=(10, 6))

# PDA PLOT
## Plot blank and calibration curve
ax[0].plot(
    info.time(blank.INFO),
    extract.by_wavelength(blank, wavelength),
    label="Blanco",
)
## Plot Analytes
ax[0].plot(
    info.time(analytes.INFO),
    extract.by_wavelength(analytes, wavelength) + off_set,
    label="Analitos",
)
## Plot analite peaks
ax[0].scatter(
    analytes_pda_peaks["residence_time"],
    analytes_pda_peaks[["height"]] + off_set,
    s=20,
    marker="x",
    color="red",
)
## PLOT PEAK NAMES
for idx, row in analytes_pda_peaks.iterrows():
    ax[0].annotate(
        row["name"],
        xy=(row["residence_time"], row["height"]),
        xycoords="data",
        xytext=(3, 2),
        textcoords="offset points",
    )

## Plot blank and calibration curve (FL)
ax[1].plot(
    blank.FL_DATA["time"],
    blank.FL_DATA["CH1"],
    label="Blanco",
)
## Plot Analytes
ax[1].plot(
    analytes.FL_DATA["time"],
    analytes.FL_DATA["CH1"] + off_set,
    label="Analitos",
)
# Plot analite peaks
ax[1].scatter(
    analytes_fl_peaks["residence_time"],
    analytes_fl_peaks[["height"]] + off_set,
    s=20,
    marker="x",
    color="red",
)
## PLOT PEAK NAMES
for idx, row in analytes_fl_peaks.iterrows():
    ax[1].annotate(
        row["name"],
        xy=(row["residence_time"], row["height"]),
        xycoords="data",
        xytext=(3, 2),
        textcoords="offset points",
    )


# Plot configuration
ax[0].set_title(f"Detección UV {wavelength} nm", fontsize=11)
ax[1].set_title("Detección por fluoresencia", fontsize=11)

for axi in ax:
    axi.set_xlim(xmin=0, xmax=20)
    axi.set_ylabel("Intensidad relativa")
    axi.set_xlabel("Tiempo de residencia [min]")
    axi.legend(loc="upper left")
    axi.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    axi.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

## Show the plot
plt.tight_layout()
# plt.show() """

chroma_plot.pda_contour(
    analytes,
    y_max=350,
    z_min=-50000,
    # z_max=100000,
    save_path=None,
)
