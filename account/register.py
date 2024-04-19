"""This module will use a tikinte GUI interface and use a mysql connection
so that a user can register to this application."""

from tkinter import NSEW, Button, E, Entry, Frame, Label, StringVar, Tk, Toplevel, W

import bcrypt

from database import db_connects


class Register:
    """This class register a user to this application."""

    window = Tk()

    def __init__(self):
        """Initializing the window for the GUI"""
        self.window.geometry("640x540")
        self.window.resizable(height=True, width=False)
        self.window.config(bg="#040B20")
        self.window.title("Please register your account.")
        self.db_connects = db_connects.DbConnnects()

    def register_gui(self):
        """The Graphical interface for the user register"""
        register_frame = Frame(self.window)
        register_frame.configure(bg="#040B20")
        Label(
            register_frame,
            text="Register your new account",
            bg="#040B20",
            fg="#29FF2C",
            font=("Arial", 15),
        ).grid(row=0, column=0, columnspan=3, sticky=NSEW)
        Label(register_frame, text="", bg="#040B20").grid(row=1, column=1, columnspan=3)
        first_name = StringVar()
        Label(
            register_frame,
            text="Your first name:",
            bg="#040B20",
            fg="#29FF2C",
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
            fg="#29FF2C",
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
            fg="#29FF2C",
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
            fg="#29FF2C",
            font=("Arial", 14),
        ).grid(row=8, column=0, ipady=8, sticky=E)
        Entry(register_frame, textvariable=password, width=30, font=("Arial", 13)).grid(
            row=8, column=2, ipady=8
        )
        Label(register_frame, text="", bg="#040B20").grid(row=9, column=1, columnspan=3)
        Button(
            register_frame,
            text="REGISTER",
            bg="#29FF2C",
            fg="#040B20",
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
        pop = Toplevel(register_frame)
        first_name = first_name.get()
        last_name = last_name.get()
        user_name = user_name.get()
        password = password.get().encode("utf-8")
        hashed_password = self.salt_hash(password)
        if self.db_connects.check_user_name(user_name):
            query = (
                "INSERT INTO user (first_name, last_name, user_name, password)"
                "VALUES (%s, %s, %s, %s)"
            )
            values = (first_name, last_name, user_name, hashed_password)
            self.cursor.execute(query, values)
            if self.cursor.rowcount == 1:
                self.my_con.commit()
                pop.title("Register successful1")
                Label(pop, text="Registered user successfully!").pack()
            else:
                pop.title("Register unsuccesfull!")
                Label(pop, text="Please try again!").pack()
        else:
            pop.title("Register unsuccesfull!")
            Label(pop, text="Please try again!").pack()

    def salt_hash(self, password):
        """This will transform their password to an encrypte version."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        return hashed


reg = Register()
reg.register_gui()
