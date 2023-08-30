import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import pybeads as be


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1 :] / n


# PyBEADS parameters
# try changing fc and lam0-2, amp if these dont' fit your data
fc = 0.006
d = 1
r = 6
amp = 0.8
lam0 = 0.5 * amp
lam1 = 5 * amp
lam2 = 4 * amp
Nit = 15
pen = "L1_v2"

signal_est, bg_est, cost = be.beads(y, d, fc, r, Nit, lam0, lam1, lam2, pen, conv=None)
