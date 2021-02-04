# Author: Oskar Domingos
# This file contains classes related to SalesReports which are models for data


class Category:
    def __init__(self, category_id, name):
        self._id = category_id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name


class Product:
    def __init__(self, product_id, name, cost, category):
        self._id = product_id
        self._name = name
        self._cost = cost
        self._category = Category(category['id'], category['name'])

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def cost(self):
        return self._cost

    @property
    def category(self):
        return self._category


class Sale:
    def __init__(self, sale_id, product, purchase_date, quantity):
        self._id = sale_id
        self._product = Product(product['id'], product['name'], product['cost'], product['category'])
        self._purchase_date = purchase_date
        self._quantity = quantity

        self._total = self._product.cost * self._quantity

    @property
    def product(self):
        return self._product

    @property
    def purchase_date(self):
        return self._purchase_date

    @property
    def quantity(self):
        return self._quantity

    @property
    def total(self):
        return self._total

