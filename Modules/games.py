import chess
from stockfish import Stockfish
import tkinter as tk
from tkinter import messagebox
import random
import time
from tkinter import simpledialog


class MemoryGame:

    def __init__(self, parent):
        self.ranking_var = None
        self.moves = 0
        self.matches = 0
        self.highscores = []
        self.start_time = time.time()
        self.timer_running = True
        self.parent = parent
        self.games_won = 0
        self.best_moves = None
        self.best_time = None
        self.symbols = [
            "🍎", "🍎",
            "🍌", "🍌",
            "🍇", "🍇",
            "🍓", "🍓",
            "🍒", "🍒",
            "🍍", "🍍",
            "🥝", "🥝",
            "🍉", "🍉"
        ]

        random.shuffle(self.symbols)

        self.buttons = []

        self.first_card = None
        self.second_card = None

        self.moves = 0
        self.matches = 0
        self.best_time_seconds = None

        self.build_ui()

    # ----------------------------
    # UI
    # ----------------------------

    def build_ui(self):

        self.main_frame = tk.Frame(self.parent)
        self.main_frame.pack(fill="both", expand=True)

        tk.Label(
            self.main_frame,
            text="Memory",
            font=("Arial", 18, "bold")
        ).pack(pady=10)
        self.score_var = tk.StringVar()
        self.score_var.set(self.get_score_text())

        tk.Label(
            self.main_frame,
            textvariable=self.score_var,
            font=("Arial", 10, "bold"),
            fg="blue"
        ).pack(pady=5)
        self.info_var = tk.StringVar()
        self.info_var.set("Züge: 0")

        self.time_var = tk.StringVar()
        self.time_var.set("Zeit: 00:00")

        tk.Label(
            self.main_frame,
            textvariable=self.time_var,
            font=("Arial", 12)
        ).pack()

        tk.Label(
            self.main_frame,
            textvariable=self.info_var,
            font=("Arial", 12)
        ).pack()

        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.pack(pady=10)

        index = 0

        for row in range(4):

            row_buttons = []

            for col in range(4):
                btn = tk.Button(
                    self.board_frame,
                    text="?",
                    width=6,
                    height=3,
                    font=("Arial", 16),
                    command=lambda i=index: self.card_click(i)
                )

                btn.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5
                )

                row_buttons.append(btn)

                index += 1

            self.buttons.append(row_buttons)
        self.ranking_var = tk.StringVar()
        self.ranking_var.set("Noch keine Einträge")

        tk.Label(
            self.main_frame,
            text="🏆 Rangliste",
            font=("Arial", 12, "bold")
        ).pack(pady=(10, 0))

        tk.Label(
            self.main_frame,
            textvariable=self.ranking_var,
            justify="left",
            font=("Consolas", 10)
        ).pack()
        tk.Button(
            self.main_frame,
            text="Neues Spiel",
            command=self.reset_game
        ).pack(pady=10)

        self.update_timer()

    def get_score_text(self):

        best_moves = (
            str(self.best_moves)
            if self.best_moves is not None
            else "-"
        )

        best_time = (
            self.best_time
            if self.best_time is not None
            else "--:--"
        )

        return (
            f"Gewonnen: {self.games_won}    "
            f"Beste Züge: {best_moves}    "
            f"Beste Zeit: {best_time}"
        )

    def update_ranking(self):

        if not self.highscores:
            self.ranking_var.set("Noch keine Einträge")
            return

        text = ""

        for idx, entry in enumerate(self.highscores, start=1):
            text += (
                f"{idx:2}. "
                f"{entry['name']:<12} "
                f"{entry['moves']:>3} ZZüge "
                f"{entry['time']}\n"
            )

        self.ranking_var.set(text)

    # ----------------------------
    # Kartenklick
    # ----------------------------
    def update_timer(self):

        if not self.timer_running:
            return

        elapsed = int(time.time() - self.start_time)

        minutes = elapsed // 60
        seconds = elapsed % 60

        self.time_var.set(
            f"Zeit: {minutes:02}:{seconds:02}"
        )

        self.main_frame.after(
            1000,
            self.update_timer
        )

    def card_click(self, index):

        if self.second_card:
            return

        row = index // 4
        col = index % 4

        button = self.buttons[row][col]

        if button["text"] != "?":
            return

        button["text"] = self.symbols[index]

        if self.first_card is None:
            self.first_card = index
            return

        self.second_card = index

        self.moves += 1

        self.info_var.set(
            f"Züge: {self.moves}"
        )

        self.main_frame.after(
            700,
            self.check_cards
        )

    # ----------------------------
    # Karten prüfen
    # ----------------------------

    def check_cards(self):

        first_symbol = self.symbols[self.first_card]
        second_symbol = self.symbols[self.second_card]

        row1 = self.first_card // 4
        col1 = self.first_card % 4

        row2 = self.second_card // 4
        col2 = self.second_card % 4

        btn1 = self.buttons[row1][col1]
        btn2 = self.buttons[row2][col2]

        if first_symbol == second_symbol:

            btn1.config(state="disabled")
            btn2.config(state="disabled")

            self.matches += 1

            if self.matches == 8:

                self.timer_running = False

                elapsed = int(time.time() - self.start_time)

                minutes = elapsed // 60
                seconds = elapsed % 60

                time_string = f"{minutes:02}:{seconds:02}"

                name = simpledialog.askstring(
                    "Rangliste",
                    "Name eingeben:"
                )

                if not name:
                    name = "Spieler"

                self.highscores.append({
                    "name": name,
                    "moves": self.moves,
                    "time": time_string,
                    "seconds": elapsed
                })

                # Nach Zeit sortieren
                self.highscores.sort(
                    key=lambda x: (x["seconds"], x["moves"])
                )

                # Top 10 behalten
                self.highscores = self.highscores[:10]

                self.update_ranking()

                messagebox.showinfo(
                    "Gewonnen",
                    f"Gratulation {name}!\n\n"
                    f"Züge: {self.moves}\n"
                    f"Zeit: {time_string}"
                )


        else:

            btn1.config(text="?")
            btn2.config(text="?")

        self.first_card = None
        self.second_card = None

    # ----------------------------
    # Reset
    # ----------------------------

    def reset_game(self):

        random.shuffle(self.symbols)

        self.first_card = None
        self.second_card = None

        self.moves = 0
        self.matches = 0

        self.info_var.set("Züge: 0")

        for row in self.buttons:
            for btn in row:
                btn.config(
                    text="?",
                    state="normal"
                )

        self.start_time = time.time()
        self.timer_running = True

        self.update_timer()
        self.reset_scoreboard()
        self.reset_ranking()

    def reset_ranking(self):

        self.highscores.clear()

        self.update_ranking()

    def reset_scoreboard(self):

        self.games_won = 0
        self.best_moves = None
        self.best_time = None
        self.best_time_seconds = None

        self.score_var.set(
            self.get_score_text()
        )


class tictactoe:
    def __init__(self, root, finished_callback=None):
        self.root = root
        self.frame = None
        self.finished_callback = finished_callback
        self.brett = self.erstelle_brett()
        self.aktuelle_spieler = "X"

        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.spielfeld_erstellen()

    def erstelle_brett(self):
        return [[" " for _ in range(3)] for _ in range(3)]

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
        self.brett = self.erstelle_brett()
        self.aktuelle_spieler = "X"
        for z in range(3):
            for s in range(3):
                self.buttons[z][s].config(text=" ")


class ChessGame:

    def __init__(self, parent):

        self.parent = parent

        self.board = chess.Board()

        self.selected_square = None

        self.buttons = {}

        self.stockfish = Stockfish(
            path=r"C:\Dev\Stockfish\stockfish-windows-x86-64-universal.exe"
        )

        # 0-20
        self.stockfish.set_skill_level(10)

        self.status_var = tk.StringVar()
        self.status_var.set("Weiß am Zug")

        self.square_size = 40

        self.build_ui()

        self.update_board()

    # --------------------------------------------------------
    # UI
    # --------------------------------------------------------

    def build_ui(self):

        self.main_frame = tk.Frame(self.parent)
        self.main_frame.pack(fill="both", expand=True)

        tk.Label(
            self.main_frame,
            text="Schach gegen Stockfish",
            font=("Arial", 16, "bold")
        ).pack(pady=5)

        tk.Label(
            self.main_frame,
            textvariable=self.status_var,
            font=("Arial", 11)
        ).pack(pady=5)

        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.pack()

        self.create_board()

        control_frame = tk.Frame(self.main_frame)
        control_frame.pack(pady=10)

        tk.Label(
            control_frame,
            text="Stärke:"
        ).pack(side="left", padx=5)

        self.skill_var = tk.IntVar(value=10)

        tk.Scale(
            control_frame,
            from_=0,
            to=20,
            orient="horizontal",
            variable=self.skill_var
        ).pack(side="left")

        tk.Button(
            control_frame,
            text="Neues Spiel",
            command=self.reset_game
        ).pack(side="left", padx=10)

    # --------------------------------------------------------
    # Brett
    # --------------------------------------------------------

    def create_board(self):

        for row in range(8):
            self.board_frame.grid_rowconfigure(
                row,
                minsize=self.square_size
            )

        for col in range(8):
            self.board_frame.grid_columnconfigure(
                col,
                minsize=self.square_size
            )

        for row in range(8):
            for col in range(8):
                square = chess.square(
                    col,
                    7 - row
                )
                # "#B58863"
                color = (
                    "#FFFFFF"
                    if (row + col) % 2 == 0
                    else "#B58863"
                )

                button = tk.Button(
                    self.board_frame,
                    text="",
                    font=("Arial", 14),
                    bg=color,
                    relief="flat",
                    command=lambda sq=square: self.on_square_click(sq)
                )

                button.grid(
                    row=row,
                    column=col,
                    sticky="nsew"
                )

                self.buttons[square] = button

    # --------------------------------------------------------
    # Unicode Figuren
    # --------------------------------------------------------

    @staticmethod
    def piece_symbol(piece):

        symbols = {
            'P': '♙',
            'R': '♖',
            'N': '♘',
            'B': '♗',
            'Q': '♕',
            'K': '♔',
            'p': '♟',
            'r': '♜',
            'n': '♞',
            'b': '♝',
            'q': '♛',
            'k': '♚'
        }

        return symbols.get(
            piece.symbol(),
            ""
        )

    # --------------------------------------------------------
    # Brett aktualisieren
    # --------------------------------------------------------

    def update_board(self):

        for square, button in self.buttons.items():

            piece = self.board.piece_at(square)

            if piece:
                button.config(
                    text=self.piece_symbol(piece)
                )
            else:
                button.config(text="")

        if self.board.turn:
            self.status_var.set("Weiß am Zug")
        else:
            self.status_var.set("Stockfish denkt...")

    # --------------------------------------------------------
    # Farben
    # --------------------------------------------------------

    def restore_colors(self):

        for row in range(8):
            for col in range(8):
                square = chess.square(
                    col,
                    7 - row
                )

                color = (
                    "#F0D9B5"
                    if (row + col) % 2 == 0
                    else "#B58863"
                )

                self.buttons[square].config(
                    bg=color
                )

    # --------------------------------------------------------
    # Klick
    # --------------------------------------------------------

    def on_square_click(self, square):

        # Mensch spielt nur Weiß
        if not self.board.turn:
            return

        if self.selected_square is None:

            piece = self.board.piece_at(square)

            if piece and piece.color == chess.WHITE:
                self.selected_square = square

                self.buttons[square].config(
                    bg="yellow"
                )

            return

        source = self.selected_square

        self.restore_colors()

        move = chess.Move(
            source,
            square
        )

        piece = self.board.piece_at(source)

        # Bauernumwandlung
        if piece and piece.piece_type == chess.PAWN:

            rank = chess.square_rank(square)

            if rank == 7:
                move = chess.Move(
                    source,
                    square,
                    promotion=chess.QUEEN
                )

        if move in self.board.legal_moves:

            self.board.push(move)

            self.update_board()

            self.check_game_end()

            if not self.board.is_game_over():
                self.parent.after(
                    400,
                    self.computer_move
                )

        self.selected_square = None

    # --------------------------------------------------------
    # Stockfish
    # --------------------------------------------------------

    def computer_move(self):

        if self.board.is_game_over():
            return

        self.stockfish.set_skill_level(
            self.skill_var.get()
        )

        self.stockfish.set_fen_position(
            self.board.fen()
        )

        best_move = self.stockfish.get_best_move()

        if best_move:
            move = chess.Move.from_uci(
                best_move
            )

            self.board.push(move)

            self.update_board()

            self.check_game_end()

    # --------------------------------------------------------
    # Spielende
    # --------------------------------------------------------

    def check_game_end(self):

        if self.board.is_checkmate():
            winner = (
                "Weiß"
                if not self.board.turn
                else "Schwarz"
            )

            messagebox.showinfo(
                "Schachmatt",
                f"{winner} gewinnt!"
            )

            return

        if self.board.is_stalemate():
            messagebox.showinfo(
                "Patt",
                "Unentschieden"
            )

            return

        if self.board.is_check():
            side = (
                "Weiß"
                if self.board.turn
                else "Schwarz"
            )

            self.status_var.set(
                f"{side} steht im Schach"
            )

    # --------------------------------------------------------
    # Reset
    # --------------------------------------------------------

    def reset_game(self):

        self.board.reset()

        self.selected_square = None

        self.restore_colors()

        self.update_board()
