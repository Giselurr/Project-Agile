"""This tests the main class."""

from unittest import TestCase
from unittest.mock import MagicMock

import main


class TestMain(TestCase):
    """This class will test the main class and its methods."""

    def setUp(self):
        self.mock_window = MagicMock()
        self.mock_user_frame = MagicMock()
        self.main = main.Main()

    def test_main_init(self):
        """Test so that the class is being instanciated."""
        self.assertIsInstance(self.main, main.Main)
