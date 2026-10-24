import unittest
from unittest.mock import patch, mock_open
import pandas as pd

from Modules.weather import analyzer


class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        self.csv_path = "data/test.csv"
        self.json_path = "data/test.json"
        self.xlsx_path = "data/test.xlsx"
        self.txt_path = "data/test.txt"

        self.analyzer_csv = analyzer("test.csv", self.csv_path, "csv")
        self.analyzer_json = analyzer("test.json", self.json_path, "json")
        self.analyzer_xlsx = analyzer("test.xlsx", self.xlsx_path, "xlsx")
        self.analyzer_txt = analyzer("test.txt", self.txt_path, "txt")

    # ---------------------------------------------------------
    # CSV TEST
    # ---------------------------------------------------------
    @patch("pandas.read_csv")
    def test_open_file_csv(self, mock_read_csv):
        mock_df = pd.DataFrame({"a": [1], "b": [2]})
        mock_read_csv.return_value = mock_df

        self.analyzer_csv.open_file()

        mock_read_csv.assert_called_once_with(self.csv_path)

    # ---------------------------------------------------------
    # JSON TEST
    # ---------------------------------------------------------
    @patch("builtins.open", new_callable=mock_open, read_data='{"x": 1, "y": 2}')
    def test_open_file_json(self, mock_file):
        with patch("json.load", return_value={"x": 1, "y": 2}) as mock_json:
            self.analyzer_json.open_file()
            mock_file.assert_called_once_with(self.json_path, "r")
            mock_json.assert_called_once()

    # ---------------------------------------------------------
    # XLSX TEST
    # ---------------------------------------------------------
    @patch("pandas.read_excel")
    def test_open_file_xlsx(self, mock_read_excel):
        mock_df = pd.DataFrame({"col": [10]})
        mock_read_excel.return_value = mock_df

        self.analyzer_xlsx.open_file()

        mock_read_excel.assert_called_once_with(self.xlsx_path)

    # ---------------------------------------------------------
    # TXT TEST
    # ---------------------------------------------------------
    @patch("builtins.open", new_callable=mock_open, read_data="42")
    def test_open_file_txt(self, mock_file):
        self.analyzer_txt.open_file()
        mock_file.assert_called_once_with(self.txt_path, "r")

    # ---------------------------------------------------------
    # TXT TEST – FILE NOT FOUND
    # ---------------------------------------------------------
    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_open_file_txt_not_found(self, mock_file):
        self.analyzer_txt.open_file()
        mock_file.assert_called_once_with(self.txt_path, "r")

    # ---------------------------------------------------------
    # calculate_totals TEST Modules.weather
    # ---------------------------------------------------------
    @patch("pandas.read_csv")
    @patch("Modules.weather.analyzer.calculate_totals")
    def test_calculate_totals(self, mock_calc_total, mock_read_csv):
        mock_df = pd.DataFrame({
            "quantity": [2, 3],
            "price": [10, 20]
        })

        mock_read_csv.return_value = mock_df
        mock_calc_total.side_effect = [20, 60]  # 2*10, 3*20

        result = self.analyzer_csv.calculate_totals()

        mock_read_csv.assert_called_once_with(self.csv_path)
        self.assertIn("total", result.columns)
        self.assertEqual(result["total"].tolist(), [20, 60])
        self.assertEqual(mock_calc_total.call_count, 2)


if __name__ == "__main__":
    unittest.main()
