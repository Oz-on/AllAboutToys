# Author: Oskar Domingos

from tkinter import *
import tkinter as ttk
from SalesFeature.Views.TabUI import Tab, SubTab
from SalesFeature.interfaces import PreviewInterface


class RequestElement(PreviewInterface):
    def __init__(self, parent_node, request, row, handle_reply):
        self._row = row
        self._request = request
        self.__handle_reply = handle_reply
        # Wrapper is for giving a margin
        self._wrapper = ttk.Frame(parent_node, pady=10, bg=parent_node['background'])

        self.__generate_view()

    def __generate_view(self):
        # Container stores every widget related to this component
        container = ttk.Frame(self._wrapper, bg='#fff', padx=5, pady=5, borderwidth=1, relief='solid')
        # Give a container flexibility
        self._wrapper.columnconfigure(0, weight=1)
        self._wrapper.rowconfigure(0, weight=1)
        container.grid(column=0, row=0, sticky=(W, E, N, S))

        # For a now it will be a frame
        image = ttk.Frame(container, bg='#ff0', width=70, height=70)
        image.grid(column=0, row=0, columnspan=2, rowspan=2, sticky=(N, W))

        # Label for username
        label = ttk.Label(
            container,
            text=self._request.author.username,
            bg=container['background']
        )
        label.grid(column=2, row=0, rowspan=2, sticky=(N, W))

        # Label for content of the request
        request_content = ttk.Label(
            container,
            pady=10,
            bg=container['background'],
            wraplength=400,
            text=self._request.content
        )
        request_content.grid(column=0, row=2, columnspan=10, sticky=(N, W))
        container.columnconfigure(2, weight=2)

        reply_button = ttk.Button(
            container,
            text='Reply',
            padx=5,
            pady=5,
            command=lambda: self.__handle_reply(self._request)
        )
        reply_button.grid(column=10, row=2, sticky=(S, E))

    def remove(self):
        self._wrapper.grid_remove()

    def show(self):
        print('show request: ', self._request)
        self._wrapper.grid(column=0, row=self._row, sticky=(W, E))


class CustomerRequestDetails(SubTab):
    def __init__(self, parent_node, customer_request, handle_back, send_reply):
        super().__init__(parent_node)

        self._customer_request = customer_request
        self.__handle_back = handle_back
        self.__send_reply = send_reply
        self._rows = 0

        self._rows = self.generate_top_panel(handle_back)

        self.__generate_main_panel()

    def __generate_main_panel(self):
        # It generates main panel with message and possibility to reply
        main_panel = ttk.Frame(self.container, bg='#fff')
        main_panel.grid(column=0, row=self._rows, sticky=(N, W, E, S), columnspan=12)

        image = ttk.Frame(main_panel, bg='#ff0', width=70, height=70)
        image.grid(column=0, row=1, columnspan=2, rowspan=2, sticky=(N, W))

        username_label = ttk.Label(main_panel, text=self._customer_request.author.username)
        username_label.grid(column=2, row=1, rowspan=2, sticky=(N, W))

        # Label for content of the request
        request_content = ttk.Label(
            main_panel,
            pady=10,
            wraplength=400,
            text=self._customer_request.content
        )
        request_content.grid(column=0, row=3, columnspan=10, sticky=(N, W))
        main_panel.columnconfigure(2, weight=2)

        # add text input for staff
        text_box = ttk.Text(main_panel, bg='#ebebeb')
        text_box.grid(column=0, row=5, columnspan=10, sticky=W)

        submit_btn = ttk.Button(
            main_panel,
            text='Submit',
            padx=5,
            pady=5,
            command=lambda: self.__send_reply(text_box.get("1.0","end-1c"))
        )

        submit_btn.grid(column=9, row=10)


class CustomerRequestsTabUI(Tab):
    def __init__(self, parent_node, customer_requests, handle_open):
        super().__init__(parent_node)

        self._customer_requests_type = 'query'
        self.__handle_open = handle_open

        # Container for elements
        self.container.columnconfigure(0, weight=1)

        # Generate picker
        self.__generate_top_panel()

        # Generate previews
        query_previews, review_previews = self.__generate_previews(customer_requests)
        self._previews = {
            'query': query_previews,
            'review': review_previews,
        }
        self.__render_previews()

    def __generate_top_panel(self):
        # It generates picker for choosing type of the request
        self._top_panel = ttk.Frame(self.container)

        self._top_panel.grid(column=0, row=0, sticky=(N, W, E), columnspan=12, rowspan=2)

        # Add label
        label = ttk.Label(self._top_panel, text="Select request type:")
        label.grid(column=0, row=0, sticky=(N, W))

        # Add picker
        picker_current = ttk.StringVar(self._top_panel)
        picker_current.set(self._customer_requests_type)
        picker = ttk.OptionMenu(self._top_panel, picker_current, 'review', 'query')
        picker.grid(column=1, row=0)

        change_btn = ttk.Button(
            self._top_panel,
            text="Change type",
            command=lambda: self.__change_request_type(picker_current.get())
        )
        change_btn.grid(column=2, row=0)

    def __generate_previews(self, requests):
        # It generates request's previews based on given list
        query_previews = []
        review_previews = []
        for i in range(len(requests)):
            request = requests[i]
            preview = RequestElement(
                parent_node=self.container,
                request=request,
                row=i+2,
                handle_reply=self.__handle_open
            )
            if request.request_type == 'query':
                query_previews.append(preview)
            elif request.request_type == 'review':
                review_previews.append(preview)

        return query_previews, review_previews

    def __render_previews(self):
        for preview in self._previews[self._customer_requests_type]:
            preview.show()

    def __change_request_type(self, new_type):
        for preview in self._previews[self._customer_requests_type]:
            preview.remove()

        self._customer_requests_type = new_type
        self.__render_previews()

    def update_previews(self, requests):
        # IT updates list of previews
        # Hie all previews that should be visible
        for preview in self._previews[self._customer_requests_type]:
            preview.remove()

        # generate new previews
        self._previews['query'], self._previews['review'] = self.__generate_previews(requests)

        # render actual previews
        self.__render_previews()
