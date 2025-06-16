import numpy as np
from skimage import measure
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Needed for 3D plotting
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def contour_plot(
    f, x_range=(-5, 5), y_range=(-5, 5), resolution=100, levels=20, cmap="viridis"
):
    """
    Plots contour lines of a function f(x, y).

    Parameters:
        f (function): A function of two variables, e.g., lambda x, y: np.sin(x)*np.cos(y)
        x_range (tuple): Range of x values
        y_range (tuple): Range of y values
        resolution (int): Grid resolution
        levels (int): Number of contour levels
        cmap (str): Color map for lines
    """
    x = np.linspace(*x_range, resolution)
    y = np.linspace(*y_range, resolution)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)

    plt.figure(figsize=(8, 6))
    contours = plt.contour(X, Y, Z, levels=levels, cmap=cmap)
    plt.clabel(contours, inline=True, fontsize=8)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Contour Plot of f(x, y)")
    plt.grid(True)
    plt.show()


def surface_plot(f, x_range=(-5, 5), y_range=(-5, 5), resolution=100, cmap="viridis"):
    """
    Plots a 3D surface of a function f(x, y).

    Parameters:
        f (function): A function of two variables, e.g., lambda x, y: np.sin(x)*np.cos(y)
        x_range (tuple): Range of x values
        y_range (tuple): Range of y values
        resolution (int): Grid resolution
        cmap (str): Color map for surface
    """
    x = np.linspace(*x_range, resolution)
    y = np.linspace(*y_range, resolution)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")
    surface = ax.plot_surface(X, Y, Z, cmap=cmap, edgecolor="none")
    fig.colorbar(surface, ax=ax, shrink=0.5, aspect=10, label="f(x, y)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("f(x, y)")
    ax.set_title("Surface Plot of f(x, y)")
    plt.show()


# Example fucntion
func = lambda x, y: 10 * x**2 + y**2

# contour_plot
contour_plot(
    func,
    x_range=(-5, 5),
    y_range=(-5, 5),
    levels=[-2, -1, 0, 1, 4, 16],
)

# surface_plot
surface_plot(
    func,
    x_range=(-5, 5),
    y_range=(-5, 5),
)
