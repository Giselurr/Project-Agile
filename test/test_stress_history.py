"""This tests the History class."""

import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from schedule import stress_history


class TestHistory(unittest.TestCase):
    """This class tests the non gui part of the history class."""

    def setUp(self):
        """Set up the test."""
        self.mock_user = MagicMock()
        self.mock_window = MagicMock()

    def test_calculate_current_week(self):
        """Test calculate_current_week."""
        history = stress_history.History(self.mock_user, self.mock_window)
        history.current_date = datetime.now()
        history.calculate_current_week()

        self.assertEqual(
            history.monday_date,
            history.current_date
            - timedelta(days=history.current_date.isoweekday() - 1),
        )
        self.assertEqual(history.tuesday_date, history.monday_date + timedelta(days=1))
        self.assertEqual(
            history.wednesday_date, history.monday_date + timedelta(days=2)
        )
        self.assertEqual(history.thursday_date, history.monday_date + timedelta(days=3))
        self.assertEqual(history.friday_date, history.monday_date + timedelta(days=4))
        self.assertEqual(history.saturday_date, history.monday_date + timedelta(days=5))
        self.assertEqual(history.sunday_date, history.monday_date + timedelta(days=6))

    def test_calculate_next_week(self):
        """Test calculate_next_week."""
        history = stress_history.History(self.mock_user, self.mock_window)
        history.current_date = datetime.now()
        history.calculate_current_week()
        old_dates = (
            history.monday_date,
            history.tuesday_date,
            history.wednesday_date,
            history.thursday_date,
            history.friday_date,
            history.saturday_date,
            history.sunday_date,
        )
        history.calculate_next_week()

        for i, date in enumerate(
            (
                history.monday_date,
                history.tuesday_date,
                history.wednesday_date,
                history.thursday_date,
                history.friday_date,
                history.saturday_date,
                history.sunday_date,
            )
        ):
            self.assertEqual(date, old_dates[i] + timedelta(days=7))

    def test_calculate_previous_week(self):
        """Test calculate_previous_week."""
        history = stress_history.History(self.mock_user, self.mock_window)
        history.current_date = datetime.now()
        history.calculate_current_week()
        old_dates = (
            history.monday_date,
            history.tuesday_date,
            history.wednesday_date,
            history.thursday_date,
            history.friday_date,
            history.saturday_date,
            history.sunday_date,
        )
        history.calculate_previous_week()

        for i, date in enumerate(
            (
                history.monday_date,
                history.tuesday_date,
                history.wednesday_date,
                history.thursday_date,
                history.friday_date,
                history.saturday_date,
                history.sunday_date,
            )
        ):
            self.assertEqual(date, old_dates[i] - timedelta(days=7))

    def test_change_week(self):
        """Test change_week."""
        history = stress_history.History(self.mock_user, self.mock_window)
        history.calculate_next_week = MagicMock()
        history.calculate_previous_week = MagicMock()
        history.draw_stress_history = MagicMock()
        history.draw_notes_page = MagicMock()

        history.change_week("NEXT", "BARCHART")
        history.calculate_next_week.assert_called_once()
        history.draw_stress_history.assert_called_once()
        history.draw_notes_page.assert_not_called()

        history.calculate_next_week.reset_mock()
        history.calculate_previous_week.reset_mock()
        history.draw_stress_history.reset_mock()
        history.draw_notes_page.reset_mock()

        history.change_week("NEXT", "NOTES")
        history.calculate_next_week.assert_called_once()
        history.draw_notes_page.assert_called_once()
        history.draw_stress_history.assert_not_called()

        history.calculate_next_week.reset_mock()
        history.calculate_previous_week.reset_mock()
        history.draw_stress_history.reset_mock()
        history.draw_notes_page.reset_mock()

        history.change_week("PREVIOUS", "BARCHART")
        history.calculate_previous_week.assert_called_once()
        history.draw_stress_history.assert_called_once()
        history.draw_notes_page.assert_not_called()

        history.calculate_next_week.reset_mock()
        history.calculate_previous_week.reset_mock()
        history.draw_stress_history.reset_mock()
        history.draw_notes_page.reset_mock()

        history.change_week("PREVIOUS", "NOTES")
        history.calculate_previous_week.assert_called_once()
        history.draw_notes_page.assert_called_once()
        history.draw_stress_history.assert_not_called()

    @patch("schedule.stress_history.History.draw_stress_history")
    def test_return_to_barchart(self, mock_draw_stress_history):
        """Test return_to_barchart."""
        history = stress_history.History(self.mock_user, self.mock_window)
        mock_barchart_canvas = MagicMock()
        mock_notes_canvas = MagicMock()
        history.barchart_canvas = mock_barchart_canvas
        history.notes_canvas = mock_notes_canvas

        history.return_to_barchart()

        mock_notes_canvas.delete.assert_called_with("all")
        mock_notes_canvas.pack_forget.assert_called_once()
        mock_barchart_canvas.pack.assert_called_once()
        mock_draw_stress_history.assert_called_once()

    @patch("schedule.stress_history.History.draw_notes_page")
    def test_prepare_notes_page(self, mock_draw_notes_page):
        """Test prepare_notes_page."""
        history = stress_history.History(self.mock_user, self.mock_window)
        mock_barchart_canvas = MagicMock()
        mock_notes_canvas = MagicMock()
        history.barchart_canvas = mock_barchart_canvas
        history.notes_canvas = mock_notes_canvas

        history.prepare_notes_page()

        mock_barchart_canvas.pack_forget.assert_called_once()
        mock_notes_canvas.pack.assert_called_once()
        mock_draw_notes_page.assert_called_with(False)

    @patch("schedule.stress_history.History.draw_notes_dates")
    @patch("schedule.stress_history.History.draw_click_button_text")
    @patch("schedule.stress_history.History.draw_notes_buttons")
    def test_draw_notes_page_true(
        self,
        mock_draw_notes_buttons,
        mock_draw_click_button_text,
        mock_draw_notes_dates,
    ):
        """Test draw_notes_page with draw_frame set to True."""
        history = stress_history.History(self.mock_user, self.mock_window)
        history.draw_notes_page(True)

        mock_draw_notes_dates.assert_called_once()
        mock_draw_click_button_text.assert_not_called()
        mock_draw_notes_buttons.assert_called_with(True)

    @patch("schedule.stress_history.History.draw_notes_dates")
    @patch("schedule.stress_history.History.draw_click_button_text")
    @patch("schedule.stress_history.History.draw_notes_buttons")
    def test_draw_notes_page_false(
        self,
        mock_draw_notes_buttons,
        mock_draw_click_button_text,
        mock_draw_notes_dates,
    ):
        """Test draw_notes_page with draw_frame set to False."""
        history = stress_history.History(self.mock_user, self.mock_window)
        history.draw_notes_page(False)

        mock_draw_notes_dates.assert_called_once()
        mock_draw_click_button_text.assert_called_once()
        mock_draw_notes_buttons.assert_called_with(False)

    # test_draw_stress_history_current_date only works locally and not on github.

    # @patch("schedule.stress_history.History.calculate_current_week")
    # @patch("schedule.stress_history.History.draw_scale_text")
    # @patch("schedule.stress_history.History.draw_barchart")
    # @patch("schedule.stress_history.History.draw_day_text")
    # @patch("schedule.stress_history.History.draw_current_week_text")
    # @patch("schedule.stress_history.History.draw_buttons")
    # def test_draw_stress_history_current_date(
    #     self,
    #     mock_draw_buttons,
    #     mock_draw_current_week_text,
    #     mock_draw_day_text,
    #     mock_draw_barchart,
    #     mock_draw_scale_text,
    #     mock_calculate_current_week,
    # ):
    #     """Test draw_stress_history with current date being datetime.now()"""
    #     history = stress_history.History(self.mock_user, self.mock_window)
    #     history.draw_stress_history()

    #     mock_draw_buttons.assert_called_once()
    #     mock_draw_current_week_text.assert_called_once()
    #     mock_draw_day_text.assert_called_once()
    #     mock_draw_barchart.assert_called_once()
    #     mock_draw_scale_text.assert_called_once()
    #     mock_calculate_current_week.assert_called_once()

    @patch("schedule.stress_history.History.calculate_current_week")
    @patch("schedule.stress_history.History.draw_scale_text")
    @patch("schedule.stress_history.History.draw_barchart")
    @patch("schedule.stress_history.History.draw_day_text")
    @patch("schedule.stress_history.History.draw_current_week_text")
    @patch("schedule.stress_history.History.draw_buttons")
    def test_draw_stress_history_not_current_date(
        self,
        mock_draw_buttons,
        mock_draw_current_week_text,
        mock_draw_day_text,
        mock_draw_barchart,
        mock_draw_scale_text,
        mock_calculate_current_week,
    ):
        """Test draw_stress_history with current date not being datetime.now()"""
        history = stress_history.History(self.mock_user, self.mock_window)
        history.current_date = "not current date"
        history.draw_stress_history()

        mock_draw_buttons.assert_called_once()
        mock_draw_current_week_text.assert_called_once()
        mock_draw_day_text.assert_called_once()
        mock_draw_barchart.assert_called_once()
        mock_draw_scale_text.assert_called_once()
        mock_calculate_current_week.assert_not_called()


if __name__ == "__main__":
    unittest.main()
