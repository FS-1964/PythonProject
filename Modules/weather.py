import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import messagebox
from Modules.utilities import helper

import json


class weatherexporter:
    def __init__(self, latitude, longitude, city, startdate, enddate):
        self.latitude = latitude
        self.longitude = longitude
        self.city = city
        self.startdate = startdate
        self.enddate = enddate

    def get_weather_forecast(self):
        url = (
            "https://api.open-meteo.com/v1/forecast?"
            f"latitude={self.latitude}&longitude={self.longitude}"
            f"&start_date={self.startdate}&end_date={self.enddate}"
            "&daily=temperature_2m_max,temperature_2m_min"
        )
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def convert_to_dataframe(self, data):
        daily = data["daily"]

        df = pd.DataFrame({
            "date": daily["time"],
            "temp_max": daily["temperature_2m_max"],
            "temp_min": daily["temperature_2m_min"]
        })

        # WICHTIG: Komma als Dezimaltrennzeichen für Excel
        df["temp_max"] = df["temp_max"].astype(str).str.replace(".", ",")
        df["temp_min"] = df["temp_min"].astype(str).str.replace(".", ",")

        return df

    def save_csv(self, df):
        os.makedirs("weather-forcast/weatherdata", exist_ok=True)
        path = f"weather-forcast/weatherdata/{self.city}_weather.csv"

        df.to_csv(path, index=False, sep=";", encoding="utf-8")
        print(f"Data saved to {path}")
        return path

    def export_to_csv(self):
        weather_data = self.get_weather_forecast()
        df = self.convert_to_dataframe(weather_data)
        path = self.save_csv(df)
        return path


class weatherforecast:

    def __init__(self, latitude, longitude, startdate, enddate, city):
        self.latitude = latitude
        self.longitude = longitude
        self.startdate = startdate
        self.enddate = enddate
        self.city = city

    def get_weather_forecast(self):
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={self.latitude}&longitude={self.longitude}"
            f"&start_date={self.startdate}&end_date={self.enddate}"
            f"&daily=temperature_2m_max,temperature_2m_min"
        )
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # HTTP-Fehler abfangen

            data = response.json()  # JSON-Fehler abfangen
            return data

        except requests.exceptions.Timeout:
            messagebox.showerror(f"Timeout Error",
                                 "❌ Fehler: Die Anfrage an Open-Meteo hat zu lange gedauert (Timeout).")
            return None

        except requests.exceptions.ConnectionError:
            messagebox.showerror(f"Connection Error", "❌ Fehler: Keine Internetverbindung oder API nicht erreichbar.")
            return None

        except requests.exceptions.HTTPError as e:
            messagebox.showerror(f"HTTP Error", f"❌ HTTP-Fehler: {e}[change the startdate]")
            return None

        except ValueError:
            messagebox.showerror(f"Response value Error", "❌ Fehler: Die API hat ein ungültiges JSON zurückgegeben.")
            return None

        except Exception as e:
            messagebox.showerror(f"Unknown Error", f"❌ Error", f"Unerwarteter Fehler: {e}")
            return None

    def extract_weather_forecast(self):
        data = self.get_weather_forecast()
        daily_data = data["daily"]

        df = pd.DataFrame({
            "date": daily_data["time"],
            "max_temp": daily_data["temperature_2m_max"],
            "min_temp": daily_data["temperature_2m_min"]
        })

        df["date"] = pd.to_datetime(df["date"])

        return df

    def print_weather_forecast(self):
        df = self.extract_weather_forecast()
        df["max_temp"] = df["max_temp"].apply(lambda x: f"{x}°C")
        df["min_temp"] = df["min_temp"].apply(lambda x: f"{x}°C")
        print(df)
        return df

    def visualize_weather_forecast(self):
        df = self.extract_weather_forecast()

        fig, ax = plt.subplots(figsize=(6, 4))

        ax.plot(df['date'], df['max_temp'], marker='o', label='Max Temp')
        ax.plot(df['date'], df['min_temp'], marker='o', label='Min Temp')

        ax.set_xlabel('Date')
        ax.set_ylabel('Temperature (°C)')
        ax.set_title(f'{self.city} Weather - Past 14 Days')
        ax.legend()

        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()

        return fig


class analyzer:
    def __init__(self, filename, path, format):
        self.filename = filename
        self.path = path
        self.format = format
        self.df = None

    def open_file(self):
        match self.format:
            case 'csv':
                df = pd.read_csv(self.path)
                print("CSV Data:")
                print(df)

            case 'json':
                with open(self.path, 'r') as f:
                    df = json.load(f)
                    print(f"JSON Data: {df}")
            case 'xlsx':
                df = pd.read_excel(self.path)
                print(f"Excel Data: {df}")
            case 'txt':
                try:
                    # Read a number from a file
                    with open(self.path, 'r') as f:
                        text = f.read()

                    print(f"Result: {text}")
                except FileNotFoundError:
                    print("File not found")

    def calculate_totals(self):

        df = pd.read_csv(self.path)

        # Calculate total for each row
        totals = []
        for index, row in df.iterrows():
            total = helper.calculate_total(row['quantity'], row['price'])
            totals.append(total)
        # Add totals to our data
        df['total'] = totals
        return df

        # ---------------------------------------------------------
        # 1) Umsatz pro Produkt (Bar Chart)
        # ---------------------------------------------------------

    def visualize_totals(self, df):

        grouped = df.groupby("product")["total"].sum()

        fig, ax = plt.subplots(figsize=(6, 4))
        grouped.plot(kind="bar", color=["#4e79a7", "#f28e2b", "#e15759", "#76b7b2"])

        ax.set_title("Gesamtumsatz pro Produkt")
        ax.set_xlabel("Produkt")
        ax.set_ylabel("Umsatz (€)")
        ax.grid(axis="y", linestyle="--", alpha=0.6)
        ax.tick_params(axis='x', rotation=0)  # <--- horizontal

        return fig

    # ---------------------------------------------------------
    # 2) Umsatz pro Datum (Line Chart)
    # ---------------------------------------------------------


    def visualize_total_by_date(self, df):
        grouped = df.groupby("date")["total"].sum()

        fig, ax = plt.subplots(figsize=(6, 4))
        grouped.plot(kind="line", marker="o", color="#4e79a7")

        ax.set_title("Gesamtumsatz pro Datum")
        ax.set_xlabel("Datum")
        ax.set_ylabel("Umsatz (€)")
        ax.grid(True)
        ax.tick_params(axis='x', rotation=0)  # <--- horizontal
        return fig


    def visualize_trend(self, df):
        pivot = df.pivot_table(index="date", columns="product", values="total", aggfunc="sum")

        pivot.plot(kind="line", marker="o", figsize=(6, 4))

        fig, ax = plt.subplots(figsize=(6, 4))
        pivot.plot(kind="line", marker="o", figsize=(12, 6))

        ax.set_title("Umsatz-Trend pro Produkt")
        ax.set_xlabel("datum")
        ax.set_ylabel("Umsatz (€)")
        ax.grid(axis="y", linestyle="--", alpha=0.6)
        ax.tick_params(axis='x', rotation=0)  # <--- horizontal
        return fig

    # ---------------------------------------------------------
    # 3) Produkt-Umsatz pro Datum (Grouped Bar Chart)
    # ---------------------------------------------------------


    def visualize_product_total_by_date(self, df):
        pivot = df.pivot_table(index="date", columns="product", values="total", aggfunc="sum")

        fig, ax = plt.subplots(figsize=(6, 4))
        pivot.plot(kind="bar", ax=ax)

        ax.set_title("Umsatz pro Produkt und Datum")
        ax.set_xlabel("Datum")
        ax.set_ylabel("Umsatz (€)")
        ax.grid(axis="y", linestyle="--", alpha=0.6)
        ax.tick_params(axis='x', rotation=0)  # <--- horizontal
        return fig


    # ---------------------------------------------------------
    # 4) Gestapelter Umsatz pro Datum (Stacked Bar Chart)
    # ---------------------------------------------------------
    def visualize_stacked(self, df):
        pivot = df.pivot_table(index="date", columns="product", values="total", aggfunc="sum")

        fig, ax = plt.subplots(figsize=(6, 4))
        pivot.plot(kind="bar", stacked=True, ax=ax)

        ax.set_title("Gestapelter Umsatz pro Datum")
        ax.set_xlabel("Datum")
        ax.set_ylabel("Umsatz (€)")
        ax.grid(axis="y", linestyle="--", alpha=0.6)
        ax.tick_params(axis='x', rotation=0)  # <--- horizontal
        return fig
