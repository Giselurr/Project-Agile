"""This module will store the user information and the GUI for the user page"""

from tkinter import Button, Frame, Label


class User:
    """The user class will set up a user instance, add GUI and buttons(links)
    to the things a user that is logged in is able to do."""

    def __init__(self, logged_in, user_name, window):
        self.is_logged_in = logged_in
        self.user_name = user_name
        self.window = window

    def user_gui(self):
        """The interface for a logged in user."""
        self.window.geometry("640x540")
        self.window.resizable(height=True, width=False)
        self.window.config(bg="#040B20")
        if self.is_logged_in:
            self.window.title(f"Welcome {self.user_name}!")
            user_frame = Frame(self.window)
            user_frame.configure(bg="#040B20")
            Label(user_frame, bg="#040B20", text="").grid(row=0)
            Label(
                user_frame,
                text="Welcome " + self.user_name + ", what would you like to do? ",
                bg="#040B20",
                fg="#76ADCF",
                font=("Arial", 18),
            ).grid(row=1, column=0, columnspan=4)
            Label(user_frame, bg="#040B20", text="").grid(row=2)
            Button(
                user_frame,
                text="BREATHE",
                bg="#76ADCF",
                fg="#040B20",
                font=("Arial", 20, "bold"),
                width="25",
                height="2",
            ).grid(row=3, column=0, columnspan=4)
            Label(user_frame, bg="#040B20", text="").grid(row=4)
            Button(
                user_frame,
                text="Set schedule",
                bg="#76ADCF",
                fg="#040B20",
                font=("Arial", 15, "bold"),
                width="16",
            ).grid(row=5, column=0, columnspan=2)
            Button(
                user_frame,
                text="Set you stresslevel",
                bg="#76ADCF",
                fg="#040B20",
                font=("Arial", 15, "bold"),
                width="16",
            ).grid(row=5, column=2, columnspan=2)
            Label(user_frame, bg="#040B20", text="").grid(row=6)
            Button(
                user_frame,
                text="View your calender",
                bg="#76ADCF",
                fg="#040B20",
                font=("Arial", 15, "bold"),
                width="16",
            ).grid(row=7, column=0, columnspan=2)
            Button(
                user_frame,
                text="Stress history",
                bg="#76ADCF",
                fg="#040B20",
                font=("Arial", 15, "bold"),
                width="16",
            ).grid(row=7, column=2, columnspan=2)
            user_frame.pack()
        else:
            self.window.title("Not logged in!")
            user_frame = Frame(self.window)
            user_frame.configure(bg="#040B20")
            Label(user_frame, bg="#040B20", text="").grid(row=0)
            Label(
                user_frame,
                text="Please go back and login to your accout ",
                bg="#040B20",
                fg="#76ADCF",
                font=("Arial", 18),
            ).grid(row=1, column=0, columnspan=4)
            user_frame.pack()
        self.window.mainloop()
