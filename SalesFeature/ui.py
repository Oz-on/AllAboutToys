# This file contains class that represents window of worker's panel

from tkinter import *
import tkinter as ttk


class Tab:
    def __init__(self, parent_node):
        self.container = ttk.Frame(parent_node, padx=10, pady=10, bg='#fff')

    def show(self):
        self.container.grid(row=0, column=0, sticky=(W, E, N, S))

    def close(self):
        self.container.grid_remove()


class RequestElement:
    def __init__(self, parent_node, user_name, row, message):
        # Wrapper is for giving a margin
        wrapper = ttk.Frame(parent_node, pady=10, bg=parent_node['background'])
        wrapper.grid(column=0, row=row, sticky=(W, E))

        # Container stores every widget related to this component
        container = ttk.Frame(wrapper, bg='#fff', padx=5, pady=5, borderwidth=1, relief='solid')
        # Give a container flexibility
        wrapper.columnconfigure(0, weight=1)
        wrapper.rowconfigure(0, weight=1)
        container.grid(column=0, row=0, sticky=(W, E, N, S))

        # For a now it will be a frame
        image = ttk.Frame(container, bg='#ff0', width=70, height=70)
        image.grid(column=0, row=0, columnspan=2, rowspan=2, sticky=(N, W))

        label = ttk.Label(container, text=user_name, bg=container['background'])
        label.grid(column=2, row=0, rowspan=2, sticky=(N, W))

        request_content = ttk.Label(container, pady=10, bg=container['background'], wraplength=400, text=message)
        request_content.grid(column=0, row=2, columnspan=10, sticky=(N, W))
        container.columnconfigure(2, weight=2)

        reply_button = ttk.Button(container, text='Reply', padx=5, pady=5)
        reply_button.grid(column=10, row=2, sticky=(S, E))


class ReportPreview:
    def __init__(self, parent_node, date_period, row, column):
        # Create wrapper
        wrapper = ttk.Frame(parent_node, pady=5, padx=5, bg=parent_node['background'])
        # Create container
        container = ttk.Frame(wrapper, bg='#fff', padx=5, pady=5, borderwidth=1, relief='solid')

        wrapper.grid(column=column, row=row)
        container.grid(column=0, row=0, sticky=(N, W, E, S))

        # Stretch container to fit whole wrapper
        wrapper.columnconfigure(0, weight=1)
        wrapper.rowconfigure(0, weight=1)

        report_image = ttk.Frame(container, bg='#eeba31', width=70, height=70)
        label = ttk.Label(container, text=date_period, bg=container['background'])
        button = ttk.Button(container, text='Open', padx=5, pady=5)

        report_image.grid(column=0, row=0, columnspan=2, rowspan=2, sticky=N)
        label.grid(row=2, column=0, sticky=N)
        button.grid(column=0, row=3)


class DiscountsTab(Tab):
    def __init__(self, parent_node):
        super().__init__(parent_node)


class SalesReportTab(Tab):
    def __init__(self, parent_node):
        super().__init__(parent_node)

        ReportPreview(self.container, '01.07.2020', 0, 0)
        ReportPreview(self.container, '01.08.2020', 0, 1)
        ReportPreview(self.container, '01.09.2020', 0, 2)


class CustomerRequestTab(Tab):
    def __init__(self, parent_node):
        super().__init__(parent_node)

        # Container for elements
        self.container.columnconfigure(0, weight=1)

        # Add elements
        RequestElement(self.container, user_name='John Doe', row=0, message='vsiooihvoishvosihvsoivhoishvoihvoishfioshoivhsoihvsvoih')
        RequestElement(self.container, user_name='Capitan America', row=1, message='vsiooihvoishvosihvsoivhoishvoihvoishfioshoivhsoihvsvoih')
        RequestElement(self.container, user_name='Lewis', row=2, message='pojgrsopjsgporjgrpsogjpsogjsprogjsprojsrpgosrgjspogj')


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
    It is responsible for Panel for workers, where Sale Staff
    can reply for user enquiries, generate sales reports and apply discount schemes
    """
    def __init__(self, parent_node):
        # Container stores everything that is in this class
        container = ttk.Frame(parent_node, bg='#fff')
        # left_panel stores only buttons for switching frames
        left_panel = ttk.Frame(container, bg='#ebebeb', padx=5, width=200, borderwidth=1, relief='solid')
        # Center panel will be main panel for every frame with main functionality
        center_panel = ttk.Frame(container, bg='#ff04ff')

        # Place all elements
        container.grid(column=0, row=0, sticky=(N, W, E, S))
        left_panel.grid(column=0, row=0, rowspan=12, sticky=(N, S, W))
        center_panel.grid(column=1, row=0, columnspan=10, rowspan=12, sticky=(N, W, E, S))

        # set left panel to be resizable
        container.rowconfigure(0, weight=1)
        # Set center panel to be resizable
        container.columnconfigure(1, weight=1)
        container.rowconfigure(1, weight=1)
        # Set all tabs to be resizable
        center_panel.columnconfigure(0, weight=1)
        center_panel.rowconfigure(0, weight=1)

        # Create particular tabs
        # Initialize tabs
        self.customer_request_tab = CustomerRequestTab(center_panel)
        self.sales_report_tab = SalesReportTab(center_panel)
        self.discounts_tab = DiscountsTab(center_panel)

        # Set current tab that will display customer request tab when user will open the app
        self.current_tab = self.customer_request_tab
        self.current_tab.show()

        # Add buttons to left panel
        self.cust_req_btn = SectionButton(parent_node=left_panel, text='Customer requests', col=1, row=0, handle_click=lambda: self.open_tab(self.customer_request_tab), disabled=True)
        self.sales_btn = SectionButton(parent_node=left_panel, text='Sales reports', col=1, row=1, handle_click=lambda: self.open_tab(self.sales_report_tab))
        self.discount_btn = SectionButton(parent_node=left_panel, text='Discount Schemes', col=1, row=2, handle_click=lambda: self.open_tab(self.discounts_tab))

    def open_tab(self, tab_to_open):
        self.current_tab.close()
        self.current_tab = tab_to_open
        self.current_tab.show()

    def open_customer_request_tab(self):
        self.open_tab(self.customer_request_tab)
        self.cust_req_btn.disable_button()
        self.discount_btn.enable_button()
        self.sales_btn.enable_button()
