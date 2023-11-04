from pathlib import Path
from tkinter import PhotoImage
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

import matplotlib.pyplot as plt
import json
import utils

class PathFinder(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES)

        # assets
        self.images = []
        
        # A. make column
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)

        # A.1. column 1
        col1 = ttk.Frame(self, padding=10)
        col1.config(borderwidth=10, relief="groove")
        col1.grid(row=0, column=0, sticky='nsew')
        col1.grid_columnconfigure(0, weight=1)
        col1.grid_rowconfigure(0, weight=1)
        col1.grid_rowconfigure(1, weight=1)
        
        # A.2 column 2
        col2 = ttk.Frame(self, padding=10)
        col2.grid(row=0, column=1, sticky='nsew')
        col2.grid_columnconfigure(0, weight=1)
        col2.grid_rowconfigure(0, weight=2)
        col2.grid_rowconfigure(1, weight=1)

def app_config(app : ttk.Frame|ttk.Window):
    app.iconbitmap("./assets/icon.ico")
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (1000/2))
    y_cordinate = int((screen_height/2) - (750/2))
    app.geometry("{}x{}+{}+{}".format(1000, 750, x_cordinate, y_cordinate))
    app.minsize(1000,750)
    return app

if __name__ == "__main__":
    app = ttk.Window("Path Finder",
                     "cosmo")
    app = app_config(app)
    PathFinder(app)
    app.mainloop()