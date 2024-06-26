"""A module that will be the user interface when not logged in."""

from tkinter import Button, Frame, Label, PhotoImage

import main


class MainMenu:
    """This class will handle the user GUI when he/she is not logged in."""

    def __init__(self, window):
        """Initiates the window."""
        self.window = window
        self.window.resizable(height=False, width=False)
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - 640) // 2
        y = (screen_height - 700) // 2
        self.window.geometry(f"640x700+{x}+{y}")
        self.window.configure(bg="#040B20")
        self.window.title("Breathe")
        self.window.iconbitmap("account\images\Breathe_icon.ico")

    def main_gui(self):
        """Main menu window with selection between register and login."""
        main_frame = Frame(self.window)
        main_frame.configure(bg="#040B20")
        logo = PhotoImage(file="account\images\Logo.png")
        login = PhotoImage(file="account\images\Login.png")
        register = PhotoImage(file="account\images\Register.png")
        Label(main_frame, text="", bg="#040B20").grid(row=0)

        Label(main_frame, text="", bg="#040B20").grid(row=0)
        Label(main_frame, image=logo, border=0).grid(row=2, column=0, columnspan=4)
        Label(main_frame, text="", bg="#040B20").grid(row=3)
        Button(
            main_frame,
            image=register,
            command=lambda: main.Main.manager_menu_choice(
                self, main_frame, "REGISTER", None, None, None
            ),
            activebackground="#040B20",
            border=0,
            highlightthickness=0,
            pady=0,
            padx=0,
        ).grid(row=4, column=0, columnspan=2)
        Button(
            main_frame,
            image=login,
            command=lambda: main.Main.manager_menu_choice(
                self, main_frame, "LOGIN", None, None, None
            ),
            activebackground="#040B20",
            border=0,
            highlightthickness=0,
            pady=0,
            padx=0,
        ).grid(row=4, column=2, columnspan=2)
        main_frame.pack()
        self.window.mainloop()
