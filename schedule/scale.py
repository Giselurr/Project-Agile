from datetime import datetime
from tkinter import Button, Frame, Label, Radiobutton, StringVar

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
        Label(
            scale_frame,
            text="Please scale you stress level today",
            font=("Arial", 14),
            bg="#040B20",
            fg="#78CBFF",
        ).grid(row=0, column=1, columnspan=10, pady=40)

        scale = [
            (1, 1),  # "#F8D5BE"),
            (2, 2),  # "#F9BB93"),
            (3, 3),  # "#F79757"),
            (4, 4),  # "#F88A41"),
            (5, 5),  # "#F77119"),
            (6, 6),  # "#E75E04"),
            (7, 7),  # "#C55206"),
            (8, 8),  # "#A83304"),
            (9, 9),  # "#922D05"),
            (10, 10),
        ]  # "#BE0808")]

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
                font=("Arial", 0),
                bg="#040B20",
                fg="black",
            ).grid(row=1, column=number, sticky="w")
            Label(
                scale_frame,
                text=number,
                font=("Arial", 14),
                bg="#040B20",
                fg="white",
            ).grid(row=3, column=number, sticky="W", pady=10)

        Button(
            scale_frame,
            text="Select",
            bg="#78CBFF",
            fg="#040B20",
            height=1,
            width=10,
            font=("Arial", 14),
            command=lambda: self.store_selected(scale_frame),
        ).grid(row=4, column=4, columnspan=10, pady=40)

        Button(
            scale_frame,
            text="Return",
            bg="#78CBFF",
            fg="#040B20",
            height=1,
            width=10,
            font=("Arial", 14),
            command=lambda: self.return_to_user_page(scale_frame),
        ).grid(row=4, column=1, columnspan=10, pady=40, sticky="W")

        scale_frame.pack()
        self.window.mainloop()

    def return_to_user_page(self, scale_frame):
        """button action for return."""
        scale_frame.pack_forget()
        logged_in_user = user.User(True, self.user, self.window)
        logged_in_user.user_gui()

    def store_selected(self, scale_frame):
        """load to database selected stress level."""
        colour = self.var.get()
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
            self.return_to_user_page(scale_frame)
