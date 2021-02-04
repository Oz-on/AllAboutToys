# Author: Oskar Domingos
# This file contains controllers for features related to Discounts schemes

from tkinter import messagebox
from SalesFeature.interfaces import TabControllerInterface
from SalesFeature.Discounts.models import DiscountScheme
from SalesFeature.Discounts.views import DiscountSchemesTabUI, DiscountSchemesDetails, DiscountSchemesCreationPanel


class DiscountsTab(TabControllerInterface):
    def __init__(self, parent_view, database):
        self._database = database
        self._parent_view = parent_view

        # Get request from database
        self._discounts_schemes = database.fetch_discounts_schemes()

        self._current_subview_opened = None
        self._current_discount_scheme = None

        self.__create_view()

    def __create_view(self):
        self._view = DiscountSchemesTabUI(
            parent_node=self._parent_view.center_panel,
            discounts=self._discounts_schemes,
            handle_open_discount=self.__open_subtab,
            handle_remove_discount=self.__remove_discount_scheme,
            handle_open_creation_panel=self.__open_creation_panel,
        )

        self._parent_view.discounts_tab = self._view

    def __open_subtab(self, discount_scheme):
        self._view.close()

        self._current_discount_scheme = discount_scheme
        self._current_subview_opened = DiscountSchemesDetails(
            parent_node=self._parent_view.center_panel,
            handle_back=self.__handle_back,
            discount=self._current_discount_scheme,
        )

        self._current_subview_opened.show()

    def __remove_discount_scheme(self, discount_scheme):
        # Remove scheme from database
        self._database.remove_discount_scheme(discount_scheme)

        # Remove scheme from list
        self._discounts_schemes = list(filter(
            lambda scheme: discount_scheme.discount_scheme_id != scheme.discount_scheme_id,
            self._discounts_schemes
        ))

        #  Update previews
        self._view.update_previews(self._discounts_schemes)

    def __create_discount_scheme(self, discount_scheme_id, details, discount_percentage):
        discount_scheme = DiscountScheme(
            discount_scheme_id=discount_scheme_id,
            details=details,
            discount_percentage=discount_percentage
        )
        # Add new scheme to the database
        success = self._database.add_discount_scheme(discount_scheme)

        if success:
            self._discounts_schemes.append(discount_scheme)
            self._view.update_previews(self._discounts_schemes)
            self.__handle_back()

        else:
            messagebox.showinfo(message=f'Discount scheme with id {discount_scheme_id} already exists')

    def __handle_back(self):
        self._current_subview_opened.close()
        self._current_subview_opened = None
        self._current_discount_scheme = None
        self._view.show()

    def __open_creation_panel(self):
        self._current_subview_opened = DiscountSchemesCreationPanel(
            parent_node=self._parent_view.center_panel,
            handle_back=self.__handle_back,
            handle_create_discount_scheme=self.__create_discount_scheme
        )
        self._current_subview_opened.show()

    @property
    def view(self):
        return self._view
