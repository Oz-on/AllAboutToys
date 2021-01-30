#   In this file we are going to build the receipt ui, so other than its structure, the file receipt will be stored in a file for printing
# Two objectives: display and save the receipt created
import datetime
import tkinter as tk
import Basket
import tkinter.filedialog as tkf


# This class will form the receipt window

class ReceiptUI(tk.Frame):

    def __init__(self, parent, names_list, prices_list, tot_p_list, qty_list, r_option, cost_d):
        tk.Frame.__init__(self, parent)

        self.names = names_list
        self.prices = prices_list
        self.tot_price = tot_p_list
        self.qtys_list = qty_list
        self.returned_opt = r_option
        self.percentage = cost_d
        self.text = tk.StringVar()
        # Initialization of the receipt window

        self.parent = tk.Toplevel(parent)
        parent = self.parent

        #  title of the root receipt
        parent.title("Receipt of AAT")

        # Create a frame for the first part of the receipt window

        parent.rcpt_f1 = tk.Frame(parent)
        parent.rcpt_f1.pack(anchor=tk.W)

        # Definition of the subtitle

        parent.rcpt_lbl = tk.Label(parent.rcpt_f1, text="ALL ABOUT Toys", font=Basket.FontStyle().get_fontbb())
        parent.rcpt_lbl.pack(anchor=tk.W)

        # Create the part for bill to , ship to, and receipt info

        parent.rcpt_f2 = tk.Frame(parent)
        parent.rcpt_f2.pack()
        # First row

        # bill to

        parent.bill_lbl = tk.Label(parent.rcpt_f2, text="Bill to", font=Basket.FontStyle().get_fontbs())
        parent.bill_lbl.grid(row=0, column=0, pady=10, padx=30)

        # ship to

        parent.ship_lbl = tk.Label(parent.rcpt_f2, text="Ship to", font=Basket.FontStyle().get_fontbs())
        parent.ship_lbl.grid(row=0, column=1, pady=10, padx=30)

        # Receipt ID

        parent.rcptinfo_lbl = tk.Label(parent.rcpt_f2, text="RECEIPT ID:", font=Basket.FontStyle().get_fontbs())
        parent.rcptinfoans_lbl = tk.Label(parent.rcpt_f2, text="2345-QAZSEF", font=Basket.FontStyle().get_fonts())
        parent.rcptinfo_lbl.grid(row=0, column=2, pady=10, padx=30)
        parent.rcptinfoans_lbl.grid(row=0, column=3, pady=10, padx=30)

        # Second row

        # Bill place

        parent.billplace_lbl = tk.Label(parent.rcpt_f2, text="To AAT National Store",
                                        font=Basket.FontStyle().get_fonts())
        parent.billplace_lbl.grid(row=1, column=0, pady=10, padx=30)

        # Ship place

        parent.shipaddr_lbl = tk.Label(parent.rcpt_f2,
                                       text="User choice's address ", font=Basket.FontStyle().get_fonts())  # Risolvere il tama
        parent.shipaddr_lbl.grid(row=1, column=1, pady=10, padx=30)

        # Receipt date

        parent.rcptdate_lbl = tk.Label(parent.rcpt_f2, text="RECEIPT DATE:", font=Basket.FontStyle().get_fontbs())
        parent.rcptdateans_lbl = tk.Label(parent.rcpt_f2, text=str(datetime.datetime.today().strftime('%x')),
                                          font=Basket.FontStyle().get_fonts())  # This is why I've imported datetime
        parent.rcptdate_lbl.grid(row=1, column=2, pady=10, padx=30)
        parent.rcptdateans_lbl.grid(row=1, column=3, pady=10, padx=30)

        # Create the second part of the window

        parent.rcpt_f3 = tk.Frame(parent)
        parent.rcpt_f3.pack()

        # Create the main content of the receipt

        parent.rcpt_title = tk.Label(parent.rcpt_f3, text="RECEIPT TOTAL\t", font=Basket.FontStyle().get_fontbb())
        parent.rcpt_title.pack(anchor=tk.W)

        # Retrieve the total cost:

        parent.rcpt_f4 = tk.Frame(parent)
        parent.rcpt_f4.pack()

        self.total_cost = self.calc_cost()
        print("Receipt: Total cost: ", str(self.total_cost))
        parent.rcpt_price = tk.Label(parent.rcpt_f4,
                                     text="£" + str(self.total_cost),
                                     font=Basket.FontStyle().get_fontbb())
        parent.rcpt_price.pack(anchor=tk.S)

        # Create the third part of the window: Will describe what you have brought and all the info needed

        parent.rcpt_f5 = tk.Frame(parent)
        parent.rcpt_f5.pack()

        # Creation of the info toys labels

        product_lbl = tk.Label(parent.rcpt_f5, text="Product name:", font=Basket.FontStyle().get_fontb())
        price_lbl = tk.Label(parent.rcpt_f5, text="Price:", font=Basket.FontStyle().get_fontb())
        quantity_lbl = tk.Label(parent.rcpt_f5, text="QTY:", font=Basket.FontStyle().get_fontb())
        totprice_lbl = tk.Label(parent.rcpt_f5, text="TOT Price:", font=Basket.FontStyle().get_fontb())

        product_lbl.grid(row=0, column=0, padx=20, pady=5)
        price_lbl.grid(row=0, column=1, padx=20, pady=5)
        quantity_lbl.grid(row=0, column=3, padx=20, pady=5)
        totprice_lbl.grid(row=0, column=2, padx=20, pady=5)

        # Create the list labels for the toys

        parent.list_name = list()
        parent.list_price = list()
        parent.list_total_price = list()
        parent.list_quantity = list()

        # you need the following values to make the function work: self, frameb, t_list, column_b, c_num

        # Retrieve the BasketCartUI class

        p = Basket.BasketCartUI(parent)

        # Use the create labels function

        p.create_lbls(parent.rcpt_f5, parent.list_name, self.names, c_num=0)
        p.create_lbls(parent.rcpt_f5, parent.list_price, self.prices, c_num=1)
        p.create_lbls(parent.rcpt_f5, parent.list_total_price, self.tot_price, c_num=2)
        p.create_lbls(parent.rcpt_f5, parent.list_quantity, self.qtys_list, c_num=3)

        parent.rcpt_f6 = tk.Frame(parent)
        parent.rcpt_f6.pack()

        # Definition of the button that will save the file receipt for printing

        parent.save_btn = tk.Button(parent.rcpt_f6, text="Save for printing", font=Basket.FontStyle().get_fonts(),
                                    command=lambda: self.file_save())
        parent.save_btn.pack()

        parent.state("zoomed")
        parent.mainloop()

    # This method will calculate the total price of everything purchased by the user

    def calc_cost(self):
        sum_ = 0

        if self.percentage is None:

            for i in range(0, len(self.tot_price)):
                sum_ += self.tot_price[i]

            tot_sum = sum_ + self.returned_opt

            print(tot_sum)

        else:

            for i in range(0, len(self.tot_price)):
                sum_ += self.tot_price[i]

            cost_d = self.percentage / 100

            partial_sum = sum_ * cost_d

            sum_ = sum_ - partial_sum

            tot_sum = sum_ + self.returned_opt

            print(tot_sum)

        return tot_sum

    # This method will save a file that will be used eventually for printing

    def file_save(self):

        f = tkf.asksaveasfile(mode='w', defaultextension=".txt")
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return

        text2save = self.generate_text()
        f.write(text2save)
        f.close()

    # This method is connected to the previous one and it generate the text for the receipt file

    def generate_text(self):
        text = "Toys:\t" + str(self.names) + "\nQty:\t" + str(self.qtys_list) + "\nPrice:\t" + str(self.prices) + \
               "\nTotal Price:\t" + str(self.total_cost) + "\nReceipt ID:\t" + "2345-QAZSEF" + "\nReceipt Date:\t" + \
               str(datetime.datetime.today().strftime('%x'))
        return text
