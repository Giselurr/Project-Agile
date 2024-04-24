"""Test the database connection module."""

import unittest
from unittest import TestCase, mock
from unittest.mock import patch

from database import database_connection


class TestDatabaseConnetion(TestCase):
    """This will test the database connection class."""

    @patch("mysql.connector.connect")
    def test_connect(self, mock_connect):
        """Will test so a connetion with the database works."""
        db = database_connection.DatabaseConnection("test_user", "test_password")
        db.connect()
        mock_connect.assert_called_once_with(
            user="test_user",
            password="test_password",
            host="localhost",
            port=3306,
            database="breathe",
            raise_on_warnings=True,
        )

    @patch("mysql.connector.connect")
    def test_commit(self, mock_connect):
        """Test so that the commit will work"""
        mock_conn = mock.Mock()
        mock_conn.is_connected.return_value = True
        mock_connect.return_value = mock_conn

        db_connection = database_connection.DatabaseConnection("user", "password")
        db_connection.my_con = (
            mock_conn  # Manually setting the connection to mock object
        )
        db_connection.commit()

        mock_conn.commit.assert_called_once()

        mock_connect.assert_not_called()


if __name__ == "__main__":
    unittest.main()
