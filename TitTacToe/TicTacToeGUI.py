import tkinter as tk
from tkinter import messagebox
class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        self.brett = self.erstelle_brett()
        self.aktuelle_spieler = "X"

        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.spielfeld_erstellen()

    def erstelle_brett():
        return [[" " for _ in range(3)] for _ in range(3)]

    def check_winner(brett, spieler):
        # Reihen
        for z in range(3):
            if brett[z][0] == brett[z][1] == brett[z][2] == spieler:
                return True
        # Spalten
        for s in range(3):
            if brett[0][s] == brett[1][s] == brett[2][s] == spieler:
                return True
        # Diagonalen
        if brett[0][0] == brett[1][1] == brett[2][2] == spieler:
            return True
        if brett[0][2] == brett[1][1] == brett[2][0] == spieler:
            return True
        return False

    def check_remie(brett):
        for zeile in brett:
            if " " in zeile:
                return False
        return True
    def spielfeld_erstellen(self):
        frame = tk.Frame(self.root, bg="black")
        frame.pack()

        for z in range(3):
            for s in range(3):
                btn = tk.Button(
                    frame,
                    text=" ",
                    font=("Arial", 32, "bold"),
                    width=4,
                    height=1,
                    bg="#e0e0e0",
                    activebackground="#c0c0c0",
                    command=lambda zeile=z, spalte=s: self.klick(zeile, spalte)
                )
                btn.grid(row=z, column=s, padx=5, pady=5)
                self.buttons[z][s] = btn

    def klick(self, zeile, spalte):
        if self.brett[zeile][spalte] != " ":
            return  # Feld schon belegt

        # Setze Zeichen
        self.brett[zeile][spalte] = self.aktuelle_spieler
        self.buttons[zeile][spalte].config(text=self.aktuelle_spieler)

        # Gewinner?
        if self.check_winner(self.brett, self.aktuelle_spieler):
            messagebox.showinfo("Spielende", f"Spieler {self.aktuelle_spieler} hat gewonnen!")
            self.reset()
            return

        # Remis?
        if self.check_remie(self.brett):
            messagebox.showinfo("Spielende", "Unentschieden!")
            self.reset()
            return

        # Spieler wechseln
        self.aktuelle_spieler = "O" if self.aktuelle_spieler == "X" else "X"

    def reset(self):
        self.brett = self.erstelle_brett()
        self.aktuelle_spieler = "X"
        for z in range(3):
            for s in range(3):
                self.buttons[z][s].config(text=" ")