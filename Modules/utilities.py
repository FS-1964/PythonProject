import tkinter as tk
from Modules.games import tictactoe
import time
from random import randint
from datetime import datetime


class helper:
    def __init__(self, filename, path, fileformat):
        self.path = path
        self.filename = filename
        self.fileformat = fileformat

    def calculate_total(quantity, price):
        """Calculate total for a single item"""
        return quantity * price

    def format_currency(amount):
        """Format number as currency"""
        return f"${amount:,.2f}"

    def startticktacktoe(self):
        root = tk.Tk()
        app = tictactoe(root)
        root.mainloop()

    def zufallgame(self):
        counter = 0
        while True:
            zufallzahl = randint(1, 100)
            counter = counter + 1
            time.sleep(1)
            print(datetime.now().strftime("%H:%M:%S"))
            if counter == 20:
                print(counter, "-", zufallzahl, "exit by 20")
                print("total generated Random number is", counter)
                break
            elif zufallzahl % 2 == 0:
                print(counter, "-", zufallzahl, "is divisible by 2")
            elif zufallzahl % 2 != 0:
                print(counter, "-", zufallzahl, "is divisible by 1")

    def addieren(*zahlen):
        return sum(zahlen)
