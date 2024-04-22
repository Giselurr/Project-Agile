"""Make automated test for the register class."""

import unittest
from tkinter import Frame, Tk
from unittest.mock import MagicMock, patch

from account import register


class TestRegister(unittest.TestCase):
    """Test for the login class."""

    def setUp(self):
        self.mock_window = MagicMock()
        self.root = Tk()
        self.register_frame = Frame(self.root)
        self.register_frame.pack()
        self.reg = register.Register(self.root)

    def tearDown(self):
        self.register_frame.destroy()
        self.root.destroy()

    def test_init_object(self):
        """Test so an object of the class is created."""
        reg = register.Register(self.mock_window)

        self.assertIsInstance(reg, register.Register)

    def test_init_window(self):
        """Test the initialaztion window."""
        reg = register.Register(self.mock_window)

        self.assertEqual(reg.window, self.mock_window)

    @patch("database.database_handler.DatabaseHandler")
    def test_init_db_handler(self, mock_db_handler):
        """Test so that the connects class instansiates"""
        reg = register.Register(self.mock_window)

        mock_db_handler.assert_called_once()

    @patch(
        "database.database_connection.DatabaseConnection",
        MagicMock(return_value=MagicMock()),
    )
    def test_init_db_connect(self):
        """Test the connection class instansiates"""
        reg = register.Register(self.mock_window)

        self.assertTrue(reg.database.called_once)

    @patch("database.database_handler")
    def test_register_user_exists_true(self, mock_db_handler):
        """Test if the user exists works with a true value"""
        reg = register.Register(self.mock_window)
        mock_check_user_name = mock_db_handler.check_user_name.return_value = True
        user_exists = mock_db_handler.check_user_name(mock_check_user_name)

        self.assertTrue(user_exists)

    @patch("database.database_handler")
    def test_register_user_exists_false(self, mock_db_handler):
        """Test if the user exists works with a false value"""
        reg = register.Register(self.mock_window)
        mock_check_user_name = mock_db_handler.check_user_name.return_value = False
        user_exists = mock_db_handler.check_user_name(mock_check_user_name)

        self.assertFalse(user_exists)

    @patch("database.database_connection.DatabaseConnection")
    def test_register_user_curser(self, mock_database):
        mock_cursor = MagicMock()
        mock_database.connect.return_value = mock_cursor

        reg = register.Register(self.mock_window)
        cursor = mock_database.connect()

        self.assertEqual(mock_cursor, cursor)


@patch("account.register.Toplevel")
@patch("account.register.bcrypt.hashpw")
@patch("database.datbase_handler.DatabaseHandler.check_user_name", return_value=False)
@patch("database.database_connection.DatabaseConnection.connect")
def test_register_uscker_success(
    self, mock_connect, mock_check_user_name, mock_hashpw, mock_toplevel
):
    """Test so that the user can register his or hers account successfully."""
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_cursor
    mock_cursor.rowcount = 1
    mock_hashpw.return_value = b"hashed_password"
    password = "password".encode("utf-8")

    self.reg.register_user("First", "Last", "user", password, self.register_frame)

    mock_check_user_name.assert_called_once_with("user")
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cursor.commit.assert_called_once()
    mock_toplevel.assert_called_once()


if __name__ == "__main__":
    unittest.main()