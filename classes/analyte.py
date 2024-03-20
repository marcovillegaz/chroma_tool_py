import numpy as np
import pandas as pd


class Analyte:
    """In liquid chromatography using diode array detectors, the data obtained
    is a surface of the intensition depending on time and wavelength. Each
    analyte is identified by it spectrum (wavelength vs intensity)."""

    all = []

    def __init__(self, name, wavelength, residence_time=None):
        """
        residence_time: time where the peak that represent the analyte appear.
        wavelength: wavelength (nm) where the analye is quantified in the PDA surface
        """
        # Run validation to reacive arguments
        assert type(name) is str, f"{name} must be a string!"
        assert type(residence_time) is float, f"{residence_time} must be a numpy.array!"
        assert type(wavelength) is float, f"{wavelength} must be a numpy.array!"

        # Assign to self object (instance attributes)
        self.name = name
        self.wavelength = wavelength  # (nm)
        self.residence_time = residence_time  # (min)

        # Action to execute
        Analyte.all.append(self)

    # Return an unambiguous string representation of the object
    def __repr__(self) -> str:
        return f"Analyte('{self.name}',{self.residence_time},{self.wavelength})"

    @classmethod
    def indetify_analyte():
        """This method use the PDA_data surface and search for the correpsonding
        spectrum using the residence time as reference. THe residence time should
        be provided by the analist."""
