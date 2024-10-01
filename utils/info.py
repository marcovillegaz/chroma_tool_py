"""This are function that are applied on the information dictionary of
the Chromatogram class"""

import numpy as np


def time(CHROMA_INFO):
    """Create the time array that would be useful for data processing

    Args:
        CHROMA_INFO (dict): Information of the chromatogram

    Return:
        time_array (numpy.array): vector of time of the chromatogram
    """
    # Extract and convert the relevant values
    start_time = float(CHROMA_INFO["START_TIME"].replace("min", ""))
    end_time = float(CHROMA_INFO["END_TIME"].replace("min", ""))
    time_npoints = int(CHROMA_INFO["TIME_NPOINTS"])

    # Create a NumPy array using np.linspace
    time_array = np.linspace(start_time, end_time, time_npoints)

    return time_array


def wavelenth(CHROMA_INFO):
    """Create the wavelength array that would be useful for data processing

    Args:
        CHROMA_INFO (dict): Information of the chromatogram

    Return:
        time_array (numpy.array): vector of time of the chromatogram
    """

    # Extract and convert the relevant values
    start_wl = float(CHROMA_INFO["START_WL"].replace("nm", ""))
    end_wl = float(CHROMA_INFO["END_WL"].replace("nm", ""))
    wl_npoints = int(CHROMA_INFO["WL_NPOINTS"])

    # Create a NumPy array using np.linspace
    wl_array = np.linspace(start_wl, end_wl, wl_npoints)

    return wl_array
