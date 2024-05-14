"""Main module that creates the original window that gets passed around.
Also contains the redirect manager for the program."""

from tkinter import Tk

from account import login, main_menu, register, settings, user
from breathing import boxbreathing
from schedule import (
    calendar,
    daily_schedule,
    scale,
    stress_history,
)


class Main:
    def __init__(self, window):
        """Init Main."""
        self.window = window

    def start_main_window(self):
        """Start the main menu window."""
        main_window = main_menu.MainMenu(self.window)
        main_window.main_gui()

    def manager_menu_choice(self, frame, menu_choice, user_name, date, reminder):
        """Handles all the redirects and frame forgets for all windows."""
        if frame is not None:
            frame.pack_forget()
        if menu_choice == "MAIN_MENU":
            main_menu_redirect = main_menu.MainMenu(self.window)
            main_menu_redirect.main_gui()
        elif menu_choice == "LOGIN":
            login_redirect = login.Login(self.window)
            login_redirect.login_gui()
        elif menu_choice == "REGISTER":
            register_redirect = register.Register(self.window)
            register_redirect.register_gui()
        elif menu_choice == "USER_MENU":
            user_redirect = user.User(True, user_name, self.window)
            user_redirect.user_gui()
        elif menu_choice == "BREATHE":
            breath_redirect = boxbreathing.DisplayExercise(
                self.window, user_name, reminder
            )
            (breath_redirect.display_imagery(),)
        elif menu_choice == "SCHEDULE":
            schedule = daily_schedule.DailyScheduele(
                self.window, user_name, date, reminder
            )
            schedule.daily_schedule_gui()

        elif menu_choice == "STRESS_LEVEL":
            stress_level_redirect = scale.Scale(self.window, user_name, date, reminder)
            stress_level_redirect.scale_gui()

        elif menu_choice == "CALENDAR":
            frame.pack_forget()
            calendar_redirect = calendar.CalendarInt(
                self.window, user_name, date, reminder
            )
            calendar_redirect.calendar_gui()

        elif menu_choice == "STRESS_HISTORY":
            stress_history_redirect = stress_history.History(self.window, user_name)
            stress_history_redirect.draw_stress_history()
        elif menu_choice == "USER_SETTINGS":
            user_settings_redirect = settings.UserSettings(True, user_name, self.window)
            user_settings_redirect.user_setting_gui()
        else:
            print("ERROR IN REDIRECT!")


if __name__ == "__main__":
    window = Tk()
    main = Main(window)
    main.start_main_window()
