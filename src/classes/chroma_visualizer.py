import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from utils import info, extract


class ChromaVisualizer:
    """ChromaVisualize class is used to plot a chromatogram instance
    in real time."""

    def __init__(self, master, cls):
        """
        args:
            master: root window of the Tkinter application.
            chroma: instance of Chromatogram class.
        """
        self.master = master
        self.master.title("Chromatogram Viewer")

        # Load the data
        self.time = info.time(cls.INFO)
        self.intensity = extract.by_wavelength(cls, 260)

        # Create a figure and axis for the plot
        self.fig, self.ax = plt.subplots()
        self.ax.plot(self.time, self.intensity, label="Chromatogram")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Intensity")
        self.ax.set_title("Chromatogram")
        self.ax.legend()

        # Create a canvas and pack it into the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create control frame
        self.control_frame = ttk.Frame(master)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Create limit entry boxes
        self.start_label = ttk.Label(self.control_frame, text="Start Time:")
        self.start_label.pack(side=tk.LEFT)
        self.start_entry = ttk.Entry(self.control_frame, width=10)
        self.start_entry.pack(side=tk.LEFT)

        self.end_label = ttk.Label(self.control_frame, text="End Time:")
        self.end_label.pack(side=tk.LEFT)
        self.end_entry = ttk.Entry(self.control_frame, width=10)
        self.end_entry.pack(side=tk.LEFT)

        # Create update button
        self.update_button = ttk.Button(
            self.control_frame, text="Update", command=self.update_plot
        )
        self.update_button.pack(side=tk.LEFT)

    def update_plot(self):
        start_time = float(self.start_entry.get())
        end_time = float(self.end_entry.get())

        # Filter data based on the provided time limits
        mask = (self.time >= start_time) & (self.time <= end_time)
        filtered_time = self.time[mask]
        filtered_intensity = self.intensity[mask]

        # Clear the previous plot and plot the new data
        self.ax.clear()
        self.ax.plot(filtered_time, filtered_intensity, label="Chromatogram")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Intensity")
        self.ax.set_title("Chromatogram")
        self.ax.legend()

        # Draw the updated plot
        self.canvas.draw()
