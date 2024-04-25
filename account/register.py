"""This module will use a tikinte GUI interface and use a mysql connection
so that a user can register to this application."""

from tkinter import NSEW, Button, E, Entry, Frame, Label, StringVar, W

import bcrypt

from account import login
from database import database_connection, database_handler


class Register:
    """This class register a user to this application."""

    def __init__(self, window):
        """Initializing the window for the GUI"""
        self.window = window
        self.window.geometry("640x540")
        self.window.resizable(height=True, width=False)
        self.window.config(bg="#040B20")
        self.window.title("Please register your account.")
        self.db_handler = database_handler.DatabaseHandler()
        self.database = database_connection.DatabaseConnection(
            "root", "KamelKatt3801"
        )  # Change to your db username and password.  # noqa: E501

    def register_gui(self):
        """The Graphical interface for the user register"""
        register_frame = Frame(self.window)
        register_frame.configure(bg="#040B20")
        Label(
            register_frame,
            text="Register your new account",
            bg="#040B20",
            fg="#AFB5D6",
            font=("Arial", 15),
        ).grid(row=0, column=0, columnspan=3, sticky=NSEW)
        Label(register_frame, text="", bg="#040B20").grid(row=1, column=1, columnspan=3)
        first_name = StringVar()
        Label(
            register_frame,
            text="Your first name:",
            bg="#040B20",
            fg="#AFB5D6",
            font=("Arial", 14),
        ).grid(row=2, column=0, ipady=8, sticky=E)
        Entry(
            register_frame, textvariable=first_name, width=30, font=("Arial", 13)
        ).grid(row=2, column=2, ipady=8)
        Label(register_frame, text="", bg="#040B20").grid(row=3, column=1, columnspan=3)
        last_name = StringVar()
        Label(
            register_frame,
            text="Your last name:",
            bg="#040B20",
            fg="#AFB5D6",
            font=("Arial", 14),
        ).grid(row=4, column=0, ipady=8, sticky=E)
        Entry(
            register_frame, textvariable=last_name, width=30, font=("Arial", 13)
        ).grid(row=4, column=2, ipady=8)
        Label(register_frame, text="", bg="#040B20").grid(row=5, column=1, columnspan=3)
        user_name = StringVar()
        Label(
            register_frame,
            text="Your user name:",
            bg="#040B20",
            fg="#AFB5D6",
            font=("Arial", 14),
        ).grid(row=6, column=0, ipady=8, sticky=W)
        Entry(
            register_frame, textvariable=user_name, width=30, font=("Arial", 13)
        ).grid(
            row=6,
            column=2,
            ipady=8,
        )
        Label(register_frame, text="", bg="#040B20").grid(row=7, column=1, columnspan=3)
        password = StringVar()
        Label(
            register_frame,
            text="Your password:",
            bg="#040B20",
            fg="#AFB5D6",
            font=("Arial", 14),
        ).grid(row=8, column=0, ipady=8, sticky=E)
        Entry(register_frame, textvariable=password, width=30, font=("Arial", 13)).grid(
            row=8, column=2, ipady=8
        )
        Label(register_frame, text="", bg="#040B20").grid(row=9, column=1, columnspan=3)
        Button(
            register_frame,
            text="REGISTER",
            bg="#040B20",
            fg="#AFB5D6",
            width=30,
            height=3,
            command=lambda: self.register_user(
                first_name, last_name, user_name, password, register_frame
            ),
        ).grid(row=10, column=0, columnspan=3)
        register_frame.pack()
        self.window.mainloop()

    def register_user(self, first_name, last_name, user_name, password, register_frame):
        """This method will get the users name from the GUI
        and add their information to the DB."""
        first_name = first_name.get()
        last_name = last_name.get()
        user_name = user_name.get()
        password = password.get().encode("utf-8")
        hashed_password = self.salt_hash(password)
        user_exists = self.db_handler.check_user_name(user_name)
        if not user_exists:
            self.cursor = self.database.connect()
            try:
                query = (
                    "INSERT INTO user (first_name, last_name, user_name, password)"
                    "VALUES (%s, %s, %s, %s)"
                )
                values = (first_name, last_name, user_name, hashed_password)
                self.cursor.execute(query, values)
                if self.cursor.rowcount == 1:
                    self.database.commit()
                    register_frame.pack_forget()
            finally:
                self.cursor.close()
                log = login.Login(self.window)
                log.login_gui()
        else:
            Label(
                register_frame,
                text="The user already exists, please try again!",
                bg="#040B20",
                fg="#AFB5D6",
                font=("Arial", 14),
            ).grid(row=12, column=0, columnspan=3, ipady=10)

    def salt_hash(self, password):
        """This will transform their password to an encrypte version."""
        if isinstance(password, str):
            password = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        return hashed
