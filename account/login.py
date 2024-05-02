"""This module will use a tikinter GUI interface
so that a user can login to this application."""

from tkinter import Button, Entry, Frame, Label, PhotoImage, StringVar, W

import bcrypt

import main
from database import database_handler


class Login:
    """This class will login the user."""

    def __init__(self, window):
        """Initializing the class it starts the GUI and the db connection."""
        self.window = window
        self.window.geometry("640x700")
        self.window.resizable(height=True, width=False)
        self.window.config(bg="#040B20")
        self.window.title("Breathe")
        self.db_handler = database_handler.DatabaseHandler()

    def login_gui(self):
        """This is the login graphical interface."""
        login_frame = Frame(self.window)
        login_frame.configure(bg="#040B20")
        login_button = PhotoImage(file="account\images\Login.png")
        Label(
            login_frame,
            text="USER LOGIN",
            font=("Arial", 20, "bold"),
            bg="#040B20",
            fg="#AFB5D6",
        ).grid(row=0, column=0, columnspan=3, pady=15)
        user_name = StringVar()
        Label(
            login_frame,
            text="User Name:",
            font=("Arial", 14),
            bg="#040B20",
            fg="#AFB5D6",
        ).grid(row=2, column=0, pady=15)
        Entry(login_frame, font=("Arial", 20), textvariable=user_name).grid(
            row=2, column=2, sticky=W
        )
        password = StringVar()
        Label(
            login_frame,
            text="Password:",
            font=("Arial", 14),
            bg="#040B20",
            fg="#AFB5D6",
        ).grid(row=4, column=0, pady=15)
        Entry(login_frame, font=("Arial", 20), textvariable=password, show="*").grid(
            row=4, column=2, sticky=W
        )
        Button(
            login_frame,
            image=login_button,
            border=0,
            highlightthickness=0,
            pady=0,
            padx=0,
            command=lambda: self.login_user(user_name, password, login_frame),
        ).grid(row=6, column=0, columnspan=3, pady=10)
        login_frame.pack()
        self.window.mainloop()

    def login_user(self, user_name, password, login_frame):
        """Checks the password and compares it with the
        hashed password from the database."""
        user_name = user_name.get()
        password = password.get().encode("utf-8")
        hashed = self.db_handler.get_hashed_pass(user_name)
        if hashed and bcrypt.checkpw(password, hashed.encode("utf-8")):
            main.Main.manager_menu_choice(self, login_frame, "USER_MENU", user_name, "")
        else:
            Label(
                login_frame,
                text="Wrong username or password",
                font=("Arial", 14),
                bg="#040B20",
                fg="#78CBFF",
            ).grid(row=8, column=0, columnspan=3, pady=5)
