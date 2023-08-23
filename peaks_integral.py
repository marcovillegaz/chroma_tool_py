import numpy as np
import math as m
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid


def func(x):
    y = 1 + np.sin(2 * np.pi * x) + 2 * np.exp(x) + np.cos(0.5 * np.pi * x)
    return y


# INPUTS

# Generating data
x = np.arange(0, 50, 1)
y = func(x)

# Index of integration limits. Each row is an interval.
limits = np.array([[2, 12], [15, 25], [27, 46]])

print(type(limits.shape))
print(limits.shape[1])
print(limits[1, :])
print(len(y))

areas = np.zeros([limits.shape[0], 1])  # Preallocation

for i in range(0, limits.shape[0]):
    a = limits[i, 0]
    b = limits[i, 1]
    y_i = y[a:b]
    x_i = x[a:b]
    areas[i] = trapezoid(y, x)

    print(areas)


# Plotting results
fix, ax = plt.subplots()
ax.plot(x, y)
plt.show()
