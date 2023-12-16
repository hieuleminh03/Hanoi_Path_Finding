from pathlib import Path
from typing import Any
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import tkinter as tk
from tkinter import filedialog
import time
import scipy as sp

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import json
import algorithms

map_data : dict = None

class PathFinder(ttk.Frame):
    
    
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES)

        self.current_find_path_start_point = None
        self.current_find_path_end_point = None
        self.current_weight_start_point = None
        self.current_weight_end_point = None
        self.current_algorithm = None

        self.json_file_path = None

        # assets
        self.images = []

        # A. make column
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1000)

        # A.1. column 1
        col1 = ttk.Frame(self, padding=10)
        col1.grid(row=0, column=0, sticky='ns')
        col1.grid_columnconfigure(0, weight=1)
        col1.grid_rowconfigure(0, weight=3)
        col1.grid_rowconfigure(1, weight=1)
        col1.grid_rowconfigure(2, weight=10)

        # A.1.1. point chooser frame
        point_chooser_frame = ttk.Labelframe(col1,
                                             text="Point Chooser",
                                             borderwidth=5,
                                             relief="groove",
                                             padding=20)
        point_chooser_frame.grid(row=0, column=0, sticky='snew')
        point_chooser_frame.grid_rowconfigure(0, weight=1)
        point_chooser_frame.grid_rowconfigure(1, weight=1)
        point_chooser_frame.grid_columnconfigure(0, weight=1)

        # A.1.1.1. point view frame
        point_view_frame = ttk.Frame(point_chooser_frame)
        point_view_frame.grid(row=0, column=0, sticky='sew')
        point_view_frame.grid_rowconfigure(0, weight=1)
        point_view_frame.grid_rowconfigure(1, weight=1)
        point_view_frame.grid_columnconfigure(0, weight=1)
        point_view_frame.grid_columnconfigure(1, weight=2)

        self.current_start_point = str()
        self.current_end_point = ""

        ttk.Label(point_view_frame,
                  text="Start",
                  ).grid(row=0, column=0, padx=(30, 0), pady=(0, 40))
        ttk.Label(point_view_frame,
                  text="End",
                  ).grid(row=1, column=0, padx=(30, 0), pady=(0, 40))
        self.start_combobox_up = ttk.Combobox(
            master=point_view_frame,
            values=[],
            state="readonly",
            bootstyle="primary",
            takefocus=False
        )
        self.start_combobox_up.grid(row=0, column=1, pady=(0, 40))

        self.end_combobox_up = ttk.Combobox(
            master=point_view_frame,
            values=[],
            state="readonly",
            bootstyle="primary",
            takefocus=False
        )
        self.end_combobox_up.grid(row=1, column=1, pady=(0, 40))

        self.start_combobox_up.bind(
            "<<ComboboxSelected>>", lambda event: self.change_chooser_start_point(self.start_combobox_up))
        self.end_combobox_up.bind(
            "<<ComboboxSelected>>", lambda event: self.change_chooser_end_point(self.end_combobox_up))

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
                                     command=lambda: self.change_map()
                                     )
        open_map_button.grid(row=0, column=0, padx=5)
        find_way_button = ttk.Button(master=main_buttons_frame,
                                     text="Find Way",
                                     bootstyle="success-outline",
                                     takefocus=False
                                     )
        find_way_button.bind("<Button-1>", lambda event: self.find_way())
        find_way_button.grid(row=0, column=1, padx=5)

        # A.1.2. change weight frame
        change_weight_frame = ttk.Labelframe(col1,
                                             text="Change Weight",
                                             padding=10)
        change_weight_frame.grid(row=2, column=0, sticky='nsew')
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
                  ).grid(row=0, column=0, padx=(30, 0))
        ttk.Label(change_weight_view_frame,
                  text="End",
                  ).grid(row=1, column=0, padx=(30, 0))
        self.start_combobox_down = ttk.Combobox(
            master=change_weight_view_frame,
            values=[],
            state="readonly",
            bootstyle="primary"
        )
        self.start_combobox_down.grid(row=0, column=1)
        self.end_combobox_down = ttk.Combobox(
            master=change_weight_view_frame,
            values=[],
            state="readonly",
            bootstyle="primary"
        )
        self.end_combobox_down.grid(row=1, column=1)

        self.start_combobox_down.bind(
            "<<ComboboxSelected>>", lambda event: self.change_weight_start_point(self.start_combobox_down))
        self.end_combobox_down.bind(
            "<<ComboboxSelected>>", lambda event: self.change_weight_end_point(self.end_combobox_down))

        # A.1.2.2. change weight buttons frame
        change_weight_buttons_frame = ttk.Frame(change_weight_frame)
        change_weight_buttons_frame.grid(row=1, column=0, sticky='nsew')
        change_weight_buttons_frame.grid_rowconfigure(0, weight=1)
        change_weight_buttons_frame.grid_columnconfigure(0, weight=1)
        change_weight_buttons_frame.grid_columnconfigure(1, weight=2)
        change_weight_buttons_frame.grid_columnconfigure(2, weight=1)

        ttk.Label(change_weight_buttons_frame,
                  text="Weight",
                  ).grid(row=0, column=0, padx=(30, 10))
        weight_input = ttk.Entry(change_weight_buttons_frame,
                                 bootstyle="dark")
        weight_input.grid(row=0, column=1, sticky='ew', padx=(0, 10))
        set_weight_button = ttk.Button(change_weight_buttons_frame,
                                       text="Set Weight",
                                       bootstyle="primary-outline"
                                       )
        set_weight_button.bind(
            "<Button-1>", lambda event: self.set_weight(weight_input.get()))
        set_weight_button.grid(row=0, column=2)

        # A.1.3 algo chooser frame
        algo_chooser_frame = ttk.Labelframe(col1,
                                            text="Algorithm Chooser",
                                            padding=10)
        algo_chooser_frame.grid(row=1, column=0, sticky='nsew')

        ttk.Label(algo_chooser_frame,
                  text="Algorithm",
                  ).grid(row=0, column=0, padx=(30, 10), pady=(25, 0))
        algo_combobox = ttk.Combobox(
            master=algo_chooser_frame,
            values=["UCS", "A*","Dijkstra", "Floyd-Warshall"],
            state="readonly",
            bootstyle="primary"
        )
        algo_combobox.grid(row=0, column=1, sticky='ew',
                           padx=(30, 10), pady=(25, 0))
        algo_combobox.bind("<<ComboboxSelected>>",
                           lambda event: self.change_algorithm(algo_combobox))

        # A.2 column 2
        col2 = ttk.Frame(self, padding=10)
        col2.grid(row=0, column=1, sticky='nsew')
        col2.grid_columnconfigure(0, weight=1)
        col2.grid_rowconfigure(0, weight=100)
        col2.grid_rowconfigure(1, weight=1)

        # A.2.1 map visual frame
        self.map_frame = ttk.Labelframe(col2,
                                        text="Map",
                                        padding=10)
        self.map_frame.grid(row=0, column=0, sticky='nsew')

        # A.2.2 noti frame
        noti_frame = ttk.Labelframe(col2,
                                    text="Notification",
                                    padding=10)
        noti_frame.grid_propagate(False)
        noti_frame.grid(row=1, column=0, sticky='nsew')
        # A.2.2.1 noti view frame
        noti_view_frame = ttk.Frame(noti_frame)
        noti_view_frame.grid(row=0, column=0, sticky='snew')
        noti_view_frame.grid_rowconfigure(0, weight=1)
        noti_view_frame.grid_columnconfigure(0, weight=1)
        # add noti to noti view frame
        # self.noti_text = ttk.Label(noti_view_frame,
        #                       text="\n".join(self.noti_data),
        #                       anchor='nw',
        #                       justify='left')
        # self.noti_text.grid(row=0, column=0, sticky='nsew')

        self.noti_listbox = tk.Listbox(
            noti_frame, border=0, highlightthickness=0, borderwidth=0)
        self.noti_listbox.pack(fill='both', expand=True)
        self.noti_index = 1

    def change_chooser_start_point(self, cbbox: ttk.Combobox) -> None:
        self.current_find_path_start_point = cbbox.get()
        self.noti_listbox.insert(tk.END, str(
            self.noti_index)+". (Find Path) Choose Starting Point: " + self.current_find_path_start_point)
        self.noti_index += 1
        self.noti_listbox.see(tk.END)
        self.noti_listbox.focus_set()
        self.start_combobox_up.selection_clear()
        self.end_combobox_up.configure(
            values=[x for x in self.start_choices if x != self.current_find_path_start_point])

    def change_chooser_end_point(self, cbbox: ttk.Combobox) -> None:
        self.current_find_path_end_point = cbbox.get()
        self.noti_listbox.insert(tk.END, str(
            self.noti_index)+". (Find Path) Choose Ending Point: " + self.current_find_path_end_point)
        self.noti_index += 1
        self.noti_listbox.see(tk.END)
        self.noti_listbox.focus_set()
        self.end_combobox_up.selection_clear()
        self.start_combobox_up.configure(
            values=[x for x in self.start_choices if x != self.current_find_path_end_point])

    def change_weight_start_point(self, cbbox: ttk.Combobox) -> None:
        self.current_weight_start_point = cbbox.get()
        self.noti_listbox.insert(tk.END, str(
            self.noti_index) + ". (Change Weight) Choose Starting Point: " + self.current_weight_start_point)
        self.noti_index += 1
        self.noti_listbox.focus_set()
        self.start_combobox_down.selection_clear()
        self.noti_listbox.see(tk.END)
        relatives = algorithms.get_relatives(self.data, algorithms.find_point_by_name(
            self.data, self.current_weight_start_point).get('id'))
        self.end_combobox_down.configure(
            values=[x.get('name') for x in self.data if x.get('id') in relatives])
        self.end_combobox_down.set('')
        self.current_weight_end_point = None

    def change_weight_end_point(self, cbbox: ttk.Combobox) -> None:
        self.current_weight_end_point = cbbox.get()
        self.noti_listbox.insert(tk.END, str(
            self.noti_index) + ". (Change Weight) Choose Ending Point: " + self.current_weight_end_point)
        self.noti_index += 1
        self.noti_listbox.focus_set()
        self.end_combobox_down.selection_clear()
        self.noti_listbox.see(tk.END)

    def change_algorithm(self, cbbox: ttk.Combobox) -> None:
        self.current_algorithm = cbbox.get()
        self.noti_listbox.insert(tk.END, str(
            self.noti_index) + ". Choose Algorithm: " + self.current_algorithm)
        self.noti_index += 1
        self.noti_listbox.see(tk.END)
        self.noti_listbox.focus_set()
        cbbox.selection_clear()

    def change_map(self):
        file_path = filedialog.askopenfilename(initialdir="", title="Select a Map File", filetypes=(
            ("JSON files", "*.json"), ("all files", "*.*")))
        if file_path:
            with open(file_path, 'r+', encoding="utf8") as f:
                self.data = json.load(f)
                # transform to dict
                global map_data
                map_data = algorithms.convert_dict_grap(self.data)

                self.json_file_path = file_path
            self.start_choices = []
            for item in self.data:
                self.start_choices.append(item.get('name'))
            self.start_combobox_up.configure(values=self.start_choices)
            self.end_combobox_up.configure(values=self.start_choices)
            self.start_combobox_down.configure(values=self.start_choices)
            self.end_combobox_down.configure(values=[])
            self.noti_listbox.delete(0, tk.END)
            self.noti_listbox.insert(tk.END, "1. Open Map: " + file_path)
            self.noti_index = 2
            self.noti_listbox.focus_set()
            self.noti_listbox.see(tk.END)
            # clear the combo box
            self.start_combobox_up.set('')
            self.end_combobox_up.set('')
            self.start_combobox_down.set('')
            self.end_combobox_down.set('')
            self.current_find_path_start_point = None
            self.current_find_path_end_point = None
            self.current_weight_start_point = None
            self.current_weight_end_point = None

    def find_way(self):
        if self.current_find_path_start_point == None:
            Messagebox.show_error(
                title="Error", message="Please choose starting point")
            return
        elif self.current_find_path_end_point == None:
            Messagebox.show_error(
                title="Error", message="Please choose ending point")
            return
        elif self.current_algorithm == None:
            Messagebox.show_error(
                title="Error", message="Please choose algorithm")
            return
        else:
            start_point = algorithms.find_point_by_name(
                self.data, self.current_find_path_start_point)
            end_point = algorithms.find_point_by_name(
                self.data, self.current_find_path_end_point)
            start_time = time.time()
            if start_point and end_point and self.current_algorithm and self.data:
                path, cost = algorithms.call_algorithm(
                    self.data, start_point, end_point, self.current_algorithm)
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(elapsed_time)
                if len(path) == 0:
                    self.noti_listbox.insert(tk.END, str(
                        self.noti_index) + ". (Find Path) No path found.")
                    self.noti_listbox.insert(
                        tk.END, f"Time taken: {elapsed_time:.5f} s")
                    self.noti_index += 1
                    self.noti_listbox.see(tk.END)
                else:
                    output = ". Path found: "
                    for point in path:
                        output += algorithms.find_point_by_id(
                            self.data, point).get('name') + " -> "
                    self.noti_listbox.insert(
                        tk.END, str(self.noti_index) + output[:-4])
                    self.noti_listbox.insert(tk.END, "Cost: " + str(cost))
                    self.noti_listbox.insert(
                        tk.END, f"Time taken: {elapsed_time:.5f} s")
                    self.noti_index += 1
                    self.noti_listbox.see(tk.END)
            else:
                Messagebox.show_error(
                    title="Error", message="Something went wrong, please check the log")

    def set_weight(self, weight: str):
        if self.current_weight_start_point == None:
            Messagebox.show_error(
                title="Error", message="Please choose starting point")
            return
        elif self.current_weight_end_point == None:
            Messagebox.show_error(
                title="Error", message="Please choose ending point")
            return
        elif weight == "":
            Messagebox.show_error(title="Error", message="Please input weight")
            return
        else:
            start_point = algorithms.find_point_by_name(
                self.data, self.current_weight_start_point)
            end_point = algorithms.find_point_by_name(
                self.data, self.current_weight_end_point)
            if start_point and end_point and self.data:
                try:
                    weight = int(weight)
                except:
                    Messagebox.show_error(
                        title="Error", message="Weight must be an integer")
                    return
                start_point["relative"][end_point["id"]] = weight
                # modify json file
                with open(self.json_file_path, 'r+') as f:
                    data = json.load(f)
                    for item in data:
                        if item.get('id') == start_point.get('id'):
                            del item["relative"][end_point['id']]
                            item["relative"][end_point["id"]] = weight
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f, indent=2)
                self.noti_listbox.insert(tk.END, str(self.noti_index) + ". (Change Weight) Set weight: " +
                                         start_point["name"] + " - " + end_point["name"] + " = " + str(weight))
                self.noti_index += 1
                self.noti_listbox.see(tk.END)
            else:
                Messagebox.show_error(
                    title="Error", message="Something went wrong, please check the log")

# map in tkinter frame


class map:
    def __init__(self, window) -> None:
        self.data = None
        self.window = window.map_frame
        self.button = ttk.Button(
            self.window, text="Map", command=self.load_map)
        self.button.grid(row=0, column=0, sticky='ns')

    def load_map(self):
        global map_data
        self.data : dict = map_data
        # give the graph to the window
        graph = nx.DiGraph()
        # get all nodes name from dict
        nodes_name = list(map_data.keys())
        # add nodes to graph
        graph.add_nodes_from(nodes_name)
        # get all edges from dict
        edges = []
        status = 0
        for node in nodes_name:
            # data is '1': [('2', 1), ('3', 1), ('8', 5)]
            for relative_weight in map_data.get(node):
                for relative in relative_weight:
                    if status == 0:
                        goal = relative
                        status = 1
                    else:
                        edges.append((node, goal, {"weight": int(relative)}))
                        status = 0
        # add edges to graph
        graph.add_edges_from(edges)
        # random layout
        layout = nx.kamada_kawai_layout(graph)
        f = plt.Figure(figsize=(10,10), dpi=120)
        f.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
        a = f.add_subplot()
        a.plot()
        nx.draw_networkx_nodes(graph, layout, node_color='black', node_size=300, ax=a)
        nx.draw_networkx_edges(graph, layout, edge_color='gray', ax=a)
        nx.draw_networkx_labels(graph, layout, font_color='white', ax=a)
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, layout, edge_labels=edge_labels, ax=a)
        
        canvas = FigureCanvasTkAgg(f, master=self.window)
        canvas.get_tk_widget().grid(row=1, column=1, sticky='nsew')
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(1, weight=1)


def app_config(app: ttk.Frame | ttk.Window):
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (1000/2))
    y_cordinate = int((screen_height/2) - (750/2))
    app.geometry("{}x{}+{}+{}".format(1000, 750, x_cordinate, y_cordinate))
    app.minsize(1000, 750)
    return app


if __name__ == "__main__":
    app = ttk.Window("Path Finder")
    app = app_config(app)
    gui = PathFinder(app)
    map = map(gui)
    app.mainloop()
