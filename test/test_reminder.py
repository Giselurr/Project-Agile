"""Test the reminder module."""

import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch

from schedule import reminder


class TestReminder(TestCase):
    """Test the reminder class."""

    def setUp(self):
        """Sets up the testing enviroment."""
        mock_window = MagicMock()
        mock_frame = MagicMock()
        mock_user = MagicMock()
        self.reminder_obj = reminder.Reminder(
            mock_window, mock_frame, mock_user, reminder.Reminder
        )

    def test_init(self):
        """Test so that the class instansiates."""
        self.assertIsInstance(self.reminder_obj, reminder.Reminder)

    @patch("schedule.reminder.datetime")
    def test_add_tasks(self, mock_datetime):
        """Check if the method adds the tasks properly."""
        mock_lock = MagicMock()
        mock_start = MagicMock()
        mock_task = MagicMock()
        self.reminder_obj.lock = mock_lock
        self.reminder_obj.tasks = []

        self.reminder_obj.lock = mock_lock

        controle_datetime = datetime.datetime(2024, 5, 7, 8, 0)
        mock_datetime.now.return_value = controle_datetime
        mock_datetime.datetime.now.return_value.time.return_value = (
            controle_datetime.time()
        )
        mock_start.time.return_value = controle_datetime.time()

        self.reminder_obj.add_tasks(mock_start, mock_task)
        exp = [(mock_start, mock_task)]

        self.assertIn((mock_start, mock_task), self.reminder_obj.tasks)
        self.assertEqual(exp, self.reminder_obj.tasks)
