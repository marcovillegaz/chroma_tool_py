"""Utility function for plotting any intermediate or finish result"""

import matplotlib.pyplot as plt


def plot_results(intensity, time, peaks_data, intervals=None):
    """This function plot the resuls of this script like: intervals, peaks,
    limits,areas"""

    print("Plotting results".center(50, "="))

    fig, ax = plt.subplots(figsize=(14, 7))

    ax.plot(time, intensity)

    # Get and set limits
    ax.set_xlim(xmin=time[0], xmax=time[-1])
    ax.set_ylabel("Intensity")
    ax.set_xlabel("Time [min]")

    """ # Plot intervals
    # if intervals != "None":
        for i, interval in enumerate(intervals):
            plt.axvline(x=interval[0], color="tab:orange", linestyle="dotted")
            plt.axvline(x=interval[1], color="tab:orange", linestyle="dotted")

            # Add text to interval
            plt.text(
                interval[0],
                ymax * 0.5,
                "user interval " + str(i + 1),
                ha="center",
                va="center",
                rotation="vertical",
                backgroundcolor="white",
            ) """

    # Plot peaks
    x_peak = peaks_data["residence_time"]
    y_peak = peaks_data["height"]
    plt.scatter(x_peak, y_peak, s=20, marker="x", color="red")

    # Add peak identification number
    for i in range(0, len(x_peak)):
        plt.text(
            x_peak.iloc[i],
            y_peak.iloc[i] + 4000,
            str(i + 1),
            ha="center",
            va="center",
            rotation="horizontal",
        )

    """ # Plot integration limits
    limits_idx = peaks_data.iloc[:, 2].to_numpy()
    limits_val = peaks_data.iloc[:, 3].to_numpy()

    for i in range(0, len(limits_idx)):
        x_ab = limits_idx[i]
        y_ab = limits_val[i]
        plt.scatter(x_ab, y_ab, s=20, marker="x", color="green") """

    """ # Plot integrated areas
    for limit in limits_idx:
        a = limit[0]
        b = limit[1]

        y = chroma_data.iloc[a : b + 1, 0]
        iy = y.values
        ix = list(range(a, b + 1))

        verts = [(a, 0), *zip(ix, iy), (b, 0)]
        poly = Polygon(verts, facecolor="0.9", edgecolor="0.5")
        ax.add_patch(poly) """

    ax.grid()
    ax.legend()
    plt.show()
