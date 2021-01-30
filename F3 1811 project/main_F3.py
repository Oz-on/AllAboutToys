from Basket import *
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.title("BasketShopping")
    BasketCart(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
