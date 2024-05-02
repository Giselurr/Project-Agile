"""Main module that creates the original window that gets passed around.
Also contains the redirect manager for the program."""

from tkinter import Tk

from account import login, main_menu, register, user
from breathing import boxbreathing
from schedule import scale  # calander, clock, dailynote,


class Main:
    def __init__(self, window):
        """Init Main."""
        self.window = window

    def start_main_window(self):
        """Start the main menu window."""
        main_window = main_menu.MainMenu(self.window)
        main_window.main_gui()

    def manager_menu_choice(self, frame, menu_choice, user_name):
        """Handles all the redirects and frame forgets for all windows."""
        # Might want to add "frame.pack_forget()" here if all of the options do it.
        if menu_choice == "MAIN_MENU":
            # Redirect to main menu (might not be needed).
            # Might use start_main_window()
            print("MAIN_MENU")
        elif menu_choice == "LOGIN":
            frame.pack_forget()
            login_redirect = login.Login(self.window)
            login_redirect.login_gui()
        elif menu_choice == "REGISTER":
            frame.pack_forget()
            register_redirect = register.Register(self.window)
            register_redirect.register_gui()
        elif menu_choice == "LOG_OUT":
            # Redirect to log out (might be merged with MAIN_MENU).
            print("LOG_OUT")
        elif menu_choice == "USER_MENU":
            frame.pack_forget()
            user_redirect = user.User(True, user_name, self.window)
            user_redirect.user_gui()
        elif menu_choice == "BREATHE":
            frame.pack_forget()
            breath_redirect = boxbreathing.DisplayExercise(self.window, user_name)
            breath_redirect.display_imagery()
        elif menu_choice == "SCHEDULE":
            # Redirect to schedule.
            print("SCHEDULE")
        elif menu_choice == "STRESS_LEVEL":
            frame.pack_forget()
            stress_level_redirect = scale.Scale(self.window, user_name)
            stress_level_redirect.scale_gui()
        elif menu_choice == "CALENDAR":
            # Redirect to calendar.
            print("CALENDAR")
        elif menu_choice == "STRESS_HISTORY":
            # Redirect to stress history.
            print("STRESS_HISTORY")


if __name__ == "__main__":
    window = Tk()
    main = Main(window)
    main.start_main_window()
