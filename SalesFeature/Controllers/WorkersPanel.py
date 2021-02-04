# Author: Oskar Domingos
# This file contains Controller class that controls all functionality related to Sales Staff Feature 4

from SalesFeature.Views.ui import WorkersPanel
from Shared.logic import DB
from SalesFeature.SalesReports.Controllers import SalesTab
from SalesFeature.CustomerRequests.Controllers import CustomerRequestsTab
from SalesFeature.Discounts.Controllers import DiscountsTab
import tkinter as tk


class WorkersPanelController:
    def __init__(self, root):
        self._root = tk.Tk()
        self._root.title('All About Toys')
        self._root.minsize(1024, 720)
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)
        self._root.grid()
        # Database class, contains all data required for working feature
        self._database = DB()

        # Create view
        self.__create_view()

        # Create controller for every sub feature
        self._sales_tab = SalesTab(self._view, self._database)
        self._customer_request_tab = CustomerRequestsTab(self._view, self._database)
        self._discounts_tab = DiscountsTab(self._view, self._database)

        # Tab which is actually opened
        self._current_tab = self._sales_tab.view

        # Show current tab to the user
        self._current_tab.show()

    def __open_tab(self, tab_to_open):
        """It opens tab given as an argument"""
        self._current_tab.close()
        self._current_tab = tab_to_open
        self._current_tab.show()

    def __create_view(self):
        # Place WorkersPanel on screen
        # Main UI Class which holds other classes related to Sales Staff Features
        self._view = WorkersPanel(self._root, self.__open_tab)
