# Author: Oskar Domingos
# This class is a super class for every tab in SalesFeature

from tkinter import *
import tkinter as ttk


class Tab:
    def __init__(self, parent_node):
        self.container = ttk.Frame(parent_node, padx=10, pady=10, bg='#fff')

    def show(self):
        self.container.grid(row=0, column=0, sticky=(W, E, N, S))

    def close(self):
        self.container.grid_remove()


class SubTab(Tab):
    def __init__(self, parent_node):
        super().__init__(parent_node)

        self._rows = 0

    def generate_top_panel(self, command):
        top_panel = ttk.Frame(self.container)
        top_panel.grid(column=0, row=self._rows, sticky=(N, W, E), columnspan=12)

        back_button = ttk.Button(
            top_panel,
            text="Back",
            command=lambda: command()
        )

        back_button.grid(column=0, row=0)

        return self._rows + 1
