import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os

from Modules.weather import weatherexporter


class TestWeatherExporter(unittest.TestCase):

    def setUp(self):
        self.exporter = weatherexporter(
            latitude=48.2082,
            longitude=16.3738,
            city="Vienna",
            startdate="2024-09-24",
            enddate="2024-09-30"
        )

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

        data = self.exporter.get_weather_forecast()

        self.assertIn("daily", data)
        self.assertEqual(data["daily"]["temperature_2m_max"][0], 22.5)

        mock_get.assert_called_once()
        called_url = mock_get.call_args[0][0]
        self.assertIn("latitude=48.2082", called_url)
        self.assertIn("longitude=16.3738", called_url)

    # ---------------------------------------------------------
    # Test: convert_to_dataframe erzeugt korrektes DataFrame
    # ---------------------------------------------------------
    def test_convert_to_dataframe(self):
        df = self.exporter.convert_to_dataframe(self.mock_api_response)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertListEqual(list(df.columns), ["date", "temp_max", "temp_min"])
        self.assertEqual(len(df), 2)

        # Dezimaltrennzeichen korrekt ersetzt
        self.assertEqual(df["temp_max"][0], "22,5")
        self.assertEqual(df["temp_min"][0], "12,3")

    # ---------------------------------------------------------
    # Test: save_csv erzeugt Datei korrekt
    # ---------------------------------------------------------
    def test_save_csv(self):
        df = self.exporter.convert_to_dataframe(self.mock_api_response)

        # Ordner vorher löschen
        if os.path.exists("weather-forcast/weatherdata/Vienna_weather.csv"):
            os.remove("weather-forcast/weatherdata/Vienna_weather.csv")

        path = self.exporter.save_csv(df)

        self.assertTrue(os.path.exists(path))
        self.assertIn("Vienna_weather.csv", path)

    # ---------------------------------------------------------
    # Test: export_to_csv führt kompletten Ablauf korrekt aus
    # ---------------------------------------------------------
    @patch("Modules.weather.requests.get")
    def test_export_to_csv(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = self.mock_api_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        path = self.exporter.export_to_csv()

        self.assertTrue(os.path.exists(path))
        self.assertIn("Vienna_weather.csv", path)

    # ---------------------------------------------------------
    # Test: API‑Fehler wird korrekt weitergegeben
    # ---------------------------------------------------------
    @patch("Modules.weather.requests.get")
    def test_get_weather_forecast_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_get.return_value = mock_response

        with self.assertRaises(Exception):
            self.exporter.get_weather_forecast()


if __name__ == "__main__":
    unittest.main()

