from classes.chromatogram import Chromatogram
from classes.analyte import Analyte

# Put this function in the same file
# import chroma_display as chdisp
from chroma_display import chroma_plot

file_path = r"GWR_project\TEST__13102023 ACTN_test_012 (PDA).txt"
# Open PDA data and set as attribute
chroma1 = Chromatogram.create_from_pda(file_path=file_path)
# chroma1 = chroma1.open_FD(file_path="CECs_Analysis.txt", detector="MD-4010")


print("\nPrinting all instances:")
for instance in Chromatogram.all:
    print(instance)

# chroma_plot.pda_contour(chroma1, z_min=-1000)  # chdisp.pda_contour
# chroma_plot.pda_2d(chroma1, wl_list=[275, 300, 365, 25])  # chdisp.pda_2d
chroma_plot.pda_spectrum(chroma1, time_list=[4.5, 5, 5.5])
#

""" # preliminar peak analysis
peaks_data = chroma1.find_peaks(wavelength=276, show=False)

# Define analytes
analyte_1 = Analyte(
    "Acetominophen",
    residence_time=peaks_data["index"][6],
)

print(Analyte.all)

analyte_1.extract_spectrum(chroma1.PDA_data)
 """
