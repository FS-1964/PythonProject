import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import matplotlib.pyplot as plt
import os
from Modules.weather import weatherforecast

class TestWeatherForecast(unittest.TestCase):

    def setUp(self):
        self.wf = weatherforecast( latitude=48.2082,
            longitude=16.3738,
            startdate="2024-09-24",
            enddate="2024-09-30",
            city="Vienna")

        # Beispiel‑API‑Response
        self.mock_api_response = {
            "daily": {
                "time": ["2024-09-24", "2024-09-25"],
                "temperature_2m_max": [22.5, 23.1],
                "temperature_2m_min": [12.3, 13.0]
            }
        }

    # ---------------------------------------------------------
    # Test: get_weather_forecast ruft API korrekt auf
    # ---------------------------------------------------------
    @patch("Modules.weather.requests.get")
    def test_get_weather_forecast(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = self.mock_api_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        data = self.wf.get_weather_forecast()

        self.assertIn("daily", data)
        self.assertEqual(data["daily"]["temperature_2m_max"][0], 22.5)

        mock_get.assert_called_once()
        called_url = mock_get.call_args[0][0]
        self.assertIn("latitude=48.2082", called_url)
        self.assertIn("longitude=16.3738", called_url)

    # ---------------------------------------------------------
    # Test: extract_weather_forecast gibt korrektes DataFrame zurück
    # ---------------------------------------------------------
    @patch("Modules.weather.requests.get")
    def test_extract_weather_forecast(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = self.mock_api_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        df = self.wf.extract_weather_forecast()

        self.assertIsInstance(df, pd.DataFrame)
        self.assertListEqual(list(df.columns), ["date", "max_temp", "min_temp"])
        self.assertEqual(len(df), 2)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df["date"]))

    # ---------------------------------------------------------
    # Test: print_weather_forecast formatiert Temperaturen korrekt
    # ---------------------------------------------------------
    @patch("Modules.weather.requests.get")
    def test_print_weather_forecast(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = self.mock_api_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with patch("builtins.print") as mock_print:
            self.wf.print_weather_forecast()
            printed_df = mock_print.call_args[0][0]

            self.assertIn("22.5°C", str(printed_df))
            self.assertIn("12.3°C", str(printed_df))

    # ---------------------------------------------------------
    # Test: visualize_weather_forecast erzeugt PNG‑Datei
    # ---------------------------------------------------------

    @patch("Modules.weather.requests.get")
    def test_visualize_weather_forecast(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "daily": {
                "time": ["2024-09-24", "2024-09-25"],
                "temperature_2m_max": [22.5, 23.1],
                "temperature_2m_min": [12.3, 13.0]
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        fig = self.wf.visualize_weather_forecast()
        self.assertIsNotNone(fig)

    # ---------------------------------------------------------
    # Test: API‑Fehler wird korrekt behandelt
    # ---------------------------------------------------------
    @patch("Modules.weather.requests.get")
    def test_get_weather_forecast_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_get.return_value = mock_response

        with self.assertRaises(Exception):
            self.wf.get_weather_forecast()


if __name__ == "__main__":
    unittest.main()
