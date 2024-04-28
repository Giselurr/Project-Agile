from unittest import TestCase
from unittest.mock import MagicMock, patch

from schedule import scale


class TestScale(TestCase):
    """later."""

    def setUp(self):
        self.mock_window = MagicMock()
        self.root = MagicMock()
        with patch("schedule.scale.StringVar") as mock_stringvar:
            self.scale_frame = MagicMock()
            self.scale_frame.pack()
            self.mock_user_name = MagicMock()
            self.reg = scale.Scale(self.root, self.mock_user_name)

    def tearDown(self):
        self.scale_frame.destroy()
        self.root.destroy()

    def test_init(self):
        """later."""
        mock_window = MagicMock()
        with patch("schedule.scale.StringVar") as mock_stringvar:
            ref = scale.Scale(mock_window, self.mock_user_name)
            self.assertIsInstance(ref, scale.Scale)

    @patch("tkinter.Toplevel")
    @patch("account.user.User")
    def test_return_to_user_page(self, mock_user, mock_toplevel):
        """later."""
        mock_destroy = MagicMock()
        mock_toplevel = MagicMock()
        mock_toplevel.destroy = mock_destroy
        mock_user_name = MagicMock()
        mock_user = MagicMock(side_effect=[True, mock_user_name, self.mock_window])

        self.reg.return_to_user_page(self.scale_frame)
        mock_user.user_gui.assert_called_once()

    @patch("database.database_connection.DatabaseConnection.execute")
    @patch("database.database_connection.DatabaseConnection.connect")
    @patch("database.database_connection.DatabaseConnection.commit")
    @patch("datetime.datetime")
    @patch("database.database_connection.DatabaseConnection")
    def test_store_selected(
        self, mock_db_connection, mock_date, mock_commit, mock_connect, mock_execute
    ):
        """later."""
        with patch("schedule.scale.Scale.store_selected") as mock_function:
            mock_function.query = MagicMock()
            mock_db_connection.connect = MagicMock()
            mock_cursor = mock_db_connection.connect
            mock_db_connection.execute = MagicMock()
            mock_db_connection.commit = MagicMock()
            mock_db_connection.close = MagicMock()
            mock_cursor.rowcount = 1
            mock_date.now.strftime = MagicMock()
            self.reg.store_selected(self.scale_frame)
            mock_date.strftime.assert_called_once_with("%Y-%m-%d")
            mock_db_connection.connect.assert_called_once()
            mock_db_connection.execute.assert_called_once()
            mock_db_connection.commit.assert_called_once()
            mock_db_connection.close.assert_called_once()
