# Part 3
# COMP1811 AAT
# Kajen Vijeyaratnam Vigneswaran
# 001136158
# 4539869650133101 card account number
# import tkinter as tk  # This has all code for GUI
# import tkinter.font as font  # This lets us use different fonts.
from CheckWindow import *
import sqlite3


# This class is responsible of taking important data regarding the toys ordered by the user

class Database:

    # opening of a database connection, creates a new
    # database if it does not exist

    def __init__(self, name='databasem.db'):

        self._conn = sqlite3.connect(name)

        # getting of a cursor object. The cursor object
        # enables us to send SQL statements to SQLite

        self._cursor = self._conn.cursor()
        self.create_tables()

    """The __enter__ and __exit__ "magic methods" let a class use the 'with' statement.
       It's basically saying return an instantiated version of this class when
       it's used in a with DBase() as db: context."""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def create_tables(self):

        # Creation of the Product Table in the database if it doesn't exist

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS Products(product_ID INTEGER PRIMARY KEY, product_name text, price integer, quantity integer)")

        # Creation of the Voucher Table in the database if it doesn't exist

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS Voucher(voucher_ID INTEGER PRIMARY KEY, discount_code text, cost_decrease integer)")

        # Creation of the Personal payment details of the user

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS CreditCard(Credit_ID INTEGER PRIMARY KEY, cardholder text, account_number integer, cvv integer, expiration_date integer)")

        # Inserting the toys data

        self.connection.execute(
            "INSERT OR REPLACE INTO Products (product_ID, product_name, price, quantity) VALUES (1, 'Barbie Doll', 27, 2);")

        self.connection.execute(
            "INSERT OR REPLACE INTO Products (product_ID, product_name, price, quantity) VALUES (2, 'Car', 22, 4);")

        self.connection.execute(
            "INSERT OR REPLACE INTO Products (product_ID, product_name, price, quantity) VALUES (3, 'Lego House', 29, 1)")

        self.connection.execute(
            "INSERT OR REPLACE INTO Products (product_ID, product_name, price, quantity) VALUES (4, 'Yu-Gi-Oh!', 15, 7)")

        self.connection.execute(
            "INSERT OR REPLACE INTO Products (product_ID, product_name, price, quantity) VALUES (5, 'Pokemon Platinum DS', 60, 1)")

        self.connection.execute(
            "INSERT OR REPLACE INTO Products (product_ID, product_name, price, quantity) VALUES (6, 'Gameboy Advance', 17, 3)")

        # Inserting the Vouchers data

        self.connection.execute(
            "INSERT OR REPLACE INTO Voucher (voucher_ID, discount_code, cost_decrease) VALUES (1, 'outlet5', 5);")

        self.connection.execute(
            "INSERT OR REPLACE INTO Voucher (voucher_ID, discount_code, cost_decrease) VALUES (2, 'outlet20', 20);")

        self.connection.execute(
            "INSERT OR REPLACE INTO Voucher (voucher_ID, discount_code, cost_decrease) VALUES (3, 'alwaysplay10', 10);")

        self.connection.commit()

        print("Records inserted successfully")

        self.data = self.connection.execute("select * from Products")

        # Using .fetchall() returns a list of results so that you have them stored locally before you re-use the cursor

        self.data = self.data.fetchall()

        # COMMIT method sends a COMMIT statement to the MySQL server, committing the current transaction

        self.connection.commit()

    def register_list(self, position):

        list_ = list()
        for row in self.data:
            list_.append(row[position])

        """print("position: ", str(position))""
        "print(list_)"""

        return list_


# This class is responsible for the sales of the market so to output every data of the database

class Product:

    def __init__(self):

        db = Database("databasem.db")

        # The position of the row is important, because it defines the id, name, price and quantity

        self.position_ID = 0

        self.position_name = 1

        self.position_price = 2

        self.position_quantity = 3

        # Get the toy's info through the register_list method

        # Id list

        self.row_ID = db.register_list(self.position_ID)

        # name list

        self.row_name = db.register_list(self.position_name)

        # price list

        self.row_price = db.register_list(self.position_price)

        # quantity list

        self.row_quantity = db.register_list(self.position_quantity)

        # total price list

        self.tot_p = self.obtain_tot_p()

    def get_name(self):

        return self.row_name

    def get_price(self):

        return self.row_price

    def get_quantity(self):

        return self.row_quantity

    # This function serves to increase the quantity of a toy

    def add_qty(self, qty, index, label):

        # Get the database info

        db = Database('databasem.sqlite')
        # db = Database('db_file.sqlite)
        # Increase the quantity value

        self.row_quantity[index] = qty + 1

        # Update the Database

        sql_update_query = """Update Products set quantity = ? where product_ID  = ?"""
        info = (self.row_quantity[index], self.row_ID[index])
        db.cursor.execute(sql_update_query, info)
        db.connection.commit()

        print(self.row_quantity[index])

        # Label update

        label.grid_forget()
        label.config(text=str(self.row_quantity[index]))
        print("quantity: " + str(self.row_quantity[index]))
        print("indice:" + str(index))
        label.grid(row=index + 1, column=3, padx=10, pady=5)

    # This function serves to increase the quantity of a toy

    def less_qty(self, qty, index, label):

        # Get the database info

        db = Database('databasem.db')

        # The if statement is needed in case the quantity doesn't go to negative values

        if qty >= 2:
            # Decrease the quantity value

            self.row_quantity[index] = qty - 1

            # Update the Database

            sql_update_query = """Update Products set quantity = ? where product_ID  = ?"""
            info = (self.row_quantity[index], self.row_ID[index])
            db.cursor.execute(sql_update_query, info)
            db.connection.commit()

            print(self.row_quantity[index])

            # Update the label

            label.grid_forget()
            label.config(text=str(self.row_quantity[index]))
            print("quantity: " + str(self.row_quantity[index]))
            print("indice:" + str(index))
            label.grid(row=index + 1, column=3, padx=10, pady=5)
            print(self.row_quantity)

    # This method is used to obtains the total cost of the toys

    def obtain_tot_p(self):

        tot_p = list()
        for i in range(0, len(self.row_price)):
            tot_p.append(self.row_price[i] * self.row_quantity[i])

        return tot_p

    # The function will update the labels of total costs of the toys

    def refresh_cost(self, label):

        tot_p = self.obtain_tot_p()
        for i in range(0, len(self.row_price)):
            t = i
            label[i].grid_forget()
            label[i].config(text="£ " + str(tot_p[i]))
            label[i].grid(row=t + 1, column=2, padx=10, pady=5)

    # This method will remove one product entirely

    def delete_prod(self, name_lbl, price_lbl, totp_lbl, quantity_lbl, position, add_btn, less_btn, remove_btn):

        db = Database('databasem.db')
        # The labels are removed from the window page

        name_lbl.destroy()

        price_lbl.destroy()

        price_lbl.destroy()

        totp_lbl.destroy()

        quantity_lbl.destroy()

        add_btn.destroy()

        less_btn.destroy()

        remove_btn.destroy()

        # The removed toys will be replaced by 0 or None in this way the functions of the list will not be compromised

        for i in range(0, len(self.row_name)):

            if i == position:
                self.row_name[i] = "None"

        for i in range(0, len(self.row_price)):

            if i == position:
                self.row_price[i] = 0

        for i in range(0, len(self.row_quantity)):

            if i == position:
                self.row_quantity[i] = 0

        x = self.row_name
        y = self.row_price
        z = self.row_quantity

        setattr(Product, 'self.row_name', x)
        setattr(Product, 'self.row_price', y)
        setattr(Product, 'self.row_quantity', z)

        for i in range(0, len(self.row_name)):
            if self.row_name[i] is None:
                db.connection("DELETE FROM Products WHERE product_id = ?", (self.row_ID[i]))
                db.connection.commit()


class FontStyle:

    def __init__(self):
        # Definition of the style for each sentence inside the windows

        # Font for header

        self.font_for_header = font.Font(family='Georgia', size='24', weight='bold')

        # Font for normal words

        self.font_normal = font.Font(family='Georgia', size='15', weight='bold')

        # For for small words

        self.font_small = font.Font(family='Georgia', size='12', weight='normal')

        # For highlighted words

        self.font_bold = font.Font(family="Helvetica", size='13', weight="bold")

        # For highlighted small words

        self.font_sbold = font.Font(family="Helvetica", size='11', weight="bold")

        # For highlighted big words

        self.font_bbold = font.Font(family="Helvetica", size='20', weight="bold")

    # Get the three fonts

    def get_fonth(self):
        return self.font_for_header

    def get_fontn(self):
        return self.font_normal

    def get_fonts(self):
        return self.font_small

    def get_fontb(self):
        return self.font_bold

    def get_fontbs(self):
        return self.font_sbold

    def get_fontbb(self):
        return self.font_bbold


# This class is mainly used for implementation of the methods needed in order to make the code more manageable

class BasketCartUI(tk.Frame, FontStyle, Product):

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)
        FontStyle.__init__(self)
        Product.__init__(self)

    # Create labels function serves to create the list of the product's features

    # t_list stands for toys list

    # Column t(toys) stands for the three characteristics of the products: name, price, and quantity

    def create_lbls(self, frameb, t_list, column_t, c_num):

        for i in range(0, len(column_t)):
            t = i
            t_list.append(tk.Label(frameb, text=str(column_t[i]), font=self.font_small))
            t_list[i].grid(row=t + 1, column=c_num, padx=10, pady=5)

    # Create buttons function serves to create the buttons for modifying the content of the window in this case for the add and the less btns

    def create_btns(self, function, qty, frameb, t_list, btn_list, word, c_num):

        for i in range(0, len(t_list)):
            t = i
            btn_list.append(tk.Button(frameb, text=word, font=self.font_small,
                                      command=lambda i=i: function(qty[i], i, t_list[i])))

            btn_list[i].grid(row=t + 1, column=c_num, padx=10, pady=5)

    # Creation of the delete btn method

    def remove_btnm(self, function, l_name, l_price, l_totp, l_qty, l_lessbtn, l_addbtn, l_delbtn, frameb, word_rem,
                    c_num):

        for i in range(0, len(l_name)):
            t = i
            l_delbtn.append(tk.Button(frameb, text=word_rem, font=self.font_small,
                                      command=lambda i=i: function(l_name[i], l_price[i], l_totp[i], l_qty[i], i,
                                                                   l_addbtn[i], l_lessbtn[i], l_delbtn[i])))

            l_delbtn[i].grid(row=t + 1, column=c_num, padx=10, pady=5)


# This class is responsible of applying the implementation of the previous class

class BasketCart(BasketCartUI):

    def __init__(self, parent):
        BasketCartUI.__init__(self, parent)

        self.parent = parent
        parent.headerf = tk.Frame(parent)
        parent.headerf.pack()
        parent.lblh = tk.Label(parent.headerf, text="SHOPPING BASKET", font=self.font_for_header)
        parent.lblh.pack()

        # definition of the basket list frame

        parent.basketlistF = tk.Frame(parent)
        parent.basketlistF.pack()

        # Definition of the columns for product name, product price and the stock quantity of the product

        product_lbl = tk.Label(parent.basketlistF, text="Product name:", font=self.font_normal)
        price_lbl = tk.Label(parent.basketlistF, text="Price:", font=self.font_normal)
        quantity_lbl = tk.Label(parent.basketlistF, text="QTY:", font=self.font_normal)
        totprice_lbl = tk.Label(parent.basketlistF, text="TOT Price:", font=self.font_normal)

        product_lbl.grid(row=0, column=0, padx=20, pady=5)
        price_lbl.grid(row=0, column=1, padx=20, pady=5)
        quantity_lbl.grid(row=0, column=3, padx=20, pady=5)
        totprice_lbl.grid(row=0, column=2, padx=20, pady=5)

        # Introduce the info of the product_name received from the DB class

        # c_num is the position in which the label need to be inserted

        list_prod_name = list()

        self.create_lbls(parent.basketlistF, list_prod_name, self.row_name, c_num=0)

        # Introduce the info of the product_price received from the DB class

        list_prod_price = list()
        self.create_lbls(parent.basketlistF, list_prod_price, self.row_price, c_num=1)

        # Introduce the info of the total price of a product per quantity

        list_tot_price = list()
        self.tot_p = self.obtain_tot_p()

        for i in range(0, len(self.row_price)):
            t = i
            list_tot_price.append(tk.Label(parent.basketlistF, text="£ " + str(self.tot_p[i]), font=self.font_small))
            list_tot_price[i].grid(row=t + 1, column=2, padx=10, pady=5)

        # Introduce the info of the product_quantity received from the DB class

        list_prod_quantity = list()
        self.create_lbls(parent.basketlistF, list_prod_quantity, self.row_quantity, c_num=3)

        # Definition of the add button for the quantity of the products

        list_add_btn = list()
        word_add = " + "

        self.create_btns(self.add_qty, self.row_quantity, parent.basketlistF,
                         list_prod_quantity, list_add_btn, word_add, c_num=4)

        # Definition of the less button for the quantity of the products

        list_less_btn = list()
        word_less = " - "

        self.create_btns(self.less_qty, self.row_quantity, parent.basketlistF,
                         list_prod_quantity, list_less_btn, word_less, c_num=5)

        # Define a refresh button in order to adjust the number calculated

        self.refresh_root = tk.Button(parent.basketlistF, text='Refresh the Total Prices', font=self.font_small,
                                      command=lambda: self.refresh_cost(list_tot_price))

        self.refresh_root.grid(row=12, column=2, pady=10)

        # Definition of the check-out button/frame

        parent.checkoutF = tk.Frame(parent)
        parent.checkoutF.pack()
        parent.check_btn = tk.Button(parent.checkoutF, text="Check out", font=self.font_normal,
                                     command=lambda: Checkoutw(parent, self.row_name, self.row_price, self.tot_p,
                                                               self.row_quantity))

        parent.check_btn.grid(row=13, column=2, pady=10)

        # Definition of the delete item/product button/Frame
        delete_btn = list()
        word_rem = " X "
        self.remove_btnm(
            self.delete_prod, list_prod_name, list_prod_price, list_tot_price, list_prod_quantity,
            list_less_btn, list_add_btn, delete_btn, parent.basketlistF, word_rem, c_num=7)

