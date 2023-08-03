import pandas as pd
import matplotlib.pyplot as plt


def central_diff(x, y):
    # This function computes the central finite difference for multiple experimental
    # points (x_i,y_i) defined as array.
    # Inputs:
    #   x: array of x values (n elements)
    #   y: array of y values (n elements)}
    # Output:
    #   x_diff: array of x values (n-2 elements)
    #   y_diff: array of first derivative (n-2 elements)
    delta_x = x[2:] - x[:-2]
    delta_y = y[2:] - y[:-2]
    y_diff = delta_y / delta_x
    x_diff = x[1 : len(x) - 1]

    return x_diff, y_diff


# Reading .csv file with chromatogram data
df1 = pd.read_csv(r"chrom-test1.csv", sep=";", decimal=",")
df = pd.read_csv(r"chrom-test1.csv", sep=";", decimal=",")
df["Int SMA30"] = df["Intensity"].rolling(15).mean()
print("=" * 50 + "\n", df)
df.dropna(inplace=True)
print("=" * 50 + "\n", df)

# df[["Int SMA30", "Intensity"]].plot(figsize=(16, 8))

interval = [5, 8]

# Data frame to numpy array
x = df["min"].to_numpy()
y = df["Int SMA30"].to_numpy()

print("---" * 8)

x_diff, y_diff = central_diff(x, y)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x_diff, y_diff, label="first derivative")
# ax.plot(x_2diff, y_2diff, label="second derivative")
ax.plot(x, y, label="Chromatogram")
ax.vlines([5, 8], -1e5, 1e5, colors="g", linestyles="dashed")
ax.legend()
plt.show()
