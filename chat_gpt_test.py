import matplotlib.pyplot as plt
import numpy as np

# Your data
categories = ["BPA", "ACTN", "TCN", "TMP", "CAF", "MeP", "OXY", "OC"]
PDMS = [-8.363, 1.775, -8.29, 4.104, 3.62, -3.423, -2.2503, 1.1227]
PP = [-3.243, 3.688, -4.909, 1.608, 2.016, -0.397, 0.4986, 0.384]
PET = [-1.065, 3.447, -3.112, -0.241, -0.022, 0.461, 0.3697, 0.4642]
PVC = [4.743, 7.828, 0.952, 2.471, 0.912, 4.182, 4.182, 0.1885]
PLA = [-1.598, 121.308, -3.6682, -1.028, -0.9001, -0.2728, -0.1972, -0.052]

# Grouped bar plot
bar_width = 0.15
index = np.arange(len(categories))
opacity = 0.8

fig, ax = plt.subplots()

bar1 = plt.bar(index - 2 * bar_width, PDMS, bar_width, alpha=opacity, label="PDMS")
bar2 = plt.bar(index - bar_width, PP, bar_width, alpha=opacity, label="PP")
bar3 = plt.bar(index, PET, bar_width, alpha=opacity, label="PET")
bar4 = plt.bar(index + bar_width, PVC, bar_width, alpha=opacity, label="PVC")
bar5 = plt.bar(index + 2 * bar_width, PLA, bar_width, alpha=opacity, label="PLA")

# Set y-axis limits
plt.ylim(-15, 15)

# Annotate the bar with a high value in the 'ACTN' category (adjust the index if needed)
high_value_index = categories.index("ACTN")
high_value = ACTN[high_value_index]
plt.annotate(
    f"{high_value}",
    xy=(index[high_value_index], high_value),
    xytext=(0, 3),  # 3 points vertical offset
    textcoords="offset points",
    ha="center",
    va="bottom",
)

# Customize the plot
plt.xlabel("Analyte")
plt.ylabel("Values")
plt.title("Grouped Bar Plot")
plt.xticks(index, categories)
plt.legend()

plt.tight_layout()
plt.show()
