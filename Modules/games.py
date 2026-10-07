import tkinter as tk
from tkinter import messagebox


def erstelle_brett():
    return [[" " for _ in range(3)] for _ in range(3)]


class tictactoe:
    def __init__(self, root, finished_callback=None):
        self.root = root
        self.frame = None
        self.finished_callback = finished_callback
        self.brett = erstelle_brett()
        self.aktuelle_spieler = "X"

        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.spielfeld_erstellen()

    def check_winner(self, brett, spieler):
        for z in range(3):
            if brett[z][0] == brett[z][1] == brett[z][2] == spieler:
                return True
        for s in range(3):
            if brett[0][s] == brett[1][s] == brett[2][s] == spieler:
                return True
        if brett[0][0] == brett[1][1] == brett[2][2] == spieler:
            return True
        if brett[0][2] == brett[1][1] == brett[2][0] == spieler:
            return True
        return False

    def check_remie(self, brett):
        for zeile in brett:
            if " " in zeile:
                return False
        return True

    def spielfeld_erstellen(self):
        # altes Spielfeld löschen
        if self.frame is not None:
            self.frame.destroy()

        self.frame = tk.Frame(self.root, bg="black")  # <-- FIX
        self.frame.pack()

        for z in range(3):
            for s in range(3):
                btn = tk.Button(
                    self.frame,  # jetzt korrekt!
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
            return

        self.brett[zeile][spalte] = self.aktuelle_spieler
        self.buttons[zeile][spalte].config(text=self.aktuelle_spieler)

        if self.check_winner(self.brett, self.aktuelle_spieler):
            messagebox.showinfo("Spielende", f"Spieler {self.aktuelle_spieler} hat gewonnen!")
            winner = self.aktuelle_spieler
            self.reset()
            if self.finished_callback:
                self.finished_callback(winner)
            return

        if self.check_remie(self.brett):
            messagebox.showinfo("Spielende", "Unentschieden!")
            self.reset()
            if self.finished_callback:
                self.finished_callback("draw")
            return

        self.aktuelle_spieler = "O" if self.aktuelle_spieler == "X" else "X"

    def reset(self):
        self.brett = erstelle_brett()
        self.aktuelle_spieler = "X"
        for z in range(3):
            for s in range(3):
                self.buttons[z][s].config(text=" ")
