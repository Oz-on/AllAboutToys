# Author: Oskar Domingos
# This file contains views for features related to Discount Schemes

from tkinter import *
import tkinter as ttk
from SalesFeature.Views.TabUI import Tab, SubTab
from SalesFeature.interfaces import PreviewInterface


class DiscountPreview(PreviewInterface):
    def __init__(self, parent_node, discount_scheme, column, row, handle_open, handle_remove):
        self._discount_scheme = discount_scheme
        self._column = column
        self._row = row
        self.__handle_open = handle_open
        self.__handle_remove = handle_remove

        self._wrapper = ttk.Frame(parent_node, pady=5, padx=5, bg=parent_node['background'])

        self.__generate_view()

    def __generate_view(self):
        # Create container
        container = ttk.Frame(self._wrapper, bg='#fff', padx=5, pady=5, borderwidth=1, relief='solid')
        container.grid(column=0, row=0, sticky=(N, W, E, S))

        # Stretch container to fit whole wrapper
        self._wrapper.columnconfigure(0, weight=1)
        self._wrapper.rowconfigure(0, weight=1)

        discount_image = ttk.Frame(container, bg='#eeba31', width=70, height=70)
        label = ttk.Label(container, text=self._discount_scheme.discount_percentage)
        edit_btn = ttk.Button(
            container,
            text='Edit',
            padx=5,
            pady=5,
            command=lambda: self.__handle_open(self._discount_scheme)
        )
        remove_btn = ttk.Button(
            container,
            text='Remove',
            padx=5,
            pady=5,
            command=lambda: self.__handle_remove(self._discount_scheme)
        )

        discount_image.grid(column=0, row=0, columnspan=2, rowspan=2, sticky=N)
        label.grid(row=2, column=0, sticky=N)
        edit_btn.grid(column=0, row=3)
        remove_btn.grid(column=0, row=4)

    def remove(self):
        self._wrapper.grid_remove()

    def show(self):
        self._wrapper.grid(column=self._column, row=self._row)


class DiscountSchemesTabUI(Tab):
    def __init__(self, parent_node, discounts, handle_open_discount, handle_remove_discount, handle_open_creation_panel):
        super().__init__(parent_node)

        self.__handle_open_discount = handle_open_discount
        self.__handle_remove_discount = handle_remove_discount
        self.__handle_open_creation_panel = handle_open_creation_panel

        self._preview_views = self.__generate_previews(discounts)

        self.__generate_top_panel()

        self.__render_previews()

    def __generate_previews(self, discounts):
        previews = []
        for i in range(len(discounts)):
            row = (len(discounts) // 5) + 2
            preview = DiscountPreview(
                parent_node=self.container,
                discount_scheme=discounts[i],
                row=row,
                column=i,
                handle_open=self.__handle_open_discount,
                handle_remove=self.__handle_remove_discount,
            )
            previews.append(preview)

        return previews

    def __generate_top_panel(self):
        # It generates top panel with one button for creating new discount scheme

        # Top panel container
        top_panel = ttk.Frame(self.container)
        top_panel.grid(column=0, row=0, sticky=(N, W, E), columnspan=12, rowspan=2)

        # Add label
        label = ttk.Label(top_panel, text="Create new scheme")
        label.grid(column=0, row=0, sticky=(N, W))

        button = ttk.Button(
            top_panel,
            text="Create",
            command=lambda: self.__handle_open_creation_panel()
        )

        button.grid(column=2, row=0)

    def __render_previews(self):
        for preview in self._preview_views:
            preview.show()

    def update_previews(self, discounts):
        # It updates list of views after view deletion or view creation
        # Firstly remove
        for preview in self._preview_views:
            preview.remove()

        # Generate new previews
        self._preview_views = self.__generate_previews(discounts)

        # Render new previews
        self.__render_previews()


class DiscountSchemesDetails(SubTab):
    def __init__(self, parent_node, handle_back, discount):
        super().__init__(parent_node)

        self.__handle_back = handle_back
        self._discount = discount

        self._rows = 0

        self._rows = self.generate_top_panel(self.__handle_back)

        self.__generate_main_panel()

    def __generate_main_panel(self):
        # It generates main panel with possibility to create new discount scheme
        main_panel = ttk.Frame(self.container, bg='#fff')
        main_panel.grid(column=0, row=self._rows, sticky=(N, W, E, S), columnspan=12)

        id_label = ttk.Label(main_panel, text='Id of discount scheme:')
        id_label.grid(column=0, row=1, columnspan=1, sticky=(N, W))

        id_label= ttk.Label(main_panel, text=self._discount.discount_scheme_id)
        id_label.grid(column=1, row=1, columnspan=8, sticky=(W,))

        details_label = ttk.Label(main_panel, text='Description of the discount Scheme')
        details_label.grid(column=0, row=2, sticky=(W,))

        details_text = ttk.Label(main_panel, text=self._discount.details)
        details_text.grid(column=0, row=3, sticky=(W,), columnspan=10, rowspan=5)

        percentage_label = ttk.Label(main_panel, text='Percentage of discount')
        percentage_label.grid(column=0, row=8, sticky=(W,))

        percentage_entry = ttk.Label(main_panel, text=self._discount.discount_percentage)
        percentage_entry.grid(column=1, row=8, sticky=(W,))

        percentage_label_sign = ttk.Label(main_panel, text='%')
        percentage_label_sign.grid(column=2, row=8, sticky=(W,))


class DiscountSchemesCreationPanel(SubTab):
    def __init__(self, parent_node, handle_back, handle_create_discount_scheme):
        super().__init__(parent_node)

        self.__handle_back = handle_back
        self.__handle_create_discount_scheme = handle_create_discount_scheme

        self._rows = 0

        self._rows = self.generate_top_panel(self.__handle_back)
        self.__generate_main_panel()

    def __generate_main_panel(self):
        # It generates main panel with possibility to create new discount scheme
        main_panel = ttk.Frame(self.container, bg='#fff')
        main_panel.grid(column=0, row=self._rows, sticky=(N, W, E, S), columnspan=12)

        id_label = ttk.Label(main_panel, text='Id of discount scheme:')
        id_label.grid(column=0, row=1, columnspan=1, sticky=(N, W))

        id_entry = ttk.Entry(main_panel)
        id_entry.grid(column=1, row=1, columnspan=8, sticky=(W,))

        details_label = ttk.Label(main_panel, text='Description of the discount Scheme')
        details_label.grid(column=0, row=2, sticky=(W,))

        details_text = ttk.Text(main_panel)
        details_text.grid(column=0, row=3, sticky=(W,), columnspan=10, rowspan=5)

        percentage_label = ttk.Label(main_panel, text='Percentage of discount')
        percentage_label.grid(column=0, row=8, sticky=(W,))

        percentage_entry = ttk.Entry(main_panel)
        percentage_entry.grid(column=1, row=8, sticky=(W,))

        percentage_label_sign = ttk.Label(main_panel, text='%')
        percentage_label_sign.grid(column=2, row=8, sticky=(W,))

        submit_btn = ttk.Button(
            main_panel,
            text='submit',
            command=lambda: self.__handle_create_discount_scheme(
                discount_scheme_id=id_entry.get(),
                details=details_text.get("1.0","end-1c"),
                discount_percentage=percentage_entry.get()
            )
        )
        submit_btn.grid(column=0, row=9, sticky=(W,))
