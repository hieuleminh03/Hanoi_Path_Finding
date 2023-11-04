from pathlib import Path
from tkinter import PhotoImage
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

import matplotlib.pyplot as plt
import json
import utils


PATH = Path(__file__).parent/'assets'


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
        col1.grid(row=0, column=0, sticky='nsew')
        col1.grid_columnconfigure(0, weight=1)
        col1.grid_rowconfigure(0, weight=1)
        col1.grid_rowconfigure(1, weight=1)

        # A.1.1. point chooser frame
        point_chooser_frame = ttk.Labelframe(col1,
                                            text="Point Chooser",
                                            borderwidth=5,
                                            relief="groove")
        point_chooser_frame.grid(row=0, column=0, sticky='nsew')
        point_chooser_frame.grid_rowconfigure(0, weight=2)
        point_chooser_frame.grid_rowconfigure(1, weight=1)
        point_chooser_frame.grid_columnconfigure(0, weight=1)
        
        # A.1.1.1. point view frame
        point_view_frame = ttk.Frame(point_chooser_frame)
        point_view_frame.grid(row=0, column=0, sticky='nsew')
        point_view_frame.grid_rowconfigure(0, weight=1)
        point_view_frame.grid_rowconfigure(1, weight=1)
        point_view_frame.grid_columnconfigure(0, weight=1)
        point_view_frame.grid_columnconfigure(1, weight=2)
        
        self.current_start_point = str()
        self.current_end_point = ""
        
        ttk.Label(point_view_frame,
                  text="Start",
                  ).grid(row=0, column=0, padx=(30,0))
        ttk.Label(point_view_frame,
                  text="End",
                  ).grid(row=1, column=0, padx=(30,0))
        start_combobox_up = ttk.Combobox(
            master=point_view_frame,
            values=[],
            state="readonly",
            bootstyle="primary",
            takefocus=False
        )
        # add data to combobox
        with open('data/4.json', 'r') as f:
            self.data = json.load(f)
        start_choices = []
        for item in self.data:
            start_choices.append(item.get('name'))
        start_combobox_up.configure(values=start_choices)
        start_combobox_up.grid(row=0, column=1)
        
        
        end_combobox_up = ttk.Combobox(
            master=point_view_frame,
            values=[],
            state="readonly",
            bootstyle="primary",
            takefocus=False
        )
        end_combobox_up.grid(row=1, column=1)
        
        
        end_combobox_up.bind("<<ComboboxSelected>>", lambda event: utils.change_end_point(end_combobox_up, self.current_end_point))
        start_combobox_up.bind("<<ComboboxSelected>>", lambda event : utils.after_cbbox_selected(start_combobox_up, end_combobox_up, self.current_start_point))
        
        # A.1.1.2. main buttons frame
        main_buttons_frame = ttk.Frame(point_chooser_frame)
        main_buttons_frame.configure()
        main_buttons_frame.grid(row=1, column=0, sticky='nsew')
        main_buttons_frame.grid_rowconfigure(0, weight=1)
        main_buttons_frame.grid_columnconfigure(0, weight=1)
        main_buttons_frame.grid_columnconfigure(1, weight=1)
        
        open_map_button = ttk.Button(master=main_buttons_frame,
                              text="Open Map",
                              bootstyle="dark-outline",
                              takefocus=False,
                              command=lambda: Messagebox.ok(
                                  title="Open Map",
                                  message="Opened Map"
                              ))
        # add event to button
        open_map_button.bind("<Button-1>", lambda event: utils.open_new_map("data/4.json"))
        open_map_button.grid(row=0, column=0, padx=5)
        find_way_button = ttk.Button(master=main_buttons_frame,
                                    text="Find Way",
                                    bootstyle="success-outline",
                                    takefocus=False,
                                    command=lambda: Messagebox.ok(
                                        title="Find Way",
                                        message="Found Way"
                                    ))
        # test event for find way button
        find_way_button.bind("<Button-1>", lambda event: utils.click_find_way(self.data, start_combobox_up))
        find_way_button.grid(row=0, column=1, padx=5)

        # A.1.2. change weight frame
        change_weight_frame = ttk.Labelframe(col1,
                                            text="Change Weight",
                                            padding=10)
        change_weight_frame.grid(row=1, column=0, sticky='nsew')
        change_weight_frame.grid_rowconfigure(0, weight=3)
        change_weight_frame.grid_rowconfigure(1, weight=3)
        change_weight_frame.grid_rowconfigure(2, weight=1)
        change_weight_frame.grid_columnconfigure(0, weight=1)
        
        # A.1.2.1. change weight view frame
        change_weight_view_frame = ttk.Frame(change_weight_frame)
        change_weight_view_frame.grid(row=0, column=0, sticky='nsew')
        change_weight_view_frame.grid_rowconfigure(0, weight=1)
        change_weight_view_frame.grid_rowconfigure(1, weight=1)
        change_weight_view_frame.grid_columnconfigure(0, weight=1)
        change_weight_view_frame.grid_columnconfigure(1, weight=3)
        
        ttk.Label(change_weight_view_frame,
                    text="Start",
                    ).grid(row=0, column=0, padx=(30,0))
        ttk.Label(change_weight_view_frame,
                    text="End",
                    ).grid(row=1, column=0, padx=(30,0))    
        start_combobox_down = ttk.Combobox(
            master=change_weight_view_frame,
            values=["test 1", "test 2", "test 3"],
            state="readonly",
            bootstyle="primary"
        )
        start_combobox_down.grid(row=0, column=1)
        end_combobox_down = ttk.Combobox(
            master=change_weight_view_frame,
            values=["test 1", "test 2", "test 3"],
            state="readonly",
            bootstyle="primary"
        )
        end_combobox_down.grid(row=1, column=1)
        
        # A.1.2.2. change weight buttons frame
        change_weight_buttons_frame = ttk.Frame(change_weight_frame)
        change_weight_buttons_frame.grid(row=1, column=0, sticky='nsew')
        change_weight_buttons_frame.grid_rowconfigure(0, weight=1)
        change_weight_buttons_frame.grid_columnconfigure(0, weight=1)
        change_weight_buttons_frame.grid_columnconfigure(1, weight=2)
        change_weight_buttons_frame.grid_columnconfigure(2, weight=1)
        
        ttk.Label(change_weight_buttons_frame,
                    text="Weight",
                    ).grid(row=0, column=0, padx=(30,0))
        weight_input = ttk.Entry(change_weight_buttons_frame,
                                 bootstyle="dark")
        weight_input.grid(row=0, column=1)
        set_weight_button = ttk.Button(change_weight_buttons_frame,
                                        text="Set Weight",
                                        bootstyle="primary-outline",
                                        command=lambda: Messagebox.ok(
                                            title="Set Weight",
                                            message="Set Weight"
                                        ))
        set_weight_button.grid(row=0, column=2)
        
        
        # A.2 column 2
        col2 = ttk.Frame(self, padding=10)
        col2.grid(row=0, column=1, sticky='nsew')
        col2.grid_columnconfigure(0, weight=1)
        col2.grid_rowconfigure(0, weight=2)
        col2.grid_rowconfigure(1, weight=1)
        
        # A.2.1 map visual frame
        map_frame = ttk.Labelframe(col2,
                                   text="Map",
                                   padding=10)
        map_frame.grid(row=0, column=0, sticky='nsew')
        
        
        # A.2.2 noti frame
        noti_frame = ttk.Labelframe(col2,
                                    text="Notification",
                                    padding=10)
        noti_frame.grid(row=1, column=0, sticky='nsew')
    
        
def app_config(app : ttk.Frame|ttk.Window):
    app.minsize(1000,500)
    app.iconbitmap("./assets/icon.ico")
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (1000/2))
    y_cordinate = int((screen_height/2) - (500/2))
    app.geometry("{}x{}+{}+{}".format(1000, 500, x_cordinate, y_cordinate))
    return app

if __name__ == "__main__":
    app = ttk.Window("Path Finder",
                     "cosmo")
    app = app_config(app)
    PathFinder(app)
    app.mainloop()
