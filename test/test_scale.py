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
        self.reg = scale.Scale(self.root, self.mock_user_name)

    def tearDown(self):
        """later."""
        self.scale_frame.destroy()
        self.root.destroy()

    def test_init(self):
        """later."""
        mock_window = MagicMock()
        ref = scale.Scale(mock_window, self.mock_user_name)
        self.assertIsInstance(ref, scale.Scale)

    @patch("account.user.User")
    def test_return_to_user_page(self, mock_user):
        """later."""
        self.reg.return_to_user_page(self.scale_frame, 2)
        mock_user.assert_called_once_with(True, self.reg.user, self.reg.window)
        mock_user.return_value.user_gui.assert_called_once()
