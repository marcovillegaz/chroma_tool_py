import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Analyte:
    """In liquid chromatography using diode array detectors, the data obtained
    is a surface of the intensition depending on time and wavelength. Each
    analyte is identified by it spectrum (wavelength vs intensity)."""

    all = []

    def __init__(self, name, residence_time=None):
        """
        residence_time: time where the peak that represent the analyte appear.
        wavelength: wavelength (nm) where the analye is quantified in the PDA surface
        """
        # Run validation to reacive arguments
        assert type(name) is str, f"{name} must be a string!"

        # Assign to self object (instance attributes)
        self.name = name
        self.residence_time = residence_time  # (min)

        # Action to execute
        Analyte.all.append(self)

    # Return an unambiguous string representation of the object
    def __repr__(self) -> str:
        return f"Analyte('{self.name}',{self.residence_time})"

    def extract_spectrum(self, PDA_data):
        """This method employ a residence time to extract espectrom of PDA data"""

        # plot spectrum
        wavelength_array = np.linspace(
            PDA_data["Wavelength"][0],
            PDA_data["Wavelength"][1],
            PDA_data["Intensity"].shape[1],
        )
        intensity = PDA_data["Intensity"]

        spectrum = intensity[self.residence_time, :]

        fig, ax = plt.subplots(figsize=(7, 5))
        ax.plot(wavelength_array, spectrum)
        plt.xlim(min(wavelength_array), max(wavelength_array))
        plt.show()
