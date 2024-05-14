"""Make automated test for the Main class."""

import unittest
from tkinter import Tk
from unittest.mock import MagicMock, Mock, patch

import main


class TestMain(unittest.TestCase):
    """Test for the Main class."""

    def setUp(self):
        self.window = Mock(spec=Tk)
        self.main = main.Main(self.window)

    @patch("account.main_menu.MainMenu")
    def test_start_main_window(self, mock_main_menu):
        """Test the start of the main menu window."""
        self.main.start_main_window()
        mock_main_menu.assert_called_once_with(self.window)
        mock_main_menu.return_value.main_gui.assert_called_once()

    @patch("account.main_menu.MainMenu")
    def test_manager_menu_choice_main_menu(self, mock_main_menu):
        """Test the manager choice main menu."""
        frame = Mock()
        mock_date = MagicMock()
        self.main.manager_menu_choice(frame, "MAIN_MENU", "test_user", mock_date)
        frame.pack_forget.assert_called_once()
        mock_main_menu.assert_called_once_with(self.window)
        mock_main_menu.return_value.main_gui.assert_called_once()

    @patch("account.login.Login")
    def test_manager_menu_choice_login(self, mock_login):
        """Test the manager choice login."""
        frame = Mock()
        mock_date = MagicMock()
        self.main.manager_menu_choice(frame, "LOGIN", "test_user", mock_date)
        frame.pack_forget.assert_called_once()
        mock_login.assert_called_once_with(self.window)
        mock_login.return_value.login_gui.assert_called_once()

    @patch("account.register.Register")
    def test_manager_menu_choice_register(self, mock_register):
        """Test the manager choice register."""
        frame = Mock()
        mock_date = MagicMock()
        self.main.manager_menu_choice(frame, "REGISTER", "test_user", mock_date)
        frame.pack_forget.assert_called_once()
        mock_register.assert_called_once_with(self.window)
        mock_register.return_value.register_gui.assert_called_once()

    @patch("account.user.User")
    def test_manager_menu_choice_user_menu(self, mock_user):
        """Test the manager choice user."""
        frame = Mock()
        mock_date = MagicMock()
        self.main.manager_menu_choice(frame, "USER_MENU", "test_user", mock_date)
        frame.pack_forget.assert_called_once()
        mock_user.assert_called_once_with(True, "test_user", self.window)
        mock_user.return_value.user_gui.assert_called_once()

    @patch("breathing.boxbreathing.DisplayExercise")
    def test_manager_menu_choice_breathe(self, mock_breathe):
        """Test the manager choice breathe."""
        frame = Mock()
        mock_date = MagicMock()
        self.main.manager_menu_choice(frame, "BREATHE", "test_user", mock_date)
        frame.pack_forget.assert_called_once()
        mock_breathe.assert_called_once_with(self.window, "test_user")
        mock_breathe.return_value.display_imagery.assert_called_once()

    @patch("schedule.scale.Scale")
    def test_manager_menu_choice_stress_level(self, mock_scale):
        """Test the manager choice scale."""
        frame = Mock()
        mock_date = MagicMock()
        self.main.manager_menu_choice(frame, "STRESS_LEVEL", "test_user", mock_date)
        frame.pack_forget.assert_called_once()
        mock_scale.assert_called_once_with(self.window, "test_user", mock_date)
        mock_scale.return_value.scale_gui.assert_called_once()

    @patch("schedule.stress_history.History")
    def test_manager_menu_choice_stress_history(self, mock_history):
        """Test the manager choice stress history."""
        frame = Mock()
        mock_date = MagicMock()

        mock_reminder = MagicMock()
        menu_choices = [
            ("LOGIN", mock_login, "login_gui"),
            ("REGISTER", mock_register, "register_gui"),
            ("USER_MENU", mock_user, "user_gui"),
            ("STRESS_LEVEL", mock_scale, "scale_gui"),
            # Add other menu choices here and in the patch.
        ]
        for menu_choice, mock_class, method_name in menu_choices:
            with self.subTest(menu_choice=menu_choice):
                self.main.manager_menu_choice(
                    frame, menu_choice, "test_user", mock_date, mock_reminder
                )
                frame.pack_forget.assert_called_once()
                if menu_choice == "USER_MENU":  # Uses different args than the rest.
                    mock_user.assert_called_once_with(True, "test_user", self.window)
                elif (
                    menu_choice == "STRESS_LEVEL"
                ):  # Uses different args than the rest.
                    mock_scale.assert_called_once_with(
                        self.window, "test_user", mock_date, mock_reminder
                    )
                else:
                    mock_class.assert_called_once_with(self.window)
                getattr(mock_class.return_value, method_name).assert_called_once()

                frame.reset_mock()
                mock_class.reset_mock()


    # OTHER IMPLEMENTATION OF TESTS THAT CAN REPLACE test_manager_menu_choice
    # IF THAT TEST BECOMES TOO ADVANCED OR COMPLICATED.

    # @patch("account.register.Register")
    # @patch("account.login.Login")
    # @patch("account.user.User")
    # @patch("schedule.scale.Scale")
    # def test_manager_menu_choice(
    #     self, mock_scale, mock_user, mock_login, mock_register
    # ):
    #     """Test all of the different choices in the manager."""
    #     frame = Mock()
    #     mock_date = MagicMock()
    #     menu_choices = [
    #         ("LOGIN", mock_login, "login_gui"),
    #         ("REGISTER", mock_register, "register_gui"),
    #         ("USER_MENU", mock_user, "user_gui"),
    #         ("STRESS_LEVEL", mock_scale, "scale_gui"),
    #         # Add other menu choices here and in the patch.
    #     ]
    #     for menu_choice, mock_class, method_name in menu_choices:
    #         with self.subTest(menu_choice=menu_choice):
    #             self.main.manager_menu_choice(
    #                 frame, menu_choice, "test_user", mock_date
    #             )
    #             frame.pack_forget.assert_called_once()
    #             if menu_choice == "USER_MENU":  # Uses different args than the rest.
    #                 mock_user.assert_called_once_with(True, "test_user", self.window)
    #             elif (
    #                 menu_choice == "STRESS_LEVEL"
    #             ):  # Uses different args than the rest.
    #                 mock_scale.assert_called_once_with(
    #                     self.window, "test_user", mock_date
    #                 )
    #             else:
    #                 mock_class.assert_called_once_with(self.window)
    #             getattr(mock_class.return_value, method_name).assert_called_once()

    #             frame.reset_mock()
    #             mock_class.reset_mock()


if __name__ == "__main__":
    unittest.main()
