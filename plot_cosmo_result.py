"""This script create a grouped bar plot for the result obtained ina COSMO-RS
screening of the best hydrofobic DES to extract PCB77"""

import matplotlib.pyplot as plt
import numpy as np

species = (
    "Men:Lid (1:2)",
    "Thy:Dec (1:1)",
    "Men:Dec (1:1)",
)
activity_coeff = {
    r"$\gamma$ PCB77": (-0.0864, 0.2965, 0.7251),
    r"$\gamma$ water": (2.8803, 4.6327, 2.3077),
}

x = np.arange(len(species))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout="constrained")

for attribute, measurement in activity_coeff.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel("Activity coefficient")
ax.set_title("HDES selected from screening")
ax.set_xticks(x + width, species)
ax.legend(loc="upper right", ncols=1)
ax.set_ylim(-0.5, 5)
plt.axhline(y=0, linewidth=1, color="k")
plt.show()
