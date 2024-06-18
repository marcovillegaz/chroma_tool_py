import numpy as np

from utils.peak_finder import peak_finder


class Chromatogram:
    # This is a class attribute
    all = []

    def __init__(self, NAME, INFO, PDA_DATA=None, FV_DATA=None):
        # Run validation to reacive arguments
        assert type(NAME) is str, f"{NAME} must be a string!"

        # Assign to self object (instance attributes)
        self.NAME = NAME
        self.INFO = INFO
        self.PDA_DATA = PDA_DATA

        # Action to execute
        Chromatogram.all.append(self)

    # Return an unambiguous string representation of the object
    def __repr__(self) -> str:
        return f"Chromatogram('{self.NAME}')\n\tPDA:'{self.INFO})"

    @classmethod
    def from_file(cls, file_path):
        """Create an instance using the name of the data file"""

        # Extract chromatogram name from filename
        path_list = file_path.split("\\")
        filename = path_list[-1].split(".")

        # Create the instance (important to return)
        return cls(name=filename[0])

    @classmethod
    def create_from_pda(cls, file_path, detector=None):
        """This method open the data obtained in a Diode Array Detector (DAD) as
        a text file and create an instance of Chromatogram class"""

        print("Openning DAD file...")

        # Open the .txt file
        with open(file_path, "r") as file:
            lines = file.readlines()

        # "Data comprises raw, unprocessed facts that need context to become
        #  useful, while information is data that has been processed, organized,
        #  and interpreted to add meaning and value."

        # Extract PDA information and data in .txt file (depend of HPLC software)
        data = []
        info = []
        for i, line in enumerate(lines):
            if i < 11:
                info.append(line)
            elif i > 11:
                row = list(map(int, line.split()))
                data.append(row)

        # PDA data
        data = np.array(data)

        # PDA information
        info_dict = {}
        for item in info:
            item = item.replace("\n", "").replace(",", ".")
            key, value = item.split("\t")
            info_dict[key] = value

        # CHromatogram name
        path_list = file_path.split("\\")
        name_list = path_list[-1].split(".")

        # Instanciate object
        return cls(
            NAME=name_list[0],
            INFO=info_dict,
            PDA_DATA=data,
        )

    def find_peaks(self, wavelength, show=None):
        """This function find de corresponding peaks in single wavelength
        chromatogram (Time vs Intensity)"""

        print("Peak identification".center(50, "="))

        time_array, intensity_2d = Extract_SingleWavelength(self.PDA_data, wavelength)
        peaks_data = peak_finder(intensity_2d, time_array)

        print(f"Peaks identified in chromatogram at {wavelength}nm:\n", peaks_data)

        if show == True:
            plot_results(intensity_2d, time_array, peaks_data)

        return peaks_data
