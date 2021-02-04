# Author: Oskar Domingos


class DiscountScheme:
    def __init__(self, discount_scheme_id, details, discount_percentage):
        self._discount_scheme_id = discount_scheme_id
        self._details = details
        self._discount_percentage = discount_percentage

    @property
    def discount_scheme_id(self):
        return self._discount_scheme_id

    @property
    def details(self):
        return self._details

    @details.setter
    def details(self, new_details):
        self._details = new_details

    @property
    def discount_percentage(self):
        return self._discount_percentage

    @discount_percentage.setter
    def discount_percentage(self, new_percentage):
        self._discount_percentage = new_percentage
