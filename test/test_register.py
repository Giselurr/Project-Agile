"""Make automated test for the register class."""

import unittest
from unittest.mock import MagicMock, Mock, patch

from account import register


class TestRegister(unittest.TestCase):
    """Test for the login class."""

    def setUp(self):
        self.mock_window = MagicMock()
        self.root = MagicMock()
        self.register_frame = MagicMock()
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
        """Test curser for registration."""
        mock_cursor = MagicMock()
        mock_database.connect.return_value = mock_cursor

        reg = register.Register(self.mock_window)
        cursor = mock_database.connect()

        self.assertEqual(mock_cursor, cursor)

    @patch("account.register.Register.check_username_conditions")
    @patch("account.register.Register.check_password_conditions")
    @patch("database.database_handler.DatabaseHandler.salt_hash")
    @patch("database.database_handler.DatabaseHandler.check_user_name")
    @patch("database.database_connection.DatabaseConnection.connect")
    @patch("database.database_connection.DatabaseConnection.commit")
    @patch("account.login.Login.login_gui")
    @patch("account.login.Login")
    def test_register_uscker_success(
        self,
        mock_login,
        mock_login_gui,
        mock_commit,
        mock_connect,
        mock_check_user_name,
        mock_hashpw,
        mock_check_username,
        mock_check_password,
    ):
        """Test so that the user can register his or hers account successfully."""
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_cursor
        mock_cursor.rowcount = 1
        mock_hashpw.return_value = b"hashed_password"
        password = "password".encode("utf-8")
        mock_name = MagicMock()
        mock_user = Mock(return_value="user")
        mock_check_username.return_value = True
        mock_check_password.return_value = True
        mock_check_user_name.return_value = False
        mock_reminder = MagicMock()

        self.reg.register_user(
            mock_user, mock_user, mock_user, mock_user, self.register_frame
        )
        mock_check_username.assert_called_once()
        mock_check_password.assert_called_once()
        mock_check_user_name.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_commit.assert_called_once()
        mock_cursor.close.assert_called_once()

    def test_username_white_space(self):
        """Test if error with only whitespace in username."""
        user_name = " "
        with self.assertRaises(register.UsernameError) as error:
            register.Register(self.mock_window).check_username_conditions(user_name)
            self.assertEqual(
                str(error.exception),
                "Not a valid username!\
                         \nUsername cannot contain whitespace",
            )

    def test_username_contain_white_space(self):
        """Test if error with whitespace in username."""
        user_name = "b b"
        with self.assertRaises(register.UsernameError) as error:
            register.Register(self.mock_window).check_username_conditions(user_name)
            self.assertEqual(
                str(error.exception),
                "Not a valid username!\
                         \nUsername cannot contain whitespace",
            )

    def test_username_to_long(self):
        """Test if error with username to long."""
        user_name = "obobobobobobo"
        with self.assertRaises(register.UsernameError) as error:
            register.Register(self.mock_window).check_username_conditions(user_name)
            self.assertEqual(str(error.exception), "Username to long!\nMax 12 letters")

    def test_password_only_white_space(self):
        """Test if only whitespace password raise error."""
        password = " "
        with self.assertRaises(register.UsernameError) as error:
            register.Register(self.mock_window).check_username_conditions(password)
            self.assertEqual(
                str(error.exception),
                "Not a valid password!\
                                \nPassword cannot contain whitespace",
            )

    def test_password_white_space(self):
        """Test if password containing whitespace raise error."""
        password = "L L"
        with self.assertRaises(register.UsernameError) as error:
            register.Register(self.mock_window).check_username_conditions(password)
            self.assertEqual(
                str(error.exception),
                "Not a valid password!\
                                \nPassword cannot contain whitespace",
            )


if __name__ == "__main__":
    unittest.main()
