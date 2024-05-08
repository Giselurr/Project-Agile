"""This module will use a tikinte GUI interface and use a mysql connection
so that a user can register to this application."""

from tkinter import NSEW, Button, E, Entry, Frame, Label, PhotoImage, StringVar, W

import main
from database import database_connection, database_handler

from .usernameerror import UsernameError


class Register:
    """This class register a user to this application."""

    def __init__(self, window):
        """Initializing the window for the GUI"""
        self.window = window
        self.window.geometry("640x700")
        self.window.resizable(height=True, width=False)
        self.window.config(bg="#040B20")
        self.window.title("Breathe")
        self.window.iconbitmap("account\images\Breathe_icon.ico")
        self.db_handler = database_handler.DatabaseHandler()
        self.database = database_connection.DatabaseConnection()

    def register_gui(self):
        """The Graphical interface for the user register"""
        register_frame = Frame(self.window)
        register_frame.configure(bg="#040B20")
        register_button = PhotoImage(file="account\images\Register.png")
        Label(
            register_frame,
            text="REGISTER USER",
            bg="#040B20",
            fg="#AFB5D6",
            font=("Arial", 20, "bold"),
        ).grid(row=0, column=0, columnspan=3, sticky=NSEW, pady=15)
        Label(register_frame, text="", bg="#040B20").grid(row=1, column=1, columnspan=3)
        first_name = StringVar()
        Label(
            register_frame,
            text="Your first name:",
            bg="#040B20",
            fg="#AFB5D6",
            font=("Arial", 14),
        ).grid(row=2, column=0, sticky=E)
        Entry(register_frame, textvariable=first_name, font=("Arial", 20)).grid(
            row=2, column=2
        )
        Label(register_frame, text="", bg="#040B20").grid(row=3, column=1, columnspan=3)
        last_name = StringVar()
        Label(
            register_frame,
            text="Your last name:",
            bg="#040B20",
            fg="#AFB5D6",
            font=("Arial", 14),
        ).grid(row=4, column=0, sticky=E)
        Entry(register_frame, textvariable=last_name, font=("Arial", 20)).grid(
            row=4, column=2
        )
        Label(register_frame, text="", bg="#040B20").grid(row=5, column=1, columnspan=3)
        user_name = StringVar()
        Label(
            register_frame,
            text="Your user name:",
            bg="#040B20",
            fg="#AFB5D6",
            font=("Arial", 14),
        ).grid(row=6, column=0, sticky=W)
        Entry(register_frame, textvariable=user_name, font=("Arial", 20)).grid(
            row=6, column=2
        )
        Label(register_frame, text="", bg="#040B20").grid(row=7, column=1, columnspan=3)
        password = StringVar()
        Label(
            register_frame,
            text="Your password:",
            bg="#040B20",
            fg="#AFB5D6",
            font=("Arial", 14),
        ).grid(row=8, column=0, sticky=E)
        register_entry = Entry(
            register_frame,
            show="*",
            textvariable=password,
            font=("Arial", 20),
        )
        register_entry.grid(row=8, column=2)
        register_entry.bind(
            "<Return>",
            lambda event: self.register_user(
                first_name, last_name, user_name, password, register_frame
            ),
        )
        Label(register_frame, text="", bg="#040B20").grid(row=9, column=1, columnspan=3)
        Button(
            register_frame,
            image=register_button,
            activebackground="#040B20",
            border=0,
            highlightthickness=0,
            pady=0,
            padx=0,
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
        password = password.get()
        try:
            self.check_username_conditions(user_name)
            self.check_password_conditions(password)
            password.encode("utf-8")
            hashed_password = self.db_handler.salt_hash(password)
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
                    main.Main.manager_menu_choice(
                        self, register_frame, "LOGIN", user_name, ""
                    )
            else:
                Label(
                    register_frame,
                    text="The user already exists, please try again!",
                    bg="#040B20",
                    fg="#AFB5D6",
                    font=("Arial", 14),
                ).grid(row=12, column=0, columnspan=3, ipady=10)
        except UsernameError as e:
            self.not_valid_username(register_frame, e.value)

    def not_valid_username(self, register_frame, message):
        """Create label to show error message."""
        Label(
            register_frame,
            text=message,
            bg="#040B20",
            fg="#ff0000",
            font=("Arial", 14),
        ).grid(row=12, column=0, columnspan=3, ipady=10)

    def check_username_conditions(self, user_name):
        """Check for unvalid username."""
        if not user_name or user_name.isspace():
            raise UsernameError(
                "Not a valid username!\nUsername cannot contain whitespace"
            )
        if " " in user_name:
            raise UsernameError(
                "Not a valid username!\nUsername cannot contain whitespace"
            )
        if len(user_name) > 12:
            raise UsernameError("Username to long!\nMax 12 letters")

    def check_password_conditions(self, password):
        """Check for unvalid password."""
        if not password or password.isspace():
            raise UsernameError(
                "Not a valid password!\nPassword cannot contain whitespace"
            )
        if " " in password:
            raise UsernameError(
                "Not a valid password!\nPassword cannot contain whitespace"
            )
