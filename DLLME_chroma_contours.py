import os

from classes.chromatogram import Chromatogram
from classes.analyte import Analyte
from chroma_display import chroma_plot

folder = "DLLLME_Chromatograms"
files = os.listdir(folder)

print(files)

# Create instances of Chromatogram class for each file
chromatograms = [
    Chromatogram.create_from_pda(os.path.join(folder, file)) for file in files[0:3]
]


# Print the created Chromatogram instances
for chromatogram in chromatograms:
    print(f"Creating contour of {chromatogram.NAME}")
    chroma_plot.pda_contour(
        chromatogram,
        y_max=400,
        z_min=-1000,
        z_max=40000,
        save_path=folder,
    )

lastChroma = Chromatogram.create_from_pda(os.path.join(folder, files[-1]))
print(f"Creating contour of {chromatogram.NAME}")
chroma_plot.pda_contour(
    lastChroma,
    y_max=400,
    z_min=-1000,
    z_max=100000,
    save_path=folder,
)
