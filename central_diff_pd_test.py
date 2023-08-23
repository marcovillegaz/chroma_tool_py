import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def differentiate_dataframe(df, xname, yname, order=2):
    def central_diff(x, y):  # Compute central difference derivative
        # Preallocation
        y_diff = np.empty([len(x)])
        y_diff[:] = np.nan
        # Computing central finite difference
        delta_x = x[2:] - x[:-2]
        delta_y = y[2:] - y[:-2]
        y_diff[1 : len(x) - 1] = delta_y / delta_x  # Result definition
        return y_diff

    order_names = ["First diff", "Second diff", "Third diff"]
    col_names = [yname] + order_names

    for i in range(order):
        # DataFrame to numpy array
        x = df[xname].to_numpy()
        y = df[col_names[i]].to_numpy()

        df[col_names[i + 1]] = central_diff(x, y)
        df.dropna(inplace=True)

    return df


# Reading .csv file with chromatogram data
df1 = pd.read_csv(r"chrom-test1.csv", sep=";", decimal=",")
df = pd.read_csv(r"chrom-test1.csv", sep=";", decimal=",")
df["Int SMA30"] = df["Intensity"].rolling(15).mean()
print("=" * 50 + "\n", df)
df.dropna(inplace=True)
print("=" * 50 + "\n", df)


df = differentiate_dataframe(df, "min", "Int SMA30", order=2)

print("=" * 50 + "\n", df)

# Find the peak in range
diff2_sorted = df[df["min"].between(0, 8)].sort_values("Second diff")
chroma_sorted = df[df["min"].between(0, 8)].sort_values("Int SMA30")
print(diff2_sorted.head())

print(chroma_sorted.tail())


fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df["min"], df["Int SMA30"], label="Chromatogram")
ax.plot(df["min"], df["First diff"], label="first derivative")
ax.plot(diff2_sorted.iloc[0:5, 0], diff2_sorted.iloc[0:5, 2], marker=".")
# ax.plot(chroma_sorted.iloc[-1, 0], chroma_sorted.iloc[-1, 2], marker=".")
# ax.vlines(new_df.iloc[0, 0], -1e5, 1e5, colors="g", linestyles="dashed")
ax.legend()
plt.show()
