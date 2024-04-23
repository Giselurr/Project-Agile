"""A module that will be the user interface when not logged in."""

from tkinter import Button, Frame, Label, Tk

from account import login, register


class Main:
    """This class will handle the user GUI whe he/she is not logged in."""

    def __init__(self, window):
        """Initiates the window."""
        self.window = window
        self.window.geometry("640x540")
        self.window.resizable(height=True, width=False)
        self.window.configure(bg="#AFB5D6")

    def main_gui(self):
        main_frame = Frame(self.window)
        main_frame.configure(bg="#AFB5D6")
        Label(main_frame, text="", bg="#AFB5D6").grid(row=0)
        Label(
            main_frame,
            text="Welcome to BREATHE - ",
            bg="#AFB5D6",
            fg="#040B20",
            font=("Century Schoolbook", 25, "bold"),
        ).grid(row=1, column=0, columnspan=4)
        Label(main_frame, text="", bg="#AFB5D6").grid(row=0)
        Label(
            main_frame,
            text="an application that will help you find your calm",
            bg="#AFB5D6",
            fg="#040B20",
            font=("Century Schoolbook", 15, "bold"),
        ).grid(row=2, column=0, columnspan=4)
        Label(main_frame, text="", bg="#AFB5D6").grid(row=3)
        Button(
            main_frame,
            text="Register an account",
            bg="#040B20",
            fg="#AFB5D6",
            font=("Century Schoolbook", 15, "bold"),
            relief="flat",
            command=lambda: self.register_user(main_frame),
            highlightbackground="#FFFFFF",
            border=1,
        ).grid(row=4, column=0, columnspan=4)
        Label(main_frame, text="", bg="#AFB5D6").grid(row=5)
        Button(
            main_frame,
            text="Login",
            bg="#040B20",
            fg="#AFB5D6",
            command=lambda: self.login_user(main_frame),
            font=("Century Schoolbook", 15, "bold"),
            relief="flat",
            highlightbackground="#FFFFFF",
            border=1,
        ).grid(row=6, column=0, columnspan=4)
        main_frame.pack()
        self.window.mainloop()

    def register_user(self, main_frame):
        main_frame.pack_forget()
        reg = register.Register(self.window)
        reg.register_gui()

    def login_user(self, main_frame):
        main_frame.pack_forget()
        log = login.Login(self.window)
        log.login_gui()


if __name__ == "__main__":
    window = Tk()
    main = Main(window)
    main.main_gui()
