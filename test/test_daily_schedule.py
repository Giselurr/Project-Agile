"""This will test if the daily schedule will work as intended."""

import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch

from schedule import daily_schedule


class TestDailySchedule(TestCase):
    """Test the daily schedule."""

    def setUp(self):
        self.mock_window = MagicMock()
        self.mock_user = "test_user"
        self.mock_date = datetime.datetime.now()
        self.mock_reminder = MagicMock()
        self.mock_db_handler = MagicMock()
        self.mock_db_handler.get_daily_schedule.return_value = []
        self.daily = daily_schedule.DailyScheduele(
            self.mock_window, self.mock_user, self.mock_date, self.mock_reminder
        )

    @patch("database.database_handler.DatabaseHandler")
    def test_init(self, mock_db_handler):
        """Test so that object will be initialized."""
        mock_db_handler.return_value = self.mock_db_handler
        self.assertIsInstance(self.daily, daily_schedule.DailyScheduele)

    @patch("database.database_handler.DatabaseHandler")
    def test_init_assert(self, mock_db_handler):
        """Test so the get daily schedule is called."""
        mock_db_handler.return_value = self.mock_db_handler
        daily_schedule.DailyScheduele(
            self.mock_window, self.mock_user, self.mock_date, self.mock_reminder
        )

        self.mock_db_handler.get_daily_schedule.assert_called_once_with(self.mock_user)
