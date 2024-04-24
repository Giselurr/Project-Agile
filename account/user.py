"""This module will store the user information and the GUI for the user page"""

from tkinter import Button, Frame, Label, PhotoImage, Tk


class User:
    """The user class will set up a user instance, add GUI and buttons(links)
    to the things a user that is logged in is able to do."""

    def __init__(self, logged_in, user_name, window):
        self.is_logged_in = logged_in
        self.user_name = user_name
        self.window = window

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
            self.window.title(f"Welcome {self.user_name}!")
            user_frame = Frame(self.window)
            user_frame.configure(bg="#040B20")
            Label(
                user_frame,
                text="Welcome " + self.user_name + "!",
                bg="#040B20",
                fg="#FFFFFF",
                font=("Arial", 20),
            ).grid(row=0, column=0)
            Label(user_frame, image=background, border=0).grid(row=1, column=0)
            Button(
                user_frame,
                image=breathe_img,
                borderwidth=0,
                command=lambda: self.redirect("breathe", user_frame),
                highlightthickness=0,
                bd=0,
                padx=0,
                pady=0,
            ).place(x=70, y=60)
            Button(
                user_frame,
                image=scheduel_img,
                borderwidth=0,
                command=lambda: self.redirect("set schedule", user_frame),
                highlightthickness=0,
                bd=0,
                padx=0,
                pady=0,
            ).place(x=82, y=360)
            Button(
                user_frame,
                image=stresslevel_img,
                borderwidth=0,
                command=lambda: self.redirect("set your stress level", user_frame),
                highlightthickness=0,
                bd=0,
                padx=0,
                pady=0,
            ).place(x=221, y=360)
            Label(user_frame, bg="#040B20", text="").grid(row=6)
            Button(
                user_frame,
                image=calendar_img,
                borderwidth=0,
                command=lambda: self.redirect("view your calender", user_frame),
                highlightthickness=0,
                bd=0,
                padx=0,
                pady=0,
            ).place(x=82, y=500)
            Button(
                user_frame,
                image=history_img,
                borderwidth=0,
                command=lambda: self.redirect("stress history", user_frame),
                highlightthickness=0,
                bd=0,
                padx=0,
                pady=0,
            ).place(x=221, y=500)
            user_frame.pack()
        else:
            self.window.title("Not logged in!")
            user_frame = Frame(self.window)
            user_frame.configure(bg="#040B20")
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

    def redirect(self, redirect_to, user_frame):
        user_frame.pack_forget()
        redirect = Frame(self.window)
        redirect.configure(bg="#AFB5D6")
        Label(redirect, bg="#AFB5D6", text="").grid(row=0)
        Label(
            redirect,
            text="Redirecting to the " + redirect_to + ".",
            bg="#040B20",
            fg="#AFB5D6",
            font=("Arial", 12),
        ).grid(row=1, column=0)
        redirect.pack()


if __name__ == "__main__":
    window = Tk()
    user = User(True, "Pernilla", window)
    user.user_gui()
