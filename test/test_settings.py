"""Testing for the user settings."""

import unittest
from unittest.mock import MagicMock, patch

from account import settings


class TestSettings(unittest.TestCase):
    """Make sure that the setting class behaves appropiatly."""

    def setUp(self):
        self.mock_window = MagicMock()
        self.mock_user_name = "test_user"
        self.mock_loggged_in = True
        self.mock_settings_frame = MagicMock()
        self.mock_old_password = MagicMock()
        self.mock_new_password = MagicMock()
        self.mock_password = MagicMock()
        self.set = settings.UserSettings(
            self.mock_loggged_in, self.mock_user_name, self.mock_window
        )

    def test_init(self):
        """Test if the class will instanciate."""

        self.assertIsInstance(self.set, settings.UserSettings)

    def test_press_enter_change(self):
        self.set.setting_frame = self.mock_settings_frame
        self.set.old_password = self.mock_old_password
        self.set.new_password = self.mock_new_password
        self.set.entry_change = MagicMock()
        self.set.entry_delete = MagicMock()

        mock_entry_change = MagicMock()
        mock_entry_delete = MagicMock()
        self.set.entry_change.bind = MagicMock()
        self.set.entry_delete.bind = MagicMock()
        mock_event = MagicMock()

        mock_event.widget = mock_entry_change

        self.set.entry_change = mock_entry_change
        self.set.change_password = MagicMock()
        self.set.press_enter(mock_event)

        self.set.change_password.assert_called_once_with(
            self.mock_settings_frame, self.mock_old_password, self.mock_new_password
        )

    def test_press_enter_delete(self):
        self.set.setting_frame = self.mock_settings_frame
        self.set.password = self.mock_password
        self.set.entry_change = MagicMock()
        self.set.entry_delete = MagicMock()
        mock_entry_delete = MagicMock()
        self.set.entry_change.bind = MagicMock()
        self.set.entry_delete.bind = MagicMock()
        mock_event = MagicMock()

        mock_event.widget = mock_entry_delete

        self.set.entry_delete = mock_entry_delete
        self.set.delete_account = MagicMock()
        self.set.press_enter(mock_event)
        self.set.delete_account.assert_called_once_with(
            self.mock_settings_frame, self.mock_password
        )

    @patch("bcrypt.checkpw", return_value=True)
    @patch("tkinter.messagebox.showinfo")
    @patch("main.Main.manager_menu_choice")
    def test_change_password(self, mock_main_manager, mock_messagebox, mock_checkpw):
        """Check so that the change password method works."""
        self.set.db_handler = MagicMock()
        self.set.database = MagicMock()
        self.set.cursor = MagicMock()
        self.set.database.connect.return_value = self.set.cursor

        self.mock_old_password.get.return_value = "old_password"
        self.mock_new_password.get.return_value = "new_password"
        self.set.db_handler.get_hashed_pass.return_value = "hashed_password"
        self.set.cursor.rowcount = 1

        self.set.change_password(
            self.mock_settings_frame, self.mock_old_password, self.mock_new_password
        )

        self.set.db_handler.salt_hash.assert_called_once_with("new_password")
        self.set.cursor.execute.assert_called()
        self.set.database.commit.assert_called()
        mock_main_manager.assert_called_once_with(
            self.set, self.mock_settings_frame, "USER_MENU", self.mock_user_name
        )

    @patch("main.Main.manager_menu_choice")
    @patch("bcrypt.checkpw", return_value=True)
    @patch("tkinter.messagebox.showinfo")
    def test_delete_account(self, mock_message, mock_checkpw, mock_main_manager):
        """Check so that the user can delete their account."""
        self.mock_password.get.return_value = "password"
        self.set.cursor = MagicMock()
        self.set.db_handler = MagicMock()
        self.set.database = MagicMock()
        self.set.db_handler.get_hashed_pass.return_value = "hashed_password"
        self.set.database.connect.return_value = self.set.cursor
        self.set.cursor.rowcount = 1

        self.set.delete_account(self.mock_settings_frame, self.mock_password)

        self.set.cursor.execute.assert_called()
        self.set.cursor.execute.assert_called_with(
            "DELETE FROM user WHERE user_name = %s", (self.mock_user_name,)
        )
        self.set.database.commit.assert_called()

        mock_message.assert_called_with(
            "Success!", "Your account has successfully been deleted."
        )
        mock_main_manager.assert_called_once_with(
            self.set, self.mock_settings_frame, "MAIN_MENU", None
        )
