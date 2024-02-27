import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


def cosmos_screening(file_path, save_path="None"):
    """DESCRIPTION"""
    df = pd.read_csv(file_path, sep=";", decimal=",")  # Read CSV file into a DataFrame
    df.set_index("CECs", inplace=True)  # Set the "indexes" column as the index
    print(df)  # Display the DataFrame

    # Transpose the DataFrame to have compounds as columns
    df_transposed = df.transpose()

    # Plotting
    ax = df_transposed.plot(
        kind="bar", figsize=(15, 6), rot=0, colormap="tab10", width=0.8
    )

    # Set axis labels and title
    ax.set_xlabel("Polymers")
    ax.set_ylabel(r"$Ln(\gamma)$")
    ax.set_title("Grouped Bar Plot of $Ln(\gamma)$ for Each Polymer")
    ax.set_ylim([-15, 15])
    ax.grid(linewidth=0.5)

    # Annotate each bar with its numeric value
    for container in ax.containers:
        ax.bar_label(
            container,
            fmt="%.2f",
            label_type="edge",
            fontsize=8,
            color="black",
            # weight="bold",
            rotation=90,
        )

    # Find the polymer with the maximum value
    max_polymer = df_transposed.max().idxmax()
    max_value = df_transposed[max_polymer].max()

    # Manually add text annotation for the highest bar
    ax.annotate(
        f"{max_value:.2f}",
        xy=(3.72, 13),
        xytext=(5, 5),
        textcoords="offset points",
        ha="center",
        va="center",
        color="red",
        fontsize=8,
        weight="bold",
        rotation="vertical",
    )

    # Show or save image
    if save_path == "None":
        plt.show()
    else:
        save_path = os.path.join(save_path, "COSMOS_bar_plot.png")
        print("\nSaving in plot in: ", save_path)
        plt.savefig(save_path, dpi=600)

    # plt.close("all")


# Replace 'your_file.csv' with the actual path to your CSV file
file_path = r"path/to/data"

cosmos_screening(
    file_path, save_path=r"path/to/data"
)
