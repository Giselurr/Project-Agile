"""This module will show scale and connect with database to store the stress level."""

from datetime import datetime
from tkinter import Button, Frame, Label, PhotoImage, Radiobutton, StringVar, Toplevel

from account import user
from database import database_connection, database_handler


class Scale:
    """This class will handle the user GUI whe he/she is not logged in."""

    def __init__(self, window, user_name):
        """Initiates the window."""
        self.window = window
        self.var = StringVar()
        self.user = user_name
        self.db_handler = database_handler.DatabaseHandler()
        self.database = database_connection.DatabaseConnection(
            "root", "Cbth2468"
        )  # Change to your db username and password.

    def scale_gui(self):
        """User interface with scale."""
        scale_frame = Frame(self.window)
        scale_frame.configure(bg="#040B20")
        return_button = PhotoImage(file=r"schedule\images\Return.png")
        select_button = PhotoImage(file=r"schedule\images\Select.png")
        Label(
            scale_frame,
            text="Please scale you stress level today",
            font=("Arial", 14),
            bg="#040B20",
            fg="#78CBFF",
        ).grid(row=0, column=1, columnspan=10, pady=40)

        scale = [
            (1, "#F8D5BE"),
            (2, "#F9BB93"),
            (3, "#F79757"),
            (4, "#F88A41"),
            (5, "#F77119"),
            (6, "#E75E04"),
            (7, "#C55206"),
            (8, "#A83304"),
            (9, "#922D05"),
            (10, "#BE0808"),
        ]

        self.var.set("1")
        Label(
            scale_frame,
            text="Not stressed",
            font=("Arial", 14),
            bg="#040B20",
            fg="#F8D5BE",
        ).grid(row=1, column=0, sticky="W")
        Label(
            scale_frame,
            text="Werry stressed",
            font=("Arial", 14),
            bg="#040B20",
            fg="#BE0808",
        ).grid(row=1, column=11, sticky="E")

        for number, code in scale:
            Radiobutton(
                scale_frame,
                variable=self.var,
                value=code,
                highlightthickness=0,
                font=("Arial", 0),
                bg="#040B20",
                fg=code,
            ).grid(row=1, column=number, sticky="w")
            Label(
                scale_frame,
                text=number,
                font=("Arial", 14),
                bg="#040B20",
                fg=code,
            ).grid(row=3, column=number, sticky="W", pady=10)

        Button(
            scale_frame,
            image=select_button,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.store_selected(scale_frame),
        ).grid(row=5, column=6, columnspan=10, pady=40)

        Button(
            scale_frame,
            image=return_button,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.return_to_user_page(scale_frame, 0),
        ).grid(row=5, column=0, columnspan=10, pady=40, sticky="W")

        scale_frame.pack()
        self.window.mainloop()

    def return_to_user_page(self, scale_frame, num):
        """button action for return."""
        if num == 1:
            self.top.destroy()
        scale_frame.pack_forget()
        logged_in_user = user.User(True, self.user, self.window)
        logged_in_user.user_gui()

    def store_selected(self, scale_frame):
        """load to database selected stress level."""
        colour = self.var.get()
        if colour == "1":
            Label(
                scale_frame,
                text="Choose stress level",
                bg="#040B20",
                fg="#ff0000",
                font=("Arial", 14),
            ).grid(row=4, column=1, columnspan=10, ipady=10)
        else:
            try:
                self.cursor = self.database.connect()
                query = (
                    "INSERT INTO stress_calender (date, stress_level, user_user_name)"
                    "VALUES (%s, %s, %s)"
                )
                formateddate = datetime.now().strftime("%Y-%m-%d")
                values = (formateddate, colour, self.user)
                self.cursor.execute(query, values)
                if self.cursor.rowcount == 1:
                    self.database.commit()
                    self.cursor.close()

            finally:
                self.top = Toplevel()
                self.top.geometry("280x200")
                self.top.title("app name")
                self.top.resizable(height=True, width=False)
                self.top.configure(bg="#040B20")
                Label(
                    self.top,
                    text="Stress level saved!",
                    font=("Arial", 14),
                    bg="#040B20",
                    fg="#F8D5BE",
                ).grid(row=1, column=5, pady=40, padx=(40, 40))
                Button(
                    self.top,
                    text="Ok",
                    bg="#78CBFF",
                    fg="#040B20",
                    height=1,
                    width=5,
                    font=("Arial", 14),
                    command=lambda: self.return_to_user_page(scale_frame, 1),
                ).grid(row=2, column=5, pady=(20, 40), padx=(40, 40))
