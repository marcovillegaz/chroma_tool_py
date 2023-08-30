import pybeads as be
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["figure.facecolor"] = "w"


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# The provided chromatograms have a 'well-behaved' background feature that the both ends
# smoothly approach to zero.

# Eight chromatograms with different background levels look like this
data = np.genfromtxt("chromatograms_and_noise.csv", skip_header=4, delimiter=",")
fig, axes = plt.subplots(1, 2, figsize=(15, 4))
for i in range(8):
    axes[0].plot(data[:, i], label=i)  # first plot
    axes[1].plot(data[:, i], ".-", label=i)  # second plot

axes[1].set_ylim(0, 100)
axes[1].set_xlim(1500, 3500)
axes[1].legend(ncol=4)
plt.show()
