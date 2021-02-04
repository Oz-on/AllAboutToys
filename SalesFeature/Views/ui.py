# Author: Oskar Domingos
# This file contains class that represents window of worker's panel

from tkinter import *
import tkinter as ttk


class SectionButton:
    """
    Class represents buttons in left panel for switching between views
    """
    def __init__(self, parent_node, text, col, row, handle_click, disabled=False):
        self.container = ttk.Frame(parent_node, pady=5, bg='#ebebeb')
        self.button = ttk.Button(self.container, text=text, pady=5, command=handle_click, default='active' if disabled else 'disabled')

        self.container.grid(column=col, row=row, sticky=(W, E))
        self.button.grid(column=0, row=0, sticky=(W, E, N, S))
        self.container.columnconfigure(0, weight=1)

    def enable_button(self):
        self.button.state['!disabled']

    def disable_button(self):
        self.button.state['disabled']


class WorkersPanel:
    """
    Main panel for Sales Staff Features.
    It is responsible for Panel for workers, where Sale Staff
    can reply for user enquiries, generate sales reports and apply discount schemes
    """
    def __init__(self, parent_node, change_tab):
        # Container stores everything that is in this class
        self._container = ttk.Frame(parent_node, bg='#fff')

        # left_panel stores only buttons for switching frames
        self._left_panel = ttk.Frame(self._container, bg='#ebebeb', padx=5, width=200, borderwidth=1, relief='solid')

        # Center panel will be main panel for every frame with main functionality
        self._center_panel = ttk.Frame(self._container, bg='#ff04ff')

        self._customer_req_tab = None
        self._sales_report_tab = None
        self._discounts_tab = None

        # Place all elements
        self._container.grid(column=0, row=0, sticky=(N, W, E, S))
        self._left_panel.grid(column=0, row=0, rowspan=12, sticky=(N, S, W))
        self._center_panel.grid(column=1, row=0, columnspan=10, rowspan=12, sticky=(N, W, E, S))

        # set left panel to be resizable
        self._container.rowconfigure(0, weight=1)
        # Set center panel to be resizable
        self._container.columnconfigure(1, weight=1)
        self._container.rowconfigure(1, weight=1)
        # Set all tabs to be resizable
        self._center_panel.columnconfigure(0, weight=1)
        self._center_panel.rowconfigure(0, weight=1)

        # Add buttons to left panel
        self._cust_req_btn = SectionButton(
            parent_node=self._left_panel,
            text='Customer requests',
            col=1,
            row=0,
            handle_click=lambda: change_tab(self._customer_req_tab),
        )
        self._sales_btn = SectionButton(
            parent_node=self._left_panel,
            text='Sales reports',
            col=1,
            row=1,
            handle_click=lambda: change_tab(self._sales_report_tab)
        )
        self._discount_btn = SectionButton(
            parent_node=self._left_panel,
            text='Discount Schemes',
            col=1,
            row=2,
            handle_click=lambda: change_tab(self._discounts_tab)
        )

    @property
    def center_panel(self):
        return self._center_panel

    @property
    def sales_report_tab(self):
        return self._sales_report_tab

    @sales_report_tab.setter
    def sales_report_tab(self, tab):
        self._sales_report_tab = tab

    @property
    def customer_req_tab(self):
        return self._customer_req_tab

    @customer_req_tab.setter
    def customer_req_tab(self, tab):
        self._customer_req_tab = tab

    @property
    def discounts_tab(self):
        return self._discounts_tab

    @discounts_tab.setter
    def discounts_tab(self, tab):
        self._discounts_tab = tab

