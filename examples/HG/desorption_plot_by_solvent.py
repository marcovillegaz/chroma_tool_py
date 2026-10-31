"""This script mekor a chromatogram plot to comapre different solvent for the desorption process"""

import os

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

from chroma_tool_py.utils import extract, info
from chroma_tool_py.classes.chromatogram import Chromatogram


def file_filter(chroma_list, criteria):
    """this function filter filename in a list based in a string that must be
    contained in the filename.
    params:
        chroma_list (list): list containing file names of chromatogram pda .txt data
        criteria (str): string to filter chromatograme by it names. It must be
        contianed in Chromatogram.INFO.NAME
    return:
        filtered_list (list): list with filtered chromatograms accordint to criteria"""

    filtered_files = [f for f in chroma_list if criteria in f]
    return filtered_files


# Solvent coding dictionary
solvents = {
    "M1": "2-butanol",
    "M2": "2-propanol",
    "M3": "Etanol",
    "M4": "Acetonitrilo",
    "M5": "Agua",
    "M6": "Acetato de metilo",
    "M7": "Acetato de etilo",
    "M8": "Éter monoetílico del dietilenglicol",
    "M9": "Hexano",
    "M10": "Benceno",
}


# folder with chromatogram of desorprion experimetn
desorption_pda_path = "path/to/HG_ChromNav_Files/PDA_DATA_POINTS/DESORPTION"  # data not included in repo
desorption_fl_path = "path/to/HG_ChromNav_Files/FL_DATA_POINTS/DESORPTION"  # data not included in repo

# SCRIPT PARAMETERS
## Define the sample filter (e.g., 'M3') and the experiment filter (e.g., '4hrs')
# sample_filter = "M10"  # Filter by sample (e.g., 'M3')
criteria = "inf"  # Filter by experiment (e.g., '4hrs')

wavelength = 230  # Wavelength to show in PDA plot
PDA_off_set = 1e5 * 1.5  # Offset for PDA plot

FL_offset = 1e5 * 1  # Offset for FL plot

# ------------------------------------------------------------------------------
# FILTER EXPERIMENTS
files_pda = os.listdir(desorption_pda_path)
files_fl = os.listdir(desorption_fl_path)

filtered_pda_files = file_filter(files_pda, criteria)
filtered_fl_files = file_filter(files_fl, criteria)
print(filtered_pda_files)

## Chromatogram for desorption experiments.
desorption_exp = [
    Chromatogram.create_from_pda(os.path.join(desorption_pda_path, f))
    for f in filtered_pda_files
]

# add fl files
for i, chroma in enumerate(desorption_exp):
    print(filtered_fl_files[i])
    chroma.add_FL(os.path.join(desorption_fl_path, filtered_fl_files[i]), "CH1")

## Creatign figure
fig, ax = plt.subplots(2, figsize=(10, 6))

## Ploting desorption experiments
for i, chroma in enumerate(desorption_exp[0:5]):
    name = chroma.NAME
    name = name.split("_")[0]
    ## PDA PLOT
    ax[0].plot(
        info.time(chroma.INFO),
        extract.by_wavelength(chroma, wavelength) + PDA_off_set * (i + 1),
        label=solvents[name],
    )
    ## FL PLOT
    ax[1].plot(
        chroma.FL_DATA["time"],
        chroma.FL_DATA["CH1"] + FL_offset * (i + 1),
        label=solvents[name],
    )

# SET TITLE, LIMS, LABELS, AXIS, AND LEGEND
ax[0].set_title(f"Detección UV {wavelength} nm", fontsize=11)
ax[1].set_title("Detección por fluoresencia", fontsize=11)

for axi in ax:
    axi.set_xlim(xmin=0, xmax=20)
    axi.set_ylabel("Intensidad relativa")
    axi.set_xlabel("Tiempo de residencia [min]")
    axi.legend(loc="upper right", fontsize=9, borderpad=0.5)
    axi.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    axi.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

# Adjust layout to prevent overlap
plt.tight_layout()
plt.show()
