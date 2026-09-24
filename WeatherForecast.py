

import requests
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
class WeatherForecast:

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
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

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


    def visualize_weather_forecast(self):
        df = self.extract_weather_forecast()
        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(df['date'], df['max_temp'], marker='o', label='Max Temp')
        plt.plot(df['date'], df['min_temp'], marker='o', label='Min Temp')

        # Add labels and title
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.title(f'{self.city} Weather - Past 7 Days')
        plt.legend()

        # Rotate x-axis labels for readability
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot
        plt.savefig('weather_chart.png')
        plt.show()
