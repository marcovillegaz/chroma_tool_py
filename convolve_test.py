# Importing required libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Creating a series of data of in range of 1-50.
x = np.linspace(1, 3000, 2000)


# Creating a Function.
def normal_dist(x, mean, sd):
    prob_density = (np.pi * sd) * np.exp(-0.5 * ((x - mean) / sd) ** 2)
    return prob_density


# Calculate mean and Standard deviation.
mean = np.mean(x)
sd = np.std(x)

# Apply function to the data.
peak1 = normal_dist(x, 360, 36)
peak2 = normal_dist(x, 450, 11)

caca = signal.convolve(peak1, peak2, mode="same") / sum(peak2)
# Plotting the Results
plt.plot(x, peak1, color="red")
plt.plot(x, peak2, color="blue")
plt.plot(x, caca, color="green")
plt.xlabel("Data points")
plt.ylabel("Probability Density")
plt.show()
