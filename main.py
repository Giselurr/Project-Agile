from tkinter import Tk

from account import login, main_menu, register, user

# from breathing import boxbreathing
# from schedule import calander, clock, dailynote, scale


class Main:
    def __init__(self, window):
        self.window = window

    def start_main_window(self):
        main_window = main_menu.MainMenu(self.window)
        main_window.main_gui()

    def manager_menu_choice(self, frame, menu_choice, user_name):
        if menu_choice == "MAIN_MENU":
            # Redirect to main menu (might not be needed).
            print("MAIN_MENU")
        elif menu_choice == "LOGIN":
            frame.pack_forget()
            log = login.Login(self.window)
            log.login_gui()
        elif menu_choice == "REGISTER":
            frame.pack_forget()
            reg = register.Register(self.window)
            reg.register_gui()
        elif menu_choice == "LOG_OUT":
            # Redirect to log out (might be merged with MAIN_MENU).
            print("LOG_OUT")
        elif menu_choice == "USER_MENU":
            frame.pack_forget()
            logged_in_user = user.User(True, user_name, self.window)
            logged_in_user.user_gui()
        elif menu_choice == "BREATHE":
            # Redirect to breathe.
            print("BREATHE")
        elif menu_choice == "SCHEDULE":
            # Redirect to schedule.
            print("SCHEDULE")
        elif menu_choice == "STRESS_LEVEL":
            # Redirect to stress level.
            print("STRESS_LEVEL")
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
