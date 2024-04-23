"""This tests the user class."""

from unittest import TestCase
from unittest.mock import MagicMock

from account import user


class TestUser(TestCase):
    """This class will test the user class and its methods."""

    def setUp(self):
        self.mock_user = MagicMock()
        self.mock_window = MagicMock()
        self.mock_user_frame = MagicMock()

    def test_user_init(self):
        """Test so that the class is being instanciated."""
        self.mock_logged_in = MagicMock
        self.user = user.User(self.mock_logged_in, self.mock_user, self.mock_window)
        self.assertIsInstance(self.user, user.User)

    def test_user_logged_in_true(self):
        """Test if the user is logged in."""
        logged_in = True
        self.user = user.User(logged_in, self.mock_user, self.mock_window)

        self.assertTrue(logged_in)

    def test_user_logged_in_false(self):
        """Test so that the user is not logged in."""
        logged_in = False
        self.user = user.User(logged_in, self.mock_user, self.mock_window)

        self.assertFalse(logged_in)
