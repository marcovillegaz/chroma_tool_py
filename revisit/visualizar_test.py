import tkinter as tk

from utils import extract

from classes.chroma_visualizer import ChromaVisualizer
from classes.chromatogram import Chromatogram


file_path = r"GWR_project\TEST__13102023 ACTN_test_012 (PDA).txt"

# Open PDA data and set as attribute
chroma1 = Chromatogram.create_from_pda(file_path=file_path)


root = tk.Tk()
app = ChromaVisualizer(root, chroma1)
root.mainloop()
