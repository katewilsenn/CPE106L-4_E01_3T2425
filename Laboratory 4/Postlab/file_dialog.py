import tkinter as tk
from tkinter import filedialog

def choose_file():
    """Open file dialog to choose a file."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt")])
    return file_path
