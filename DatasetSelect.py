import tkinter as tk
from tkinter import filedialog

def open_file_dialog():
    # Create a new Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open the file dialog and allow the user to select a file
    file_path = filedialog.askopenfilename()
    root.destroy()  # Destroy the root window after file selection

    if file_path:
        print(f"Selected file: {file_path}")
        return file_path
    else:
        print("No file selected.")
        return None


