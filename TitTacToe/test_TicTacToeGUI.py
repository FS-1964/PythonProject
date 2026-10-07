import unittest
from unittest.mock import MagicMock, patch

import tkinter as tk

from Modules.games import tictactoe


class TestTicTacToeGUI(unittest.TestCase):

    def setUp(self):
        # Tkinter root mocken
        self.root = MagicMock(spec=tk.Tk)

        # Buttons mocken
        with patch("tkinter.Button") as mock_button, \
                patch("tkinter.Frame") as mock_frame:
            # Button-Mock erzeugen
            btn_mock = MagicMock()
            mock_button.return_value = btn_mock

            frame_mock = MagicMock()
            mock_frame.return_value = frame_mock

            self.gui = tictactoe(self.root)

            # Buttons ersetzen durch echte Mocks
            self.gui.buttons = [[MagicMock() for _ in range(3)] for _ in range(3)]

    # ---------------------------------------------------------
    # Test: Brett wird korrekt erstellt
    # ---------------------------------------------------------
    def test_erstelle_brett(self):
        brett = erstelle_brett()
        self.assertEqual(len(brett), 3)
        self.assertEqual(len(brett[0]), 3)
        self.assertEqual(brett[0][0], " ")

    # ---------------------------------------------------------
    # Test: Gewinnererkennung funktioniert
    # ---------------------------------------------------------
    def test_check_winner(self):
        brett = [
            ["X", "X", "X"],
            [" ", " ", " "],
            [" ", " ", " "]
        ]
        self.assertTrue(tictactoe.check_winner(brett, "X"))

    # ---------------------------------------------------------
    # Test: Remis funktioniert
    # ---------------------------------------------------------
    def test_check_remie(self):
        brett = [
            ["X", "O", "X"],
            ["O", "X", "O"],
            ["O", "X", "O"]
        ]
        self.assertTrue(tictactoe.check_remie(brett))

    # ---------------------------------------------------------
    # Test: Klick setzt Zeichen
    # ---------------------------------------------------------
    def test_klick_setzt_zeichen(self):
        self.gui.klick(0, 0)
        self.assertEqual(self.gui.brett[0][0], "X")
        self.gui.buttons[0][0].config.assert_called_with(text="X")

    # ---------------------------------------------------------
    # Test: Klick auf belegtes Feld macht nichts
    # ---------------------------------------------------------
    def test_klick_auf_belegtes_feld(self):
        self.gui.brett[0][0] = "X"
        self.gui.klick(0, 0)
        # Keine Änderung
        self.assertEqual(self.gui.brett[0][0], "X")

    # ---------------------------------------------------------
    # Test: Gewinner löst messagebox + reset aus
    # ---------------------------------------------------------
    @patch("tkinter.messagebox.showinfo")
    def test_klick_gewinner(self, mock_msg):
        self.gui.brett = [
            ["X", "X", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]
        self.gui.klick(0, 2)

        mock_msg.assert_called_once()
        # Reset wurde ausgeführt
        self.assertEqual(self.gui.brett[0][0], " ")

    # ---------------------------------------------------------
    # Test: Reset setzt Brett zurück
    # ---------------------------------------------------------
    def test_reset(self):
        self.gui.brett = [
            ["X", "O", "X"],
            ["O", "X", "O"],
            ["O", "X", "O"]
        ]
        self.gui.reset()

        for row in self.gui.brett:
            self.assertEqual(row, [" ", " ", " "])


if __name__ == "__main__":
    unittest.main()
