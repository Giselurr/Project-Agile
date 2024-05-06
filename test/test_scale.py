from unittest import TestCase
from unittest.mock import MagicMock, patch

from schedule import scale


class TestScale(TestCase):
    """later."""

    def setUp(self):
        self.mock_window = MagicMock()
        self.root = MagicMock()
        self.scale_frame = MagicMock()
        self.scale_frame.pack()
        self.mock_user_name = MagicMock()
        self.mock_date = MagicMock()
        self.reg = scale.Scale(self.root, self.mock_user_name, self.mock_date)

    def tearDown(self):
        self.scale_frame.destroy()
        self.root.destroy()

    def test_init(self):
        """Test so that the class is being instanciated."""
        mock_window = MagicMock()
        mock_date = MagicMock()
        ref = scale.Scale(mock_window, self.mock_user_name, mock_date)
        self.assertIsInstance(ref, scale.Scale)

    @patch("main.Main")
    def test_return_to_user_page(self, mock_main):
        """Test that return to user page calles on the manager menu."""
        self.reg.return_to_user_page(self.scale_frame, False)
        mock_main.manager_menu_choice.assert_called_once()

    @patch("tkinter.PhotoImage")
    @patch("mysql.connector.connect")
    @patch("database.database_handler.DatabaseHandler.check_date")
    def test_check_entry(self, mock_database, mock_connection, mock_image):
        """Test that the method call on check_date."""
        mock_note = MagicMock()
        mock_colour = MagicMock()
        mock_colour.get.return_value = "1"
        mock_image.return_value = MagicMock()
        mock_database.return_value = ("", False)
        self.reg.check_entry(
            self.scale_frame, mock_colour, mock_note, mock_image, mock_image, mock_image
        )
        mock_database.assert_called_once()

    @patch("main.Main.manager_menu_choice")
    @patch("tkinter.PhotoImage")
    @patch("mysql.connector.connect")
    @patch("database.database_handler.DatabaseHandler.update_row")
    def test_update_row(self, mock_database, mock_connection, mock_image, mock_main):
        """Test that the method call on update row."""
        mock_note = MagicMock()
        mock_colour = MagicMock()
        mock_id = MagicMock()
        self.reg.update_row(self.scale_frame, mock_colour, mock_note, mock_id, False)
        mock_database.assert_called_once()
