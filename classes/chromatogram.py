import numpy as np

from utils.single_wavelength import Extract_SingleWavelength
from utils.peaks import peak_finder
from plots.plot_peaks import plot_results


class Chromatogram:

    # This is a class attribute
    detector = "JASCO MD-4010"
    all = []

    def __init__(self, name, PDA_data=None, FV_data=None):
        # Run validation to reacive arguments
        assert type(name) is str, f"{name} must be a string!"

        # Assign to self object (instance attributes)
        self.name = name
        self.PDA_data = PDA_data
        self.FV_data = FV_data

        # Action to execute
        Chromatogram.all.append(self)

    # Return an unambiguous string representation of the object
    def __repr__(self) -> str:
        return f"Chromatogram('{self.name}')"

    @classmethod
    def from_file(cls, file_path):
        """Create an instance using the name of the data file"""

        # Extract chromatogram name from filename
        path_list = file_path.split("\\")
        filename = path_list[-1].split(".")

        # Create the instance (important to return)
        return cls(name=filename[0])

    @classmethod
    def open_PDA(cls, file_path, detector=None):
        """This method open the data obtained in a Diode Array Detector (DAD) and
        stored in a text file"""

        print("Openning DAD file...")

        # Open the .txt file
        with open(file_path, "r") as file:
            lines = file.readlines()

        # Extract PDA information in .txt file (depend of HPLC software)
        PDA_data = []
        PDA_info = []
        for i, line in enumerate(lines):
            if i < 11:
                PDA_info.append(line)
            elif i > 11:
                row = list(map(int, line.split()))
                PDA_data.append(row)

        PDA_data = np.array(PDA_data)

        # Extract PDA info and save in dictionary
        data_dict = {}
        for item in PDA_info:
            item = item.replace("\n", "")
            item = item.replace(",", ".")
            key, value = item.split("\t")
            data_dict[key] = value

        # Start and end time
        time = np.array(
            [
                float(data_dict["START_TIME"].replace("min", "")),
                float(data_dict["END_TIME"].replace("min", "")),
            ]
        )
        # Start and end wavelength
        wavelength = np.array(
            [
                float(data_dict["START_WL"].replace("nm", "")),
                float(data_dict["END_WL"].replace("nm", "")),
            ]
        )

        final_dict = {"Intensity": PDA_data, "Time": time, "Wavelength": wavelength}
        if detector is str:
            final_dict["Detector"] = detector
        else:
            final_dict["Detector"] = "None"

        # Extract chromatogram name from filename
        path_list = file_path.split("\\")
        name_list = path_list[-1].split(".")

        return cls(
            name=name_list[0],
            PDA_data=final_dict,
        )

    def find_peaks(self, wavelength, show=None):
        """This function find de corresponding peaks in single wavelength
        chromatogram (Time vs Intensity)"""

        time_array, intensity_2d = Extract_SingleWavelength(self.PDA_data, wavelength)

        print(f"Chromatogram at {wavelength} (nm)\n")

        peaks_data = peak_finder(intensity_2d, time_array)

        if show == True:
            plot_results(intensity_2d, time_array, peaks_data)

        return peaks_data
