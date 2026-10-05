import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry

from Modules.games import tictactoe
from Modules.weather import analyzer
from Modules.weather import weatherforecast
class AnalyzerGUI:
    def __init__(self,filename,path,fileformat):

        self.info_label = None
        self.label_text = None
        self.ana = analyzer(filename,path,fileformat)


        self.df = self.ana.calculate_totals()

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
        self.window.geometry("1200x700")
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

    # ---------------------------------------------------------
    # SALES TAB
    # ---------------------------------------------------------
    def build_sales_tab(self):
        canvas = tk.Canvas(self.sales_tab)
        scrollbar = tk.Scrollbar(self.sales_tab, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Buttons
        tk.Label(frame, text="Sales Dashboard", font=("Arial", 18)).pack(pady=10)

        tk.Button(frame, text="Dashboard anzeigen", command=self.show_sales_dashboard).pack(fill="x", padx=20, pady=5)
        tk.Button(frame, text="CSV anzeigen", command=lambda: self.show_csv(frame)).pack(fill="x", padx=20, pady=5)

        # Output text
        self.sales_output = scrolledtext.ScrolledText(frame, height=10)
        self.sales_output.pack(fill="both", expand=True, padx=20, pady=10)

        # Chart area
        self.sales_chart_frame = tk.Frame(frame)
        self.sales_chart_frame.pack(fill="both", expand=True)

    def show_weather(self):
        country = self.country_var.get()
        lat, lon = self.country_coords[country]

        weather_df = self.weathercaster(lat, lon)

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, weather_df.to_string())

    def country_data(self):
        frame = tk.Frame(self.weather_tab)
       # frame.pack(fill="x", padx=10, pady=10)
        frame.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

        self.info_label = tk.Label(frame, textvariable=self.label_text, font=("Arial", 12))
        self.info_label.pack(side="left", padx=10, pady=3)
        # --- Combobox für Länder ---
        tk.Label(frame, text="Land auswählen:", font=("Arial", 12)).pack(anchor="w", pady=3)

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
        self.country_combo.pack(fill="x", pady=3)
        # --- Kalender für Startdatum ---
        tk.Label(frame, text="Startdatum:", font=("Arial", 12)).pack(anchor="w", pady=3)


        current_year = 2026

        self.start_date = DateEntry(
            frame,
            date_pattern="yyyy-mm-dd",
            mindate=datetime.date(current_year, 1, 1),
            maxdate=datetime.date(current_year, 12, 31),
            width=12
        )

        self.start_date.pack(fill="x", pady=3)
        # --- Enddatum (Label + dynamischer Text) ---
        tk.Label(frame, text="Enddatum:", font=("Arial", 12)).pack(anchor="w", pady=3)

        self.label_text = tk.StringVar()
        self.label_text.set("")
        self.info_label = tk.Label(
            frame,
            textvariable=self.label_text,
            font=("Arial", 10),
            fg="blue"
        )
        self.info_label.pack(anchor="w", pady=3)


        # --- Wetter Button ---
        tk.Button(frame, text="Wetter anzeigen", command=self.show_weather_dashboard).pack(fill="x", pady=10)

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
        # Überschrift
        tk.Label(self.weather_tab, text="Weather Dashboard", font=("Arial", 18)) \
            .grid(row=0, column=0, columnspan=2, pady=10)

        # Spaltenbreiten: Canvas ~80%, rechte Spalte ~20%
        self.weather_tab.grid_columnconfigure(0, weight=4)  # Canvas
        self.weather_tab.grid_columnconfigure(1, weight=1)  # rechte Seite / Reserve
        self.weather_tab.grid_rowconfigure(1, weight=1)
        # Canvas + Scrollbar
        canvas = tk.Canvas(self.weather_tab)
        scrollbar = tk.Scrollbar(self.weather_tab, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

        # Inhalt im Canvas
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.country_data()

        self.weather_output = scrolledtext.ScrolledText(frame, height=10)
        self.weather_output.pack(fill="both", expand=True, padx=20, pady=10)

        self.weather_chart_frame = tk.Frame(frame)
        self.weather_chart_frame.pack(fill="both", expand=True)



    def start_tictactoe(self):
        game_frame = tk.Frame(self.games_tab)
        game_frame.pack(pady=20)

        tictactoe(game_frame)

    # ---------------------------------------------------------
    # Games TAB
    # ---------------------------------------------------------
    def build_system_tab(self):
        tk.Label(self.games_tab, text="Games", font=("Arial", 18)).pack(pady=10)

        info = tk.Label(self.games_tab, text="TicTacToe", font=("Arial", 14))
        info.pack(pady=20)
        start_btn = tk.Button(
            self.games_tab,
            text="Spiel starten",
            font=("Arial", 14),
            command=self.start_tictactoe
        )
        start_btn.pack(pady=10)

    # ---------------------------------------------------------
    # SALES DASHBOARD
    # ---------------------------------------------------------
    def show_sales_dashboard(self):
        # Chart-Bereich leeren
        for widget in self.sales_chart_frame.winfo_children():
            widget.destroy()

        # ---------------------------------------------------------
        # ROW 1 – zwei Charts nebeneinander
        # ---------------------------------------------------------
        row1 = tk.Frame(self.sales_chart_frame)
        row1.pack(fill="both", expand=True)

        left1 = tk.Frame(row1)
        left1.pack(side="left", fill="both", expand=True)

        right1 = tk.Frame(row1)
        right1.pack(side="left", fill="both", expand=True)

        fig1 = self.ana.visualize_totals(self.df)
        self.embed_chart(left1, fig1)

        fig2 = self.ana.visualize_total_by_date(self.df)
        self.embed_chart(right1, fig2)

        # ---------------------------------------------------------
        # ROW 2 – zwei Charts nebeneinander
        # ---------------------------------------------------------
        row2 = tk.Frame(self.sales_chart_frame)
        row2.pack(fill="both", expand=True)

        left2 = tk.Frame(row2)
        left2.pack(side="left", fill="both", expand=True)

        right2 = tk.Frame(row2)
        right2.pack(side="left", fill="both", expand=True)

        fig3 = self.ana.visualize_product_total_by_date(self.df)
        self.embed_chart(left2, fig3)

        fig4 = self.ana.visualize_stacked(self.df)
        self.embed_chart(right2, fig4)

    # ---------------------------------------------------------
    # WEATHER DASHBOARD
    # ---------------------------------------------------------


    def weathercaster(self,lat,lon):
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
        fig = self.weathercaster(lat,lon)
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
