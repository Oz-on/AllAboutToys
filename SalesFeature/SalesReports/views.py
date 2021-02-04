# Author: Oskar Domingos
from tkinter import *
import tkinter as ttk
from SalesFeature.Views.TabUI import Tab
from SalesFeature.interfaces import PreviewInterface


class ReportPreview(PreviewInterface):
    def __init__(self, parent_node, sales_report, column, row, handle_open):
        self._column = column
        self._row = row
        self._sales_report = sales_report
        self._handle_open = handle_open
        # Create wrapper
        self._wrapper = ttk.Frame(parent_node, pady=5, padx=5, bg=parent_node['background'])

        self.__generate_view()

    def __generate_view(self):
        # Create container
        container = ttk.Frame(self._wrapper, bg='#fff', padx=5, pady=5, borderwidth=1, relief='solid')
        container.grid(column=0, row=0, sticky=(N, W, E, S))

        # Stretch container to fit whole wrapper
        self._wrapper.columnconfigure(0, weight=1)
        self._wrapper.rowconfigure(0, weight=1)

        report_image = ttk.Frame(container, bg='#eeba31', width=70, height=70)
        label = ttk.Label(container, text=self._sales_report.sales_period, bg=container['background'])
        button = ttk.Button(
            container,
            text='Open',
            padx=5,
            pady=5,
            command=lambda: self._handle_open(self._sales_report)
        )

        report_image.grid(column=0, row=0, columnspan=2, rowspan=2, sticky=N)
        label.grid(row=2, column=0, sticky=N)
        button.grid(column=0, row=3)

    def remove(self):
        self._wrapper.grid_remove()

    def show(self):
        self._wrapper.grid(column=self._column, row=self._row)


class SalesReportDetails(Tab):
    def __init__(self, parent_node, total_revenue, total_sales, sales_p_prod, sales_p_cat, top_ten_best_selling, handle_back, handle_export_csv):
        super().__init__(parent_node)

        self._total_revenue = total_revenue
        self._total_sales = total_sales
        self._sales_p_prod = sales_p_prod
        self._sales_p_cat = sales_p_cat
        self._top_ten_best_selling = top_ten_best_selling
        self.__handle_back = handle_back
        self.__handle_export_csv = handle_export_csv

        self._rows = 0
        self._rows = self.__generate_top_panel()

        # Total revenue
        total_revenue_label = ttk.Label(self.container, text=f'Total revenue: {self._total_revenue}')
        total_revenue_label.grid(column=0, row=self._rows, sticky=(N, W))

        self._rows += 1

        # Total Sale Label
        self._rows = self.__generate_sales_p_prod()

        # Number of sold toys per toy
        self._rows = self.__generate_num_sold_toys()

        # Number of sold toys per category
        self._rows = self.__generate_num_sold_category()

        self._rows = self.__generate_top_best_selling()

    def __generate_top_panel(self):
        top_panel_c = ttk.Frame(self.container)
        top_panel_c.grid(column=0, row=0, sticky=(N, W, E), columnspan=12)

        back_button = ttk.Button(
            top_panel_c,
            text="Back",
            command=self.__handle_back,
        )

        back_button.grid(column=0, row=0)

        return self._rows + 1

    def __generate_sales_p_prod(self):
        rows = self._rows
        # Total Sale Label
        total_sale_label = ttk.Label(self.container, text=f'Sales Per product: ')

        # Add button for generating csv report
        generate_btn = ttk.Button(
            self.container,
            text="Export to csv",
            command=lambda: self.__handle_export_csv('total')
        )

        total_sale_label.grid(column=0, row=2, sticky=(N, W))
        generate_btn.grid(column=1, row=2, sticky=(N, W))

        rows += 1

        toys = list(self._total_sales.keys())
        for i in range(len(toys)):
            rows += 1
            key = toys[i]
            value = self._total_sales[key]
            key_label = ttk.Label(self.container, text=key)
            key_label.grid(column=0, row=i + 3, sticky=(N, W))

            value_label = ttk.Label(self.container, text=value)
            value_label.grid(column=1, row=i + 3, sticky=(N, W))

        return rows

    def __generate_num_sold_toys(self):
        rows = self._rows

        sold_toys_label = ttk.Label(self.container, text=f'Number of Sold toys for every particular toy: ')
        sold_toys_label.grid(column=0, row=rows, sticky=(N, W))

        # Add button for generating csv report
        generate_btn = ttk.Button(
            self.container,
            text="Export to csv",
            command=lambda: self.__handle_export_csv('pod_sale')
        )
        generate_btn.grid(column=1, row=rows, sticky=(N, W))

        rows += 1

        toys = list(self._sales_p_prod.keys())
        for i in range(len(toys)):
            rows += 1
            key = toys[i]
            value = self._sales_p_prod[key]
            key_label = ttk.Label(self.container, text=key)
            key_label.grid(column=0, row=rows, sticky=(N, W))

            value_label = ttk.Label(self.container, text=value)
            value_label.grid(column=1, row=rows, sticky=(N, W))

        rows += 1

        return rows

    def __generate_num_sold_category(self):
        rows = self._rows

        sold_toys_cat = ttk.Label(self.container, text=f'Number of Sold toys per category: ')

        # Add button for generating csv report
        generate_btn = ttk.Button(
            self.container,
            text="Export to csv",
            command=lambda: self.__handle_export_csv('cat_sale')
        )

        sold_toys_cat.grid(column=0, row=rows, sticky=(N, W))
        generate_btn.grid(column=1, row=rows, sticky=(N, W))

        rows += 1

        toys = list(self._sales_p_cat.keys())
        for i in range(len(toys)):
            rows += 1
            key = toys[i]
            value = self._sales_p_cat[key]
            key_label = ttk.Label(self.container, text=key)
            key_label.grid(column=0, row=rows, sticky=(N, W))

            value_label = ttk.Label(self.container, text=value)
            value_label.grid(column=1, row=rows, sticky=(N, W))

        rows += 1

        return rows

    def __generate_top_best_selling(self):
        rows = self._rows

        top_ten_label = ttk.Label(self.container, text="Top ten best selling products: ")
        # Add button for generating csv report
        generate_btn = ttk.Button(
            self.container,
            text="Export to csv",
            command=lambda: self.__handle_export_csv('top_prod')
        )

        top_ten_label.grid(column=0, row=rows, sticky=(N, W))
        generate_btn.grid(column=1, row=rows, sticky=(N, W))

        for i in range(len(self._top_ten_best_selling)):
            rows += 1
            toy = self._top_ten_best_selling[i][0]
            key_label = ttk.Label(self.container, text=f'{i+1}. {toy}')
            key_label.grid(column=0, row=rows, sticky=(N, W))

        rows += 1

        return rows


# Main tab of sales report
class SalesReportTab(Tab):
    def __init__(self, parent_node, sales_months, select_period, sales_reports, handle_open_report):
        super().__init__(parent_node)

        self._select_period = select_period
        self._sales_months = sales_months
        self._handle_open_report = handle_open_report

        # Generate previews of sales reports
        self._preview_views = self.__generate_previews(sales_reports)
        # Render these previews
        self.render_reports()

        self.__generate_top_panel()

    def __generate_previews(self, sales_reports):
        # It generates previews of sales report
        previews = []

        # Create new previews based on sales_reports
        for i in range(len(sales_reports)):
            row = (len(sales_reports) // 5) + 2
            preview = ReportPreview(
                parent_node=self.container,
                sales_report=sales_reports[i],
                row=row,
                column=i,
                handle_open=self._handle_open_report
            )
            previews.append(preview)

        return previews

    def __generate_top_panel(self):
        # It generates top panel

        # Top panel container
        self._top_panel_c = ttk.Frame(self.container)
        self._top_panel_c.grid(column=0, row=0, sticky=(N, W, E), columnspan=12, rowspan=2)

        # Beginning of the period
        self._beg_period_label = ttk.Label(self._top_panel_c, text="Select beginning of the period:")
        self._beg_period_label.grid(column=0, row=0, sticky=(N, W))

        # Add picker for start date of period
        start_period_v = ttk.StringVar(self._top_panel_c)
        start_period_v.set(self._sales_months[0])
        option_menu = ttk.OptionMenu(self._top_panel_c, start_period_v, *self._sales_months)
        option_menu.grid(column=1, row=0)

        # Ending of the period
        end_period_label = ttk.Label(self._top_panel_c, text="Select ending of the period: ")
        end_period_label.grid(column=2, row=0, sticky=(N, W))

        # Add picker for end date of period
        end_period_v = ttk.StringVar(self._top_panel_c)
        end_period_v.set(self._sales_months[0])
        option_menu = ttk.OptionMenu(self._top_panel_c, end_period_v, *self._sales_months)
        option_menu.grid(column=3, row=0)

        # Add button for generating period
        generate_button = ttk.Button(
            self._top_panel_c,
            text="Generate",
            command=lambda: self._select_period(start_period_v, end_period_v)
        )

        generate_button.grid(column=4, row=0)

    def add_sales_report(self, sales_report):
        row = (len(self._preview_views) // 5) + 2
        column = len(self._preview_views)

        preview = ReportPreview(
            parent_node=self.container,
            sales_report=sales_report,
            row=row,
            column=column,
            handle_open=self._handle_open_report
        )
        self._preview_views.append(preview)

    def render_reports(self):
        # It places reports previews on the screen
        for preview in self._preview_views:
            preview.show()
