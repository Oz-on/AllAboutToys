import tkinter.messagebox as tkm
import tkinter as tk
import tkinter.font as font  # This lets us use different fonts.
import Basket
import Receipt


# This is the class which introduces the Delivery options, their prices and theirs methods

class DeliveryOptions:

    def __init__(self):

        # Delivery options

        self.home_dlvr = "Delivery to the recipient's house address"
        self.postoffice_dlvr = "Delivery to the recipient's local post office"
        self.AATm_delvr = "Delivery to the recipient's nearest AAt market depot"

        # Delivery prices

        self.home_price = 7
        self.post_price = 5
        self.AATm_price = 3

        # Variable used to register the choice of the options
        # It has been registered 1 as default

        self.var = tk.IntVar(None, 1)

        # The cost of the option chosen

        self.returned_option = int()

    @property
    def get_var(self):

        return self.var

    @get_var.setter
    def get_var(self, x):

        self.var = x

    @classmethod
    def update_option(cls, option):
        cls.returned_option = option

    def get_home_d(self):

        return self.home_dlvr

    def get_post_d(self):

        return self.postoffice_dlvr

    def get_aatm_d(self):

        return self.AATm_delvr

    # This method will help the Check_out Window to choose the option wanted by the user

    def get_opt_result(self, vari):

        # take the price charge of the option selected

        if vari.get() == 1:

            charge_ = self.home_price

        elif vari.get() == 2:

            charge_ = self.post_price

        elif vari.get() == 3:

            charge_ = self.AATm_price

        return charge_

    # This method serves to make function the choice selection

    def sel(self, vari, label):

        self.var = vari
        print("choice option: ", self.var.get())
        select = self.var.get()

        selection = "You selected the option " + str(select)

        label.config(text=selection)

        setattr(DeliveryOptions, 'self.var', self.var)
        self.returned_option = self.get_opt_result(self.var)
        # setattr(p, 'name', 'John')
        setattr(DeliveryOptions, 'self.returned_option', self.returned_option)
        self.update_option(self.returned_option)
        print("\nself.returned option: ", str(self.returned_option))

    def showcost(self, label):
        c = self.returned_option
        label.config(text="By choosing this option you are charged of:   £" + str(c))

    def r_option(self):
        c = self.returned_option
        print("\nreturned option:", c)
        return c


class Payment(DeliveryOptions):

    # Here you need to retrieve the lists of the previous scripts and use it
    # First of all it's important to insert all the payment details of the user

    def __init__(self):

        DeliveryOptions.__init__(self)

        # Cardtypes used  for payment method
        self.cardtypes = ["VISA", "MASTERCARD", "PAYPAL", "AMEX"]

        # Cardholder name
        self.cholder = tk.StringVar()

        # User Account Number
        self.accnumber = tk.IntVar()

        # Card's cvv
        self.cvv = tk.IntVar()

        # Card's expiration date(Only the year)
        self.expirations = tk.IntVar()

        # Default selection for the radiobutton
        self.var_2 = tk.IntVar(None, 1)

        # Discount code
        self.voucher = tk.StringVar()

        # Index count
        self.count = 1

        # Cost decrease
        self.cost_decrease = None

        # Boolean Statements
        self.statement_1 = None
        self.statement_2 = None
        self.statement_3 = None

    @property
    def get_cholder(self):
        return self.cholder

    @get_cholder.setter
    def get_cholder(self, x):
        self.cholder = x

    @property
    def get_accnumber(self):
        return self.accnumber

    @get_accnumber.setter
    def get_accnumber(self, x):
        self.accnumber = x

    @property
    def get_cvv(self):
        return self.cvv

    @get_cvv.setter
    def get_cvv(self, x):
        self.cvv = x

    @property
    def get_expirations(self):
        return self.expirations

    @get_expirations.setter
    def get_expirations(self, x):
        self.expirations = x

    @property
    def get_var_2(self):
        return self.var_2

    @get_var_2.setter
    def get_var_2(self, x):
        self.var_2 = x

    @property
    def get_count(self):
        return self.count

    @get_count.setter
    def get_count(self, x):
        self.count = x

    @property
    def get_voucher(self):
        return self.voucher

    @property
    def get_cost_d(self):
        return self.cost_decrease

    @get_cost_d.setter
    def get_cost_d(self, x):
        self.cost_decrease = x

    # This method is similar to other method on the previous class, the aim is selection of a choice
    def selpay(self, var, label):

        self.var_2 = var
        print(self.var_2.get())
        select = self.var_2.get() + 1

        selection = "You selected the option " + str(select)

        label.config(text=selection)

    # This method will behave like a Visa controller and it will tell if there were any issue

    def save_verify(self, cardholder, accountnum, cvv, expdate, parent, nameslist, pricelist, tot_plist, qtylist):

        # verify the account number of the given credit card
        self.accnumber = accountnum.get()
        self.expirations = expdate.get()
        self.cholder = cardholder.get()
        self.cvv = cvv.get()
        self.cholder = cardholder.get()

        if self.luhnaccn() is True:
            print("The account number is correct\n")
            self.statement_1 = True

        else:
            tkm.showwarning("Error", "There is something wrong with the account number \nPlease try again :)")
            self.statement_1 = False

        if self.expcontr(self.expirations) is True:
            print("The expiration date is correct")
            self.statement_2 = True

        else:
            tkm.showwarning("Error Expiration", "Your expiration date is too old or is wrong\nPlease try again :D")
            self.statement_2 = False

        if self.cvvcontr(self.cvv):
            print(" is correct")
            self.statement_3 = True

        else:
            tkm.showwarning("Error", "Your cvv is wrong\nPlease try again :D")
            self.statement_3 = False

        db = Basket.Database('databasem.db')
        query = """INSERT OR REPLACE INTO CreditCard (Credit_ID, cardholder, account_number, cvv, expiration_date) VALUES (?, ?, ?, ?, ?);"""
        info = (self.count, self.cholder, self.accnumber, self.cvv, self.expirations)

        self.count = self.count + 1

        db.cursor.execute(query, info)

        data = db.connection.execute("select * from CreditCard")
        db.connection.commit()

        for row in data:
            print(row)
        self.count += 1

        print("Payment self returned option: ", str(self.returned_option))

        if self.statement_1:
            if self.statement_2:
                if self.statement_3:
                    db.connection.close()
                    Receipt.ReceiptUI(parent, nameslist, pricelist, tot_plist, qtylist, self.returned_option,
                                      self.cost_decrease)

    # To verify the account number it has been used the luhn algorithm

    def luhnaccn(self):

        # Number of digits ex: 4539869650133101

        ndigits = len(str(self.accnumber))

        # Digits

        digits = str(self.accnumber)

        nSum = 0
        isSecond = False

        if self.accnumber == 0:
            return False

        else:

            for i in range(ndigits - 1, -1, -1):

                # The ord() function returns the number representing the unicode code of a specified character

                d = ord(digits[i]) - ord('0')

                if isSecond == True:
                    d = d * 2

                # We add two digits to handle
                # cases that make two digits after
                # doubling
                nSum += d // 10
                nSum += d % 10

                isSecond = not isSecond

            if nSum % 10 == 0:
                return True

            else:
                return False

    # The following method, expiration control, will check if the expiration date is acceptable or not

    def expcontr(self, expirations):

        print(str(expirations))
        self.expirations = expirations

        if self.expirations >= 2021:
            if self.expirations <= 2031:
                return True
            else:
                return False
        else:
            return False

    # A cvv controller method

    def cvvcontr(self, cvv):

        self.cvv = cvv

        if len(str(cvv)) == 3:
            return True

        else:
            return False

    # As the method says it checks if the discount code is acceptable or not

    def check_discount(self, voucher):

        db = Basket.Database('databasem.db')

        vouchers_code = db.connection.execute("select discount_code from Voucher")
        voucher_rows = vouchers_code.fetchall()

        print(voucher_rows)

        voucher_rows, = zip(*voucher_rows)
        print(type(voucher_rows))

        t = list(voucher_rows)
        print(t)

        print("\n", str(voucher.get()))
        c = 0

        if voucher.get() in t:
            tkm.showinfo(title="Message", message="The voucher is being applied\n The price will be modified")
            voucher_cost_d = db.connection.execute("select cost_decrease from Voucher where discount_code = ?",
                                                   (voucher.get(),))
            cost_d_rows = voucher_cost_d.fetchone()
            l = list(cost_d_rows)

            self.cost_decrease = l[0]
        else:
            tkm.showinfo(title="Message", message="The voucher inserted is wrong")

        db.connection.commit()

# This class will create the window for the checkout and the payment

class Checkoutw(tk.Frame, Payment):

    def __init__(self, parent, names, price, tot_price, quantity):
        print("Checkout class \n")
        tk.Frame.__init__(self, parent)  # ADDED parent argument.
        Payment.__init__(self)

        self.nameslist = names
        self.price = price
        self.tot_p = tot_price
        self.qty = quantity

        # Creation of the Check_out Window
        # prova2.Database().get_connection().close

        self.parent = tk.Toplevel(parent)
        parent = self.parent
        # Creation of the title of the Window

        parent.title("Check_out")

        # Creation of the heading title frame

        parent.checkfh = tk.Frame(parent)
        parent.checkfh.pack()

        parent.fontb = font.Font(family="Helvetica", size=24, weight="bold")
        parent.header_lbl = tk.Label(parent.checkfh, text="--CHECK OUT--", font=parent.fontb)
        # prova2.FontStyle().get_fonth())  # getattr(prova2.FontStyle(), 'self.font_for_header'))

        parent.header_lbl.pack()

        # Define the checkbuttons for the delivery options and its frame

        # Define the delivery frame

        parent.del_f = tk.Frame(parent)

        parent.del_f.pack()

        parent.del_lbl = tk.Label(parent.del_f, text="Choose one of the three option",
                                  font=Basket.FontStyle().get_fonts())

        parent.del_lbl.pack()  # grid(row=3, column=0, padx=20, pady=15)

        #  Definition of Delivery option 1

        parent.del_opt_1 = tk.Radiobutton(parent.del_f, text=str(self.home_dlvr), font=Basket.FontStyle().get_fonts(),
                                          variable=self.var, value=1)

        parent.del_opt_1.pack(anchor=tk.W)  # grid(row=0, column=0, padx=20, pady=5)

        #  Definition of Delivery option 2

        parent.del_opt_2 = tk.Radiobutton(parent.del_f, text=str(self.postoffice_dlvr),
                                          font=Basket.FontStyle().get_fonts(),
                                          variable=self.var, value=2)

        parent.del_opt_2.pack(anchor=tk.W)  # .grid(row=1, column=0, padx=20, pady=5)

        #  Definition of Delivery option 3
        parent.del_opt_3 = tk.Radiobutton(parent.del_f, text=str(self.AATm_delvr), font=Basket.FontStyle().get_fonts(),
                                          variable=self.var, value=3)

        parent.del_opt_3.pack(anchor=tk.W)  # .grid(row=2, column=0, padx=20, pady=5)

        # Create a label where it displays the option you have chosen, and the price charged

        parent.lbl_conf = tk.Label(parent.del_f, text="Choose the option best for you",
                                   font=Basket.FontStyle().get_fonts())
        parent.lbl_conf.pack()

        # Under this options create a verify button to confirm which option you have chosen

        parent.opt_btn = tk.Button(parent.del_f, text="OK", command=lambda: self.sel(self.var, parent.lbl_conf))

        parent.opt_btn.pack(anchor=tk.W)
        # This value is very important because it needs to be calculate together with the rest

        parent.charge_lbl = tk.Label(parent.del_f,
                                     text="",
                                     # we need to implement the returned option variable/attribute
                                     font=Basket.FontStyle().get_fonts())
        parent.charge_lbl.pack()

        # Show_btn is a button served to show the cost of the option chosen:

        parent.show_btn = tk.Button(parent.del_f, text="Show Cost",
                                    command=lambda: self.showcost(parent.charge_lbl))
        parent.show_btn.pack(anchor=tk.NE)

        #  Creation of a new frame used for payment in which will be inserted the header and the entries

        parent.payment_f = tk.Frame(parent)

        parent.payment_f.pack()

        #  Creation of the header

        parent.payment_h = tk.Label(parent.payment_f, text="PAYMENT", font=Basket.FontStyle().get_fonth())
        parent.payment_h.grid(row=0, sticky="W")

        #   Creation of a subheading
        parent.payment_lbl_1 = tk.Label(parent.payment_f, text="Select Payment Method",
                                        font=Basket.FontStyle().get_fonts())
        parent.payment_lbl_1.grid(row=1, sticky="W")

        #  Creation of the radiobuttons for the methods of payment

        # Creation of label in which is inserted the chosen option of the method payment
        parent.payment_lbl_2 = tk.Label(parent.payment_f, text=("Choice default: " + str(self.var_2.get() + 1)),
                                        font=Basket.FontStyle().get_fonts())
        parent.payment_lbl_2.grid(row=2, sticky="W")
        # Definition of the second value

        parent.row_line = 3
        for cardtype in range(0, len(self.cardtypes)):
            val = cardtype
            tk.Radiobutton(parent.payment_f,
                           text=self.cardtypes[cardtype],
                           font=Basket.FontStyle().get_fontb(),
                           padx=20,
                           variable=self.var_2,
                           command=lambda: self.selpay(self.var_2, parent.payment_lbl_2),
                           value=val).grid(row=parent.row_line, sticky="W")
            parent.row_line += 1

        #  Creation of the label which tell to insert the payment details of the user(personal/payment detail of the user)

        parent.pdetail_lbl = tk.Label(parent.payment_f, text="Please insert your payment details",
                                      font=Basket.FontStyle().get_fonts())
        parent.pdetail_lbl.grid(row=10, sticky="W")

        #  Creation of labels and entries

        #  Cardholder label and entry

        parent.cholder_lbl = tk.Label(parent.payment_f, text="Cardholder", font=Basket.FontStyle().get_fonts())
        parent.cholder_lbl.grid(row=12, pady=20)

        parent.cholder_ent = tk.Entry(parent.payment_f, textvariable=self.cholder)
        parent.cholder_ent.grid(row=12, column=1)

        #  Account Number label and entry

        parent.accnumber_lbl = tk.Label(parent.payment_f, text="Account Number", font=Basket.FontStyle().get_fonts())
        parent.accnumber_lbl.grid(row=13)

        parent.accnumber_ent = tk.Entry(parent.payment_f, textvariable=self.accnumber)
        parent.accnumber_ent.grid(row=13, column=1)

        #  CVV information label and entry

        parent.cvv_lbl = tk.Label(parent.payment_f, text="CVV", font=Basket.FontStyle().get_fonts())
        parent.cvv_lbl.grid(row=14)

        parent.cvv_ent = tk.Entry(parent.payment_f, textvariable=self.cvv)
        parent.cvv_ent.grid(row=14, column=1)

        #  Expiration date info label and entry

        parent.exp_lbl = tk.Label(parent.payment_f, text="Expiration Date", font=Basket.FontStyle().get_fonts())

        parent.exp_lbl.grid(row=15)

        parent.exp_ent = tk.Entry(parent.payment_f, textvariable=self.expirations)
        parent.exp_ent.grid(row=15, column=1)

        # Creation of the discount entry and label

        parent.disc_f = tk.Frame(parent)
        parent.disc_f.pack()

        parent.disc_label = tk.Label(parent.disc_f, text="Voucher", font=Basket.FontStyle().get_fonts())
        parent.disc_label.pack()

        parent.disc_ent = tk.Entry(parent.disc_f, textvariable=self.voucher)
        parent.disc_ent.pack()

        parent.disc_btnc = tk.Button(parent.disc_f, text="Check", font=Basket.FontStyle().get_fonts(),
                                     command=lambda: self.check_discount(self.voucher))
        parent.disc_btnc.pack()

        #  Creation of the purchase button frame

        parent.purchase_f = tk.Frame(parent)
        parent.purchase_f.place(height=100, width=250)

        #  button definition

        parent.purchase_btn = tk.Button(parent.purchase_f, text="Complete Purchase",
                                        font=Basket.FontStyle().get_fontn(),
                                        command=lambda: self.save_verify(self.cholder, self.accnumber, self.cvv,
                                                                         self.expirations, self.parent, self.nameslist,
                                                                         self.price, self.tot_p, self.qty))
        parent.purchase_btn.pack()
        parent.state("zoomed")
        parent.mainloop()
