import pandas as pd
import matplotlib.pyplot as plt

# Reading .csv file with chromatogram data
df1 = pd.read_csv(r"chrom-test1.csv", sep=";", decimal=",")
df = pd.read_csv(r"chrom-test1.csv", sep=";", decimal=",")
df["Int SMA30"] = df["Intensity"].rolling(15).mean()
print("=" * 50 + "\n", df)
df.dropna(inplace=True)
print("=" * 50 + "\n", df)

df[["Int SMA30", "Intensity"]].plot(figsize=(16, 8))


# Data frame to numpy array
x = df["min"].to_numpy()
y = df["Int SMA30"].to_numpy()
print("---" * 8)
# stepforward finite difference
delta_x = x[1:] - x[:-1]  # forward step
delta_y = y[1:] - y[:-1]

diff = delta_y / delta_x

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x[1:], diff, label="260 nm")
ax.plot(x, y)
plt.show()

print(diff)
print(len(diff))
print(len(x))
