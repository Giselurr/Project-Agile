"""Test if the database handler works properly"""

import unittest
from unittest import TestCase, mock
from unittest.mock import MagicMock, patch

from database import database_handler


class TestDatabaseHandler(TestCase):
    """Test the so that the database handler does what it was intended."""

    def test_database_handler_init(self):
        """Test so that the class will be instansiated."""
        db_h = database_handler.DatabaseHandler()

        self.assertIsInstance(db_h, database_handler.DatabaseHandler)

    @patch("database.database_connection.DatabaseConnection")
    def test_database_handler_init_db(self, mock_db):
        """Test so that the database connection is called once"""
        db_h = database_handler.DatabaseHandler()

        mock_db.assert_called_once()

    @patch("mysql.connector.connect")
    def test_get_hashed_pass(self, mock_connect):
        """Test that the execute will work."""
        mock_conn = mock.Mock()
        mock_cursor = mock.Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ("hashed_password",)

        db_h = database_handler.DatabaseHandler()
        result = db_h.get_hashed_pass("user")

        self.assertEqual(result, "hashed_password")
        mock_cursor.execute.assert_called_once_with(
            "SELECT password FROM user WHERE user_name = %s", ("user",)
        )

    @patch("database.database_connection.DatabaseConnection.connect")
    def test_check_user_name_exists(self, mock_connect):
        """Check that a user can be fetched from the database."""
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ["user_name"]  # Simulate user exists

        db_h = database_handler.DatabaseHandler()

        result = db_h.check_user_name("user_name")

        self.assertTrue(result)

    @patch("database.database_connection.DatabaseConnection.connect")
    def test_check_user_name_not_exists(self, mock_connect):
        """Checks so that it works with no user found"""
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None  # Simulate user does not exist

        db_h = database_handler.DatabaseHandler()

        result = db_h.check_user_name("user_name_not_found")

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()