import os
import requests
import pandas as pd

class WeatherExporter:
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
        os.makedirs("weatherdata", exist_ok=True)

        path = f"weather-forcast/weatherdata/{self.city}_weather.csv"
        df.to_csv(path, index=False, sep=";", encoding="utf-8")
        print(f"Data saved to {path}")
        return path

    def export_to_csv(self):
        weather_data = self.get_weather_forecast()
        df = self.convert_to_dataframe(weather_data)
        path=self.save_csv(df)
        return path
