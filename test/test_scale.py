from unittest import TestCase
from unittest.mock import MagicMock, patch

from schedule import scale


class TestScale(TestCase):
    """later."""

    def setUp(self):
        """later."""
        self.mock_window = MagicMock()
        self.root = MagicMock()
        self.scale_frame = MagicMock()
        self.scale_frame.pack()
        self.mock_user_name = MagicMock()
        self.mock_date = MagicMock()
        self.reg = scale.Scale(self.root, self.mock_user_name, self.mock_date)

    def tearDown(self):
        """later."""
        self.scale_frame.destroy()
        self.root.destroy()

    def test_init(self):
        """later."""
        mock_window = MagicMock()
        mock_date = MagicMock()
        ref = scale.Scale(mock_window, self.mock_user_name, mock_date)
        self.assertIsInstance(ref, scale.Scale)

    @patch("main.Main")
    def test_return_to_user_page(self, mock_main):
        """later."""
        self.reg.return_to_user_page(self.scale_frame, False)
        mock_main.manager_menu_choice.assert_called_once()
