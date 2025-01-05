import numpy as np

# Define arrays
X = np.array([10, 20, 30, 40, 50])  # Rows (5 elements)
Y = np.array([1, 2, 3, 4])  # Columns (4 elements)
Z = np.array(
    [
        [11, 12, 13, 14],
        [21, 22, 23, 24],
        [31, 32, 33, 34],
        [41, 42, 43, 44],
        [51, 52, 53, 54],
    ]
)  # 5x4 matrix

# Define clipping limits
x_min, x_max = 15, 45
y_min, y_max = 2, 3

# Create masks for X and Y
x_mask = (X >= x_min) & (X <= x_max)  # Rows to keep
y_mask = (Y >= y_min) & (Y <= y_max)  # Columns to keep

# Apply masks to clip X, Y, and Z
X_clipped = X[x_mask]
Y_clipped = Y[y_mask]
Z_clipped = Z[x_mask, :][:, y_mask]


# Print shapes
print("Original shape X:", np.shape(X))
print("Original shapeY:", np.shape(Y))
print("Original shape Z:\n", np.shape(Z))

print("\nClipped shape X:", np.shape(X_clipped))
print("Clipped shape Y:", np.shape(Y_clipped))
print("Clipped shape Z:\n", np.shape(Z_clipped))

# Print results
print("Original X:", X)
print("Original Y:", Y)
print("Original Z:\n", Z)

print("\nClipped X:", X_clipped)
print("Clipped Y:", Y_clipped)
print("Clipped Z:\n", Z_clipped)
