# Main file of our application
# Here we will initialise core widgets of application as well as whole app

#  Documentation of Tkinter can be found here: https://docs.python.org/3/library/tkinter.html

from tkinter import *
import tkinter as ttk
from SalesFeature.ui import WorkersPanel

# Set up the main application window
root = Tk()
root.title('All About Toys')
root.minsize(1024, 720)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Add worker's panel
# WorkersPanel(root)

# Start event loop and display program
root.mainloop()
