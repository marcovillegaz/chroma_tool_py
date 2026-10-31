import numpy as np
import pandas as pd
from pathlib import Path

class Chromatogram:
    # This is a class attribute
    all = []

    def __init__(self, NAME, INFO, PDA_DATA=None, FL_DATA=None):
        # Run validation to reacive arguments
        if not isinstance(NAME, str):
            raise TypeError(f"{NAME!r} must be a string!")

       # Instance attributes
        self.NAME = NAME
        self.INFO = INFO if INFO is not None else {}
        self.PDA_DATA = PDA_DATA if PDA_DATA is not None else {}
        self.FL_DATA = FL_DATA if FL_DATA is not None else {}

        # Action to execute
        Chromatogram.all.append(self)

    # Return an unambiguous string representation of the object
    def __repr__(self) -> str:
        return f"Chromatogram('{self.NAME}')\n\tPDA:'{self.INFO})"

    # ---------- FL ----------
    @classmethod
    def create_from_fl(cls, file_path):
        """Create an instance from a Fluorescence Detector (FL) .csv file."""

        # Read CSV using pandas (FL data is a dataframe with two columns)
        fl_data = pd.read_csv(file_path,sep=";",decimal=",")
        fl_data = fl_data.rename(columns={"min": "Time"})

        # Extract name from filename
        name = Path(file_path).stem   # filename without extension
        name = name.removesuffix("(01)").strip()  # ChromNAV channel suffix

        return cls(
            NAME=name,
            INFO = None,
            FL_DATA=fl_data
        )

    # ---------- PDAL ----------
    @classmethod
    def create_from_pda(cls, file_path):
        """This method open the data obtained in a Diode Array Detector (DAD) as
        a text file and create an instance of Chromatogram class"""

        # Open the .txt file (ChromNAV exports are ASCII-compatible; the
        # fixed utf-8 encoding avoids depending on the platform default)
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # "Data comprises raw, unprocessed facts that need context to become
        #  useful, while information is data that has been processed, organized,
        #  and interpreted to add meaning and value."

        # The header ends at the separator line "INTENSITY" (no tab); the
        # numeric matrix follows it. This supports headers of any length.
        sep_idx = next(
            (i for i, line in enumerate(lines) if line.strip() == "INTENSITY"),
            None,
        )
        if sep_idx is None:
            raise ValueError(f"{file_path}: no 'INTENSITY' separator line found")
        info = lines[:sep_idx]
        data = [
            list(map(int, line.split())) for line in lines[sep_idx + 1:] if line.strip()
        ]

        # PDA data
        data = np.array(data)

        # PDA information
        info_dict = {}
        for item in info:
            item = item.replace("\n", "").replace("\r", "").replace(",", ".")
            key, value = item.split("\t", 1)
            info_dict[key] = value

        # Chromatogram name
        name = Path(file_path).stem   # filename without extension
        name = name.removesuffix(" (PDA)")

        # Instanciate object
        return cls(
            NAME=name,
            INFO=info_dict,
            PDA_DATA=data,
        )

    def add_fl(self, file_path, channel):
        """This method add the data obtained in a fluorescence detector, which
        is stored in csv file (time vs intensity)

        params:
        file_path(str): path of the csv file contianign data point.
        channel(str): channel name to store in FL attribute. In ChromNAV, FL
        data points are exported by single channels."""

        # Read csv file
        df = pd.read_csv(file_path, sep=";", decimal=",")
        # Same schema as create_from_fl: DataFrame with "Time" and "Intensity".
        # `channel` is kept as a label in df.attrs (not as a column name).
        df = df.rename(columns={"min": "Time"})[["Time", "Intensity"]]
        df.attrs["channel"] = channel
        self.FL_DATA = df

    # def add_PDA()  (DEVELOP THIS METHOD)
