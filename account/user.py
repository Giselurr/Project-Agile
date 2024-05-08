"""This module will store the user information and the GUI for the user page"""

from datetime import datetime
from tkinter import Button, Frame, Label, PhotoImage, Tk, Toplevel

import main


class User:
    """The user class will set up a user instance, add GUI and buttons(links)
    to the things a user that is logged in is able to do."""

    def __init__(self, logged_in, user_name, window):
        self.is_logged_in = logged_in
        self.user_name = user_name
        self.window = window
        self.window.title("Breathe")
        self.window.iconbitmap("account\images\Breathe_icon.ico")

    def user_gui(self):
        """The interface for a logged in user."""
        self.window.geometry("640x700")
        self.window.resizable(height=True, width=False)
        self.window.config(bg="#040B20")
        if self.is_logged_in:
            background = PhotoImage(file="account\images\Background.png")
            breathe_img = PhotoImage(file="account\images/Breathe_Lungs_Icon.png")
            scheduel_img = PhotoImage(file="account\images/schedule.png")
            stresslevel_img = PhotoImage(file="account\images\Set_levels.png")
            calendar_img = PhotoImage(file="account\images/calender.png")
            history_img = PhotoImage(file="account\images/history.png")
            sign_out_img = PhotoImage(file="account\images\sign_out.png")
            user_settings_img = PhotoImage(file="account\images/user_settings.png")
            user_frame = Frame(self.window)
            user_frame.configure(bg="#040B20")
            left_buttons = Frame(self.window, bg="#FFFFFF")
            Label(
                user_frame,
                text="Welcome " + self.user_name + "!",
                bg="#040B20",
                fg="#FFFFFF",
                font=("Arial", 20),
            ).grid(row=0, column=0)
            Label(user_frame, image=background, border=0).grid(row=1, column=0)
            Button(
                left_buttons,
                image=sign_out_img,
                activebackground="#040B20",
                borderwidth=0,
                command=lambda: self.sign_out(user_frame, left_buttons),
                highlightthickness=0,
                bd=0,
                padx=0,
                pady=0,
            ).pack()
            Button(
                left_buttons,
                image=user_settings_img,
                activebackground="#040B20",
                borderwidth=0,
                command=lambda: self.redirect_to_user_settings(
                    user_frame, left_buttons
                ),
                highlightthickness=0,
                bd=0,
                padx=0,
                pady=0,
            ).pack()
            left_buttons.place(x=1, y=50)
            Label(user_frame, image=background, border=0).grid(row=1, column=0)
            Button(
                user_frame,
                image=breathe_img,
                activebackground="#040B20",
                borderwidth=0,
                command=lambda: self.redirect_to_main(
                    user_frame, "BREATHE", left_buttons
                ),
                highlightthickness=0,
                bd=0,
                padx=0,
                pady=0,
            ).place(x=70, y=60)
            Button(
                user_frame,
                image=scheduel_img,
                activebackground="#040B20",
                borderwidth=0,
                command=lambda: self.redirect_to_main(
                    user_frame, "SCHEDULE", left_buttons
                ),
                highlightthickness=0,
                bd=0,
                padx=0,
                pady=0,
            ).place(x=82, y=360)
            Button(
                user_frame,
                image=stresslevel_img,
                activebackground="#040B20",
                borderwidth=0,
                command=lambda: self.redirect_to_main(
                    user_frame, "STRESS_LEVEL", left_buttons
                ),
                highlightthickness=0,
                bd=0,
                padx=0,
                pady=0,
            ).place(x=221, y=360)
            Label(user_frame, bg="#040B20", text="").grid(row=6)
            Button(
                user_frame,
                image=calendar_img,
                activebackground="#040B20",
                borderwidth=0,
                command=lambda: self.redirect_to_main(
                    user_frame, "CALENDAR", left_buttons
                ),
                highlightthickness=0,
                bd=0,
                padx=0,
                pady=0,
            ).place(x=82, y=500)
            Button(
                user_frame,
                image=history_img,
                activebackground="#040B20",
                borderwidth=0,
                command=lambda: self.redirect_to_main(
                    user_frame, "STRESS_HISTORY", left_buttons
                ),
                highlightthickness=0,
                bd=0,
                padx=0,
                pady=0,
            ).place(x=221, y=500)
            user_frame.pack()
        else:
            user_frame = Frame(self.window, bg="#040B20")
            Label(user_frame, bg="#040B20", text="").grid(row=0)
            Label(
                user_frame,
                text="Please go back and login to your accout ",
                bg="#AFB5D6",
                fg="#040B20",
                font=("Arial", 18),
            ).grid(row=1, column=0, columnspan=4)
            user_frame.pack()
        self.window.mainloop()

    def redirect_to_main(self, user_frame, choise, left_buttons):
        left_buttons.destroy()
        main.Main.manager_menu_choice(
            self, user_frame, choise, self.user_name, datetime.now()
        )

    def sign_out(self, user_frame, left_buttons):
        """Sign out pop-up window with Y/N."""
        self.no_img = PhotoImage(file="account\images/no.png")
        self.yes_img = PhotoImage(file="account\images\yes.png")
        self.top = Toplevel()
        self.top.geometry("280x200")
        self.top.title("Breathe")
        self.top.iconbitmap("account\images\Breathe_icon.ico")
        self.top.resizable(height=False, width=False)
        self.top.configure(bg="#040B20")
        Label(
            self.top,
            text="Do you want to sign out?",
            bg="#040B20",
            fg="#FFFFFF",
            font=("Arial", 16),
        ).pack(pady=40)
        Button(
            self.top,
            image=self.no_img,
            activebackground="#040B20",
            borderwidth=0,
            command=lambda: self.return_to_user_page(user_frame, True),
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=15, y=90)
        Button(
            self.top,
            image=self.yes_img,
            activebackground="#040B20",
            borderwidth=0,
            command=lambda: self.return_to_main_page(user_frame, left_buttons, True),
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=145, y=90)

    def return_to_user_page(self, frame, close_popup):
        """Button action for return to the user page."""
        if close_popup:
            self.top.destroy()
        main.Main.manager_menu_choice(self, frame, "USER_MENU", self.user_name, None)

    def return_to_main_page(self, frame, left_buttons, close_popup):
        """Return to the main menu."""
        left_buttons.place_forget()
        if close_popup:
            self.top.destroy()
        main.Main.manager_menu_choice(self, frame, "MAIN_MENU", self.user_name, None)

    def redirect_to_user_settings(self, frame, left_buttons):
        """Redirects to the user settings page."""
        left_buttons.place_forget()
        main.Main.manager_menu_choice(
            self, frame, "USER_SETTINGS", self.user_name, None
        )


if __name__ == "__main__":
    window = Tk()
    user = User(True, "Pernilla", window)
    user.user_gui()
