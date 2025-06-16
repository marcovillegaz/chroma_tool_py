"""This are function to extract data from PDA_DATA array

In PDA detectors de Intensity id function of time and wavelength
    Itensity = f(time,wavelength)
"""

import numpy as np
import pandas as pd

from src.utils import info


# maybe put this function in other place
def find_neighbors(array, value):
    """This function search the range where a value is in array and
    return the index of that values. For example the neighbors of 5 in
    the list [2,4,6,8] have the indexes [1,2]"""

    idx = []
    for i in range(len(array) - 1):
        if array[i] <= value <= array[i + 1]:
            idx.append(i)
            idx.append(i + 1)

    return idx


def interpolate_v(v1, v2, x1, x2, xi):
    """Interpoalte between two vector usign the relative distance

    Args:
        v1,v2 (numpy.array): vector where to interpolate
        x1,x2 (float): independent variabke
        xi (float): value to interpolate
    Return:
        vi (numpy.array): interpolated vector as function of xi
    """

    # Perform linear interpolation
    t = (xi - x1) / (x2 - x1)
    vi = (1 - t) * v1 + t * v2

    return vi


def by_wavelength(cls, wl):
    """This function extract the vector intensity as function of time at given
    wavelengths

    args:
        cls (object): instance of Chromatogram class
        wl (int): wavelength to select data

    return:
        intensity (numpy.array): intensity at correspongin wavelength (wl)"""

    # Rearrangemnet of data
    data = cls.PDA_DATA
    wl_array = info.wavelenth(cls.INFO)

    # Find index position of the setted wavelength
    if wl in wl_array:
        # print(f"{wl}nm is in wavelength array")

        # Extract the correpsonding array by index
        index = np.where(wl_array == wl)[0]
        intensity = data[:, index].flatten()
    else:
        # print(f"{wl}nm is not in wavelength array")

        # indenify neighbors of wl
        idx = find_neighbors(wl_array, wl)
        # interpolate betwene vector
        intensity = interpolate_v(
            v1=data[:, idx[0]].flatten(),
            v2=data[:, idx[1]].flatten(),
            x1=wl_array[idx[0]],
            x2=wl_array[idx[1]],
            xi=wl,
        )

    return intensity


def by_time(cls, time):
    """This function extract the vector intensity as function of wavelength at
    given time"

    Args:
        cls (object): instance of Chromatogram class
        time (float): given time
    Return:
        intensity (numpy.array): intensity at corresponging time"""

    # Rearrangemnet of data
    data = cls.PDA_DATA
    time_array = info.time(cls.INFO)

    # Find index position of the setted time
    if time in time_array:
        # Extract the correpsonding array by index
        index = np.where(time_array == time)[0]
        intensity = data[:, index].flatten()
    else:
        # indenify neighbors of time
        idx = find_neighbors(time_array, time)
        # interpolate betwene vector
        intensity = interpolate_v(
            v1=data[idx[0], :].flatten(),
            v2=data[idx[1], :].flatten(),
            x1=time_array[idx[0]],
            x2=time_array[idx[1]],
            xi=time,
        )

    return intensity


def clip_pda(
    x,
    y,
    z,
    x_lim,
    y_lim,
):
    """Clip your data based on your axis limits.
    This helps not plot inacessary information

    Args:
        x (np.array): time array
        y (np.array): wavelength array
        z (np.array): intensity with shape (len(x),len(y))
        x_lim (tuple): min and max of x
        y_lim (tuple): min and max of y

    Returns:
        x_clipped, y_clipped, z_clipped: clipped version of the same information
    """

    # Clip the time and wavelength arrays
    x_mask = (x >= x_lim[0]) & (x <= x_lim[1])
    y_mask = (y >= y_lim[0]) & (y <= y_lim[1])

    # Apply masks to clip X, Y, and Z
    x_clipped = x[x_mask]
    y_clipped = y[y_mask]
    z_clipped = z[x_mask, :][:, y_mask]

    return x_clipped, y_clipped, z_clipped
