# Author: Oskar Domingos
import datetime
from SalesFeature.interfaces import TabControllerInterface, SubTabControllerInterface
from SalesFeature.SalesReports.views import SalesReportTab, SalesReportDetails
from SalesFeature.SalesReports.models import Sale


class SalesReport(SubTabControllerInterface):
    """
    It represents sale report
    """
    def __init__(self, parent_view, sales, sales_period, handle_back):
        self._parent_view = parent_view
        # It contains start month and end month from which sales was passed
        self._sales_period = sales_period
        self._sales = sales
        self.__handle_back = handle_back

        # Total revenue for given period
        self._total_revenue = self.__calc_total_revenue()
        # Total sale for given period
        self._total_sale = self.__calc_total_sale()
        # Sales per product
        self._prod_sale = self.__calc_prod_sale()
        # Sales per category
        self._cat_sale = self.__calc_cat_sale()

        self.__create_view()

    def __create_view(self):
        # generate view for Sale Report
        # Create new View of SalesReportDetails
        self._view = SalesReportDetails(
            self._parent_view.center_panel,
            self._total_revenue,
            self._total_sale,
            self._prod_sale,
            self._cat_sale,
            self.__get_ten_top_prod(),
            self.__handle_back,
            self.__export_to_csv,
        )

    def __calc_total_sale(self):
        # it calculates total sales for every particular product
        products_sale = {}
        for sale in self._sales:
            product = sale.product
            if product.name in products_sale:
                products_sale[product.name] += sale.total
            else:
                products_sale[product.name] = sale.total

        return products_sale

    def __calc_total_revenue(self):
        # It calculates total revenue for all sold products
        total = 0
        for sale in self._sales:
            total += sale.total
        return total

    def __calc_cat_sale(self):
        # It calculates number of sales per product category
        categories_sale = {}
        for sale in self._sales:
            category = sale.product.category
            if category.name in categories_sale:
                categories_sale[category.name] += 1
            else:
                categories_sale[category.name] = 1

        return categories_sale

    def __calc_prod_sale(self):
        # It calculates number of sales per specific product
        products_sale = {}
        for sale in self._sales:
            product = sale.product
            if product.name in products_sale:
                products_sale[product.name] += 1
            else:
                products_sale[product.name] = 1

        return products_sale

    def __get_ten_top_prod(self):
        top_ten = [[key, self._prod_sale[key]] for key in list(self._prod_sale.keys())]
        top_ten.sort(key=lambda element: element[1], reverse=True)

        return top_ten

    def __export_to_csv(self, data_type):
        # Export particular data to csv file
        file_name = f'{self.sales_period[0]}-{self.sales_period[1]}.csv'
        if data_type == 'prod_sale':
            # Export sales per product
            file_name = 'sales_per_products_' + file_name
            header = 'toy;quantity_sold\n'

            with open(file_name, 'w') as file:
                file.write(header)
                for toy_name in self._prod_sale:
                    file.write(f'{toy_name};{self._prod_sale[toy_name]}\n')

        elif data_type == 'cat_sale':
            # Export sales per category
            file_name = 'sales_per_category_' + file_name
            header = 'category;quantity_sold\n'

            with open(file_name, 'w') as file:
                file.write(header)
                for category_name in self._cat_sale:
                    file.write(f'{category_name};{self._prod_sale[category_name]}\n')

        elif data_type == 'top_prod':
            # Export top selling products
            file_name = 'top_selling_products_' + file_name
            header = 'number;toy\n'

            with open(file_name, 'w') as file:
                file.write(header)

                top_ten_prod = self.__get_ten_top_prod()
                for i in range(len(top_ten_prod)):
                    file.write(f'{i};{top_ten_prod[i]}\n')

        elif data_type == 'total':
            file_name = 'total_revenue_' + file_name
            header = 'toy;revenue\n'

            with open(file_name, 'w') as file:
                file.write(header)
                for toy in self._total_sale:
                    file.write(f'{toy};{self._total_sale[toy]}\n')

    @property
    def view(self):
        return self._view

    @property
    def sales_period(self):
        return f'{self._sales_period[0]}-{self._sales_period[1]}'


class SalesTab(TabControllerInterface):
    def __init__(self, parent_view, database):
        self._database = database
        self._parent_view = parent_view
        self._sales_reports = []
        self._current_sales_report = None
        self._sales = self.__get_sales()

        # list of months in which sales were made
        self._period_dates = self.__calc_period_dates()

        self.__create_view()

    def __get_sales(self):
        # It gets sales from db
        sales = []
        for db_sale in self._database.sales:
            sales.append(
                Sale(
                    sale_id=db_sale['id'],
                    product=db_sale['product'],
                    purchase_date=db_sale['receipt_date'],
                    quantity=db_sale['quantity']
                )
            )

        return sales

    def __calc_period_dates(self):
        # It gets months of every sale and adds it to the list if
        # they are not duplicated

        period_dates = []
        # Firstly get all different months
        for sale in self._sales:

            date = datetime.datetime.strptime(sale.purchase_date, "%Y-%m-%d")
            date = date.date()
            if date not in period_dates:
                period_dates.append(date)

        return period_dates

    def __handle_select_period(self, start_period_date, end_period_date):
        start_date = datetime.datetime.strptime(start_period_date.get(), "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_period_date.get(), "%Y-%m-%d").date()
        print(start_date, end_date)
        # get only sales for given month
        period_sales = []
        for sale in self._sales:
            sale_date = datetime.datetime.strptime(sale.purchase_date, "%Y-%m-%d")
            sale_date = sale_date.date()

            if start_date >= sale_date <= end_date:
                period_sales.append(sale)

        print('Sales for period: ', period_sales)
        # Create new instance of SalesReport
        sales_report = SalesReport(
            parent_view=self._parent_view,
            sales=period_sales,
            sales_period=[start_date, end_date],
            handle_back=self.__handle_back
        )

        # TODO: add report to the db
        # Add sales report to the list and then to the views
        self._sales_reports.append(sales_report)
        self._view.add_sales_report(sales_report)
        self.__open_subtab(sales_report)

    def __create_view(self):
        # It creates SalesReportTab view object
        self._view = SalesReportTab(
            parent_node=self._parent_view.center_panel,
            sales_months=self._period_dates,
            select_period=self.__handle_select_period,
            sales_reports=self._sales_reports,
            handle_open_report=self.__open_subtab
        )

        # add view to the parent view
        self._parent_view.sales_report_tab = self._view

    def __open_subtab(self, report_to_open):
        # Close view of SalesReports tab
        self._view.close()
        # Open subview
        self._current_sales_report = report_to_open
        self._current_sales_report.view.show()

    def __handle_back(self):
        # It closes details of given report and opens back main screen
        self._current_sales_report.view.close()
        self._current_sales_report = None

        self._view.show()
        self._view.render_reports()

    @property
    def view(self):
        return self._view
