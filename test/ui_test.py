import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from matplotlib.widgets import Cursor


class PlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Plot Axis Limits")

        # Create a matplotlib figure and axis
        self.figure, self.ax = plt.subplots()
        self.ax.plot([0, 1, 2, 3], [10, 20, 25, 30])

        # Create a canvas to display the plot in the tkinter window
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Add zooming and panning
        self.canvas.mpl_connect("scroll_event", self.on_scroll)
        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion)

        # Adding a cursor for better interaction
        self.cursor = Cursor(self.ax, useblit=True, color="red", linewidth=1)

        # Create UI elements for changing the axis limits
        self.create_axis_limit_entries()

        # Variables for panning
        self.press = None
        self.cur_xlim = self.ax.get_xlim()
        self.cur_ylim = self.ax.get_ylim()
        self.pan_start = None

    def create_axis_limit_entries(self):
        frame = tk.Frame(self.root)
        frame.pack(side=tk.BOTTOM, fill=tk.X)

        # X-axis limits
        tk.Label(frame, text="X-axis min:").pack(side=tk.LEFT)
        self.xmin_entry = tk.Entry(frame)
        self.xmin_entry.pack(side=tk.LEFT)

        tk.Label(frame, text="X-axis max:").pack(side=tk.LEFT)
        self.xmax_entry = tk.Entry(frame)
        self.xmax_entry.pack(side=tk.LEFT)

        # Y-axis limits
        tk.Label(frame, text="Y-axis min:").pack(side=tk.LEFT)
        self.ymin_entry = tk.Entry(frame)
        self.ymin_entry.pack(side=tk.LEFT)

        tk.Label(frame, text="Y-axis max:").pack(side=tk.LEFT)
        self.ymax_entry = tk.Entry(frame)
        self.ymax_entry.pack(side=tk.LEFT)

        # Update button
        self.update_button = tk.Button(
            frame, text="Update Axis Limits", command=self.update_axis_limits
        )
        self.update_button.pack(side=tk.LEFT)

    def update_axis_limits(self):
        try:
            # Get the axis limits from the user entries
            xmin = float(self.xmin_entry.get())
            xmax = float(self.xmax_entry.get())
            ymin = float(self.ymin_entry.get())
            ymax = float(self.ymax_entry.get())

            # Update the axis limits
            self.ax.set_xlim([xmin, xmax])
            self.ax.set_ylim([ymin, ymax])

            # Redraw the canvas with the new limits
            self.canvas.draw()
        except ValueError:
            print("Please enter valid numbers for the axis limits.")

    def on_scroll(self, event):
        x_min, x_max = self.ax.get_xlim()
        y_min, y_max = self.ax.get_ylim()

        if event.button == "up":
            scale_factor = 1 / 1.5
        elif event.button == "down":
            scale_factor = 1.5
        else:
            scale_factor = 1

        self.ax.set_xlim([x_min * scale_factor, x_max * scale_factor])
        self.ax.set_ylim([y_min * scale_factor, y_max * scale_factor])
        self.canvas.draw()

    def on_press(self, event):
        if event.button == 1:
            self.pan_start = (event.xdata, event.ydata)
            self.cur_xlim = self.ax.get_xlim()
            self.cur_ylim = self.ax.get_ylim()

    def on_motion(self, event):
        if self.pan_start:
            dx = self.pan_start[0] - event.xdata
            dy = self.pan_start[1] - event.ydata
            self.ax.set_xlim([x + dx for x in self.cur_xlim])
            self.ax.set_ylim([y + dy for y in self.cur_ylim])
            self.canvas.draw()

    def on_release(self, event):
        self.pan_start = None


if __name__ == "__main__":
    root = tk.Tk()
    app = PlotApp(root)
    root.mainloop()
