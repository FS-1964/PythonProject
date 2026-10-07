import datetime
import os

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry
from Modules.games import tictactoe
from Modules.weather import analyzer
from Modules.weather import weatherforecast


class AnalyzerGUI:
    def __init__(self):

        # self.on_game_finished = None
        # self.select_csv = None
        self.chart_combo = None
        self.chart_var = None
        self.score_label = None
        self.game_container = None
        self.game = None
        self.score_x = 0
        self.score_o = 0
        self.score_draw = 0

        self.start_btn = None
        self.info_label = None
        self.label_text = None
        #  self.ana = analyzer(filename, path, fileformat)
        # self.df = self.ana.calculate_totals()
        self.country_coords = {
            "Deutschland": (52.52, 13.40),  # Berlin
            "Österreich": (48.2082, 16.3738),  # Wien
            "Schweiz": (47.37, 8.54),  # Zürich
            "Iran": (35.68, 51.41),  # Teheran
            "USA": (40.71, -74.00),  # New York
            "Tokio": (35.68, 139.69),  # Tokio
            "New York": (40.7306, 73.9352)
        }

        self.window = tk.Tk()
        self.window.title("Dashboard Analyzer")
        self.window.geometry("1000x700")
        self.enddate = ""

        # ---------------------------------------------------------
        # TABS
        # ---------------------------------------------------------
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill="both", expand=True)

        # Sales Tab
        self.sales_tab = tk.Frame(notebook)
        notebook.add(self.sales_tab, text="Sales")

        # Weather Tab
        self.weather_tab = tk.Frame(notebook)
        notebook.add(self.weather_tab, text="Weather")

        # Games Tab
        self.games_tab = tk.Frame(notebook)
        notebook.add(self.games_tab, text="Games")

        # ---------------------------------------------------------
        # SALES TAB CONTENT (scrollbar + charts + text)
        # ---------------------------------------------------------
        self.build_sales_tab()

        # ---------------------------------------------------------
        # WEATHER TAB CONTENT
        # ---------------------------------------------------------
        self.build_weather_tab()

        # ---------------------------------------------------------
        # SYSTEM TAB CONTENT
        # ---------------------------------------------------------
        self.build_system_tab()

        self.window.mainloop()

    def show_selected_chart(self):
        # Chart-Bereich leeren
        for widget in self.sales_chart_frame.winfo_children():
            widget.destroy()

        choice = self.chart_var.get()

        if choice == "Gesamtumsatz pro Produkt":
            fig = self.ana.visualize_totals(self.df)

        elif choice == "Gesamtumsatz pro Datum":
            fig = self.ana.visualize_total_by_date(self.df)

        elif choice == "Produktumsatz pro Datum":
            fig = self.ana.visualize_product_total_by_date(self.df)

        elif choice == "Gestapelter Umsatz pro Datum":
            fig = self.ana.visualize_stacked(self.df)

        # Diagramm einbetten
        self.embed_chart(self.sales_chart_frame, fig)

    # ---------------------------------------------------------
    # SALES TAB
    # ---------------------------------------------------------

    def enable_dark_mode(self):
        style = ttk.Style()
        style.theme_use("clam")

        dark_bg = "#373E44"
        dark_fg = "#ffffff"
        accent = "#3a7bd5"

        style.configure(".", background=dark_bg, foreground=dark_fg)
        style.configure("TFrame", background=dark_bg)
        style.configure("TLabel", background=dark_bg, foreground=dark_fg)
        style.configure("TButton", background=accent, foreground=dark_fg, padding=6)
        style.map("TButton", background=[("active", "#5596e6")])
        style.configure("TCombobox", fieldbackground="#2a2a2a", foreground=dark_fg)

    def create_card(self, parent, title, bg):
        card = tk.Frame(parent, bg=bg, highlightthickness=0)
        tk.Label(card, text=title, bg=bg, fg="white", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        return card

    def build_sales_tab(self):
        self.enable_dark_mode()

        # Canvas + Scrollbar
        canvas = tk.Canvas(self.sales_tab, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.sales_tab, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Frame im Canvas
        frame = ttk.Frame(canvas)

        # ⭐ Fenster-ID speichern, damit wir die Breite anpassen können
        frame_id = canvas.create_window((0, 0), window=frame, anchor="nw")

        # ⭐ Canvas-Breite immer anpassen → rechter Leerraum verschwindet
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(frame_id, width=e.width))

        # Scrollbereich aktualisieren
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Mausrad aktivieren
        self.bind_mousewheel(frame, canvas)

        # Responsive Layout
        frame.grid_columnconfigure(0, weight=1)

        # Titel
        ttk.Label(frame, text="Sales Dashboard", font=("Arial", 20, "bold")).grid(row=0, column=0, pady=15)

        # Card 1 – CSV Optionen
        card_csv = self.create_card(frame, "CSV Optionen", "#373E44")
        card_csv.grid(row=1, column=0, sticky="ew", padx=15, pady=10)

        ttk.Button(card_csv, text="CSV auswählen", command=self.select_csv).pack(fill="x", pady=5)
        ttk.Button(card_csv, text="CSV anzeigen", command=lambda: self.show_csv(frame)).pack(fill="x", pady=5)

        # Card 2 – Diagramm Auswahl
        card_chart = self.create_card(frame, "Diagramm Auswahl", "#373E44")
        card_chart.grid(row=2, column=0, sticky="ew", padx=15, pady=10)

        self.chart_var = tk.StringVar()
        self.chart_combo = ttk.Combobox(card_chart, foreground="#111111", textvariable=self.chart_var, state="readonly")
        self.chart_combo['values'] = [
            "Gesamtumsatz pro Produkt",
            "Gesamtumsatz pro Datum",
            "Produktumsatz pro Datum",
            "Gestapelter Umsatz pro Datum"
        ]
        self.chart_combo.current(0)
        self.chart_combo.pack(fill="x", pady=5)

        ttk.Button(card_chart, text="Diagram anzeigen", command=self.show_selected_chart).pack(fill="x", pady=10)

        # Card 3 – Ausgabe
        card_output = self.create_card(frame, "Ausgabe", bg="#373E44")

        card_output.grid(row=3, column=0, sticky="nsew", padx=15, pady=10)
        frame.grid_rowconfigure(3, weight=1)

        self.sales_output = scrolledtext.ScrolledText(card_output, height=10)
        self.sales_output.pack(fill="both", expand=True)

        # Card 4 – Chart
        card_chart_area = self.create_card(frame, "Diagramm", "#373E44")
        card_chart_area.grid(row=4, column=0, sticky="nsew", padx=15, pady=10)
        frame.grid_rowconfigure(4, weight=1)

        self.sales_chart_frame = ttk.Frame(card_chart_area)
        self.sales_chart_frame.pack(fill="both", expand=True)

    def show_weather(self):
        country = self.country_var.get()
        lat, lon = self.country_coords[country]

        weather_df = self.weathercaster(lat, lon)

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, weather_df.to_string())

    def country_data_dark(self, parent, bg, fg):
        # Frame oben kompakter
        frame = tk.Frame(parent, bg=bg)
        frame.pack(fill="x", padx=10, pady=(0, 5))  # oben 0px Abstand, unten 5px

        # Label kompakter
        tk.Label(
            frame,
            text="Land auswählen:",
            font=("Arial", 12),
            bg=bg,
            fg=fg
        ).pack(anchor="w", pady=(0, 2))

        self.country_var = tk.StringVar()
        self.country_combo = ttk.Combobox(
            frame,
            textvariable=self.country_var,
            state="readonly",
            width=25
        )
        self.country_combo['values'] = [
            "Deutschland",
            "Österreich",
            "Schweiz",
            "Iran",
            "USA",
            "Japan",
            "New York"
        ]
        self.country_combo.current(0)
        self.country_combo.pack(fill="x", pady=(0, 5))

        tk.Label(frame, text="Startdatum:", font=("Arial", 12), bg=bg, fg=fg).pack(anchor="w", pady=(0, 2))

        current_year = 2026
        self.start_date = DateEntry(
            frame,
            date_pattern="yyyy-mm-dd",
            mindate=datetime.date(current_year, 1, 1),
            maxdate=datetime.date(current_year, 12, 31),
            width=12
        )
        self.start_date.pack(fill="x", pady=(0, 5))

        tk.Label(frame, text="Enddatum:", font=("Arial", 12), bg=bg, fg=fg).pack(anchor="w", pady=(0, 2))

        self.label_text = tk.StringVar()
        tk.Label(frame, textvariable=self.label_text, font=("Arial", 10), fg="lightblue", bg=bg).pack(anchor="w",
                                                                                                      pady=(0, 5))

        ttk.Button(frame, text="Wetter anzeigen", command=self.show_weather_dashboard).pack(fill="x", pady=(5, 10))

    # ---------------------------------------------------------
    # WEATHER TAB
    # ---------------------------------------------------------

    def get_date_interval(self):
        start = self.start_date.get_date()
        end = start + datetime.timedelta(days=14)
        self.enddate = end.strftime("%Y-%m-%d")
        self.label_text.set(f"{end.strftime('%Y-%m-%d')}")
        # Sicherstellen: Enddatum bleibt im aktuellen Jahr
        last_day = datetime.date(start.year, 12, 31)

        if end > last_day:
            end = last_day

        return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


    def build_weather_tab(self):
        self.enable_dark_mode()

        # Farben für Dark Mode
        dark_bg = "#373E44"
        dark_fg = "#ffffff"
        card_bg = "#373E44"

        # Überschrift
        tk.Label(
            self.weather_tab,
            text="Weather Dashboard",
            font=("Arial", 18),
            bg=dark_bg,
            fg=dark_fg
        ).grid(row=0, column=0, columnspan=2, pady=10)

        # Hintergrund des Tabs
        self.weather_tab.configure(bg=dark_bg)

        # Spaltenbreiten
        self.weather_tab.grid_columnconfigure(0, weight=4)
        self.weather_tab.grid_columnconfigure(1, weight=1)
        self.weather_tab.grid_rowconfigure(1, weight=1)

        # Canvas + Scrollbar
        canvas = tk.Canvas(self.weather_tab, bg=dark_bg, highlightthickness=0)

        scrollbar = ttk.Scrollbar(self.weather_tab, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

        # Inhalt im Canvas
        frame = tk.Frame(canvas, bg=dark_bg)
        frame_id = canvas.create_window((0, 0), window=frame, anchor="nw")

        # Canvas-Breite anpassen
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(frame_id, width=e.width))

        # Scrollbereich aktualisieren
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Mousewheel
        self.bind_mousewheel(frame, canvas)

        # Country UI (Dark Mode)
        self.country_data_dark(frame, dark_bg, dark_fg)

        # Wetter-Ausgabe
        self.weather_output = scrolledtext.ScrolledText(
            frame,
            height=10,
            bg=card_bg,
            fg=dark_fg,
            insertbackground=dark_fg
        )
        self.weather_output.pack(fill="both", expand=True, padx=20, pady=10)

        # Chart Frame
        self.weather_chart_frame = tk.Frame(frame, bg=card_bg)
        self.weather_chart_frame.pack(fill="both", expand=True, padx=20, pady=10)




    def start_tictactoe(self):

        # Button deaktivieren
        self.start_btn.config(state="disabled")
        # altes Spielfeld löschen
        for widget in self.game_container.winfo_children():
            widget.destroy()

        # neues Spielfeld in den Container
        self.game = tictactoe(self.game_container, self.on_game_finished)

    # tictactoe(game_frame)
    def on_game_finished(self, winner):
        if winner == "X":
            self.score_x += 1
        elif winner == "O":
            self.score_o += 1
        else:
            self.score_draw += 1

            # Scoreboard aktualisieren
        self.score_label.config(text=self.get_score_text())

        # Start-Button wieder aktivieren
        self.start_btn.config(state="normal")

    def get_score_text(self):
        return f"X: {self.score_x}   O: {self.score_o}   Unentschieden: {self.score_draw}"

    # ---------------------------------------------------------
    # Games TAB
    # ---------------------------------------------------------
    def build_system_tab(self):
        tk.Label(self.games_tab, text="Games", font=("Arial", 18)).pack(pady=10)

        info = tk.Label(self.games_tab, text="TicTacToe", font=("Arial", 14))
        info.pack(pady=20)

        self.start_btn = tk.Button(
            self.games_tab,
            text="Spiel starten",
            font=("Arial", 14),
            command=self.start_tictactoe
        )
        self.start_btn.pack(pady=10)

        # ⭐ SCOREBOARD – jetzt sichtbar
        self.score_label = tk.Label(
            self.games_tab,
            text=self.get_score_text(),
            font=("Arial", 14),
            fg="blue"
        )
        self.score_label.pack(pady=10)  # <-- DIE FEHLENDE ZEILE

        # Spielfeld-Container
        self.game_container = tk.Frame(self.games_tab)
        self.game_container.pack(pady=20)

    def get_score_text(self):
        return f"X: {self.score_x}   O: {self.score_o}   Unentschieden: {self.score_draw}"

    def add_chart_row(self, parent, fig_left, fig_right):
        row = tk.Frame(parent)
        row.pack(fill="both", expand=True)

        left = tk.Frame(row)
        left.pack(side="left", fill="both", expand=True)

        right = tk.Frame(row)
        right.pack(side="left", fill="both", expand=True)

        self.embed_chart(left, fig_left)
        self.embed_chart(right, fig_right)

    # ---------------------------------------------------------
    # WEATHER DASHBOARD
    # ---------------------------------------------------------

    def weathercaster(self, lat, lon):
        # Land aus Combobox holen
        country = self.country_var.get()

        # Koordinaten aus Mapping holen
        lat, lon = self.country_coords[country]
        startdate, enddate = self.get_date_interval()
        # WeatherForecast erzeugen
        wf = weatherforecast(
            latitude=str(lat),
            longitude=str(lon),
            startdate=startdate,
            enddate=enddate,
            city=country
        )

        # Diagramm erzeugen
        fig = wf.visualize_weather_forecast()

        # Textausgabe speichern
        self.wdf = wf.print_weather_forecast()
        self.weather_output.delete("1.0", tk.END)
        self.weather_output.insert(tk.END, self.wdf.to_string())

        return fig

    def show_weather_dashboard(self):
        for widget in self.weather_chart_frame.winfo_children():
            widget.destroy()
        country = self.country_var.get()
        lat, lon = self.country_coords[country]
        fig = self.weathercaster(lat, lon)
        self.embed_chart(self.weather_chart_frame, fig)

    # ---------------------------------------------------------
    # CSV OUTPUT
    # ---------------------------------------------------------
    def show_csv(self, frame):
        self.sales_output.delete("1.0", tk.END)
        self.sales_output.insert(tk.END, self.df.to_string())

    # ---------------------------------------------------------
    # CHART EMBEDDING
    # ---------------------------------------------------------
    def embed_chart(self, parent, fig):
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True, padx=10, pady=10)

        # Chart automatisch verkleinern, wenn TabPage kleiner ist
        widget.bind("<Configure>", lambda event: widget.config(width=event.width))

    def bind_mousewheel(self, widget, canvas):
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        widget.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        widget.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel"))

    def select_csv(self):
        filepath = filedialog.askopenfilename(
            title="CSV-Datei auswählen",
            filetypes=[("CSV Dateien", "*.csv"), ("Alle Dateien", "*.*")]
        )

        if not filepath:
            return  # Benutzer hat abgebrochen

        try:
            ext = os.path.splitext(filepath)[1].lower().replace(".", "")
            # Analyzer neu laden
            self.ana = analyzer("", filepath, ext)
            self.df = self.ana.calculate_totals()

            # Ausgabe aktualisieren
            self.sales_output.delete("1.0", tk.END)
            # self.sales_output.insert(tk.END, f"CSV geladen:\n{filepath}\n\n")
            # self.sales_output.insert(tk.END, self.df.to_string())

            # Charts zurücksetzen
            for widget in self.sales_chart_frame.winfo_children():
                widget.destroy()

        except Exception as e:
            self.sales_output.delete("1.0", tk.END)
            self.sales_output.insert(tk.END, f"Fehler beim Laden der Datei:\n{e}")
