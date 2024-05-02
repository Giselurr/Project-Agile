"""This module will show scale and connect with database to store the stress level."""

from tkinter import (
    END,
    Button,
    Frame,
    Label,
    PhotoImage,
    Radiobutton,
    StringVar,
    Text,
    Toplevel,
)

import main
from database import database_connection, database_handler


class Scale:
    """This class will handle the user GUI whe he/she is not logged in."""

    def __init__(self, window, user_name, date):
        """Initiate the window."""
        self.window = window
        self.user = user_name
        self.date = date
        self.db_handler = database_handler.DatabaseHandler()
        self.database = database_connection.DatabaseConnection()

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
        colour = StringVar()
        colour.set("1")
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
                variable=colour,
                value=code,
                highlightthickness=0,
                font=("Arial", 0),
                bg="#040B20",
                fg="Black",
            ).grid(row=1, column=number, sticky="w")
            Label(
                scale_frame,
                text=number,
                font=("Arial", 14),
                bg="#040B20",
                fg=code,
            ).grid(row=3, column=number, sticky="W", pady=10)

        Label(
            scale_frame,
            text="Notes:",
            font=("Arial", 14),
            bg="#040B20",
            fg="#78CBFF",
        ).grid(row=4, column=0, columnspan=1, pady=(30, 0), padx=(50, 10))

        note = Text(
            scale_frame,
            height=5,
            width=30,
            font=("Arial", 14),
        )
        note.insert("1.0", "(Max 300 characters)")
        note.grid(row=5, column=1, columnspan=10, pady=(0, 40))

        Button(
            scale_frame,
            image=select_button,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.check_entry(scale_frame, colour, note),
        ).grid(row=7, column=6, columnspan=10, pady=40)

        Button(
            scale_frame,
            image=return_button,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.return_to_user_page(scale_frame, False),
        ).grid(row=7, column=0, columnspan=10, pady=40, sticky="W")

        scale_frame.pack()
        self.window.mainloop()

    def return_to_user_page(self, scale_frame, close_popup):
        """Button action for return."""
        if close_popup:
            self.top.destroy()
        main.Main.manager_menu_choice(
            self, scale_frame, "USER_MENU", self.user, self.date
        )

    def store_selected(self, scale_frame, var):
        """Load to database selected stress level."""
        colour = var.get()
        if colour == "1":
            Label(
                scale_frame,
                text="Choose stress level",
                bg="#040B20",
                fg="#ff0000",
                font=("Arial", 14),
            ).grid(row=6, column=1, columnspan=10, ipady=10)

    def check_entry(self, scale_frame, colour, note):
        """Load to database selected stress level."""
        colour = colour.get()
        notes = note.get(1.0, END)
        result = self.db_handler.check_date(self.user, self.date)
        if colour == "1":
            Label(
                scale_frame,
                text="Must choose stress level",
                bg="#040B20",
                fg="#ff0000",
                font=("Arial", 14),
            ).grid(row=6, column=1, columnspan=10, ipady=10)
        elif result[1]:
            self.confirm_overide(scale_frame, result[0], colour, notes)
        self.save_selected(scale_frame, colour, notes)

    def confirm_overide(self, scale_frame, id_calander, colour, notes):
        """Ensure user want to overwrite their old entry."""
        Label(
            self.top,
            text="Are you sure you want to save changes?",
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
            command=lambda: self.db_handler.update_row(
                self.top, colour, notes, id_calander
            ),
        ).grid(row=2, column=5, pady=(20, 40), padx=(40, 40))
        Button(
            self.top,
            text="Return",
            bg="#78CBFF",
            fg="#040B20",
            height=1,
            width=5,
            font=("Arial", 14),
            command=lambda: self.return_to_user_page(scale_frame, True),
        ).grid(row=2, column=5, pady=(20, 40), padx=(40, 40))

    def save_selected(self, scale_frame, colour, note):
        """This will handel insert to database."""
        try:
            self.cursor = self.database.connect()
            query = (
                "INSERT INTO stress_calender (date, stress_level, note, user_user_name)"
                "VALUES (%s, %s, %s)"
            )
            formateddate = self.date.strftime("%Y-%m-%d")
            values = (formateddate, colour, note, self.user)
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
                command=lambda: self.return_to_user_page(scale_frame, True),
            ).grid(row=2, column=5, pady=(20, 40), padx=(40, 40))
