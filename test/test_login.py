"""Automated unittest for the login module."""

import unittest
from unittest.mock import MagicMock, patch

from account import login


class TestLogin(unittest.TestCase):
    """Test for the login class."""

    def setUp(self):
        self.mock_window = MagicMock()

    def test_init_object(self):
        """Test so an object of the class is created."""
        log = login.Login(self.mock_window)

        self.assertIsInstance(log, login.Login)

    def test_init_window(self):
        """Test the window of the login site."""
        log = login.Login(self.mock_window)

        self.assertEqual(log.window, self.mock_window)

    @patch("database.database_handler.DatabaseHandler")
    def test_init_dbconnects(self, mock_db_handler):
        """Test so that the DbConnects object get called once."""

        log = login.Login(self.mock_window)

        mock_db_handler.assert_called_once()

    @patch("bcrypt.checkpw", return_value=True)
    @patch("database.database_handler.DatabaseHandler")
    def test_login_valid_password(self, mock_db_handler, mock_checkpw):
        """This will check if correct password will work."""
        user_name = "test_user"
        hashed = mock_db_handler.get_hashed_pass(user_name)
        self.assertTrue(hashed and mock_checkpw)

    @patch("bcrypt.checkpw", return_value=False)
    @patch("database.database_handler.DatabaseHandler")
    def test_login_invalid_password(self, mock_db_handler, mock_checkpw):
        """This will check if incorrect password will not work."""
        user_name = "test_user"
        hashed = mock_db_handler.get_hashed_pass(user_name)
        self.assertTrue(hashed and mock_checkpw)


if __name__ == "__main__":
    unittest.main()
