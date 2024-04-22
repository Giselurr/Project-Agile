"""This module will use a tikinter GUI interface
so that a user can login to this application."""

from tkinter import Button, Entry, Frame, Label, StringVar, Toplevel, W

import bcrypt

from database import database_handler


class Login:
    """This class will login the user."""

    def __init__(self, window):
        """Initializing the class it starts the GUI and the db connection."""
        self.window = window
        self.window.geometry("640x540")
        self.window.resizable(height=True, width=False)
        self.window.config(bg="#040B20")
        self.window.title("Please login to your account.")
        self.db_handler = database_handler.DatabaseHandler()

    def login_gui(self):
        """This is the login graphical interface."""
        login_frame = Frame(self.window)
        login_frame.configure(bg="#040B20")
        Label(
            login_frame,
            text="Please fill in your login information below",
            font=("Arial", 14),
            bg="#040B20",
            fg="#78CBFF",
        ).grid(row=0, column=0, columnspan=3, pady=15)
        user_name = StringVar()
        Label(
            login_frame,
            text="User Name:",
            font=("Arial", 14),
            bg="#040B20",
            fg="#76ADCF",
        ).grid(row=2, column=0, pady=15)
        Entry(login_frame, font=("Courier", 14), textvariable=user_name).grid(
            row=2, column=2, sticky=W
        )
        password = StringVar()
        Label(
            login_frame,
            text="Password:",
            font=("Arial", 14),
            bg="#040B20",
            fg="#64CEF0",
        ).grid(row=4, column=0, pady=15)
        Entry(login_frame, font=("Arial", 14), textvariable=password).grid(
            row=4, column=2, sticky=W
        )
        Button(
            login_frame,
            text="LOGIN",
            bg="#78CBFF",
            fg="#040B20",
            height=1,
            width=20,
            font=("Arial", 14),
            command=lambda: self.login_user(user_name, password, login_frame),
        ).grid(row=6, column=0, columnspan=3)
        login_frame.pack()
        self.window.mainloop()

    def login_user(self, user_name, password, login_frame):
        """Checks the password and compares it with the
        hashed password from the database."""
        pop_up = Toplevel(login_frame)
        user_name = user_name.get()
        password = password.get().encode("utf-8")
        hashed = self.db_handler.get_hashed_pass(user_name)
        if hashed and bcrypt.checkpw(password, hashed.encode("utf-8")):
            pop_up.title("Login successfull!")
            Label(
                pop_up,
                text="Login Successfull!",
                font=("Arial", 15),
                bg="#040B20",
                fg="#8ddf00",
            ).pack()
            login_frame.pack_forget()
        else:
            pop_up.title("Login not successful!")
            Label(
                pop_up,
                text="The login was unsuccessfull!",
                font=("Arial", 15),
                bg="#040B20",
                fg="#8ddf00",
            ).pack()
