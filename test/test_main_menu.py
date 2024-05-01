"""Automated unittest for the main_menu class."""

import unittest
from unittest.mock import MagicMock

from account import main_menu


class TestMainMenu(unittest.TestCase):
    """This class will test the main_menu class and its methods."""

    def setUp(self):
        self.mock_window = MagicMock()
        self.mock_user_frame = MagicMock()
        self.main_menu = main_menu.MainMenu(self.mock_window)
        self.main_menu.window = MagicMock()

    def test_main_menu_init(self):
        """Test so that the class is being instanciated."""

        self.assertIsInstance(self.main_menu, main_menu.MainMenu)


if __name__ == "__main__":
    unittest.main()
