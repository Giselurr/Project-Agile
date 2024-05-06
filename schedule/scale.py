"""Show the stress level scale and connect with database to store chosen\
      stress level."""

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
        ok_button = PhotoImage(file=r"schedule\\images\\Ok_light.png")
        save_button = PhotoImage(file=r"schedule\\images\Save_light.png")
        return_button = PhotoImage(file=r"schedule\images\Return.png")
        select_button = PhotoImage(file=r"schedule\images\Select.png")
        save_large_button = PhotoImage(file=r"schedule\images\Save_large_light.png")
        small_return = PhotoImage(file=r"schedule\images\return_small.png")
        Label(
            scale_frame,
            text="Please scale you stress level today",
            font=("Arial", 14),
            bg="#040B20",
            fg="#AFB5D6",
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
            text="Very stressed",
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
            fg="#AFB5D6",
        ).grid(row=4, column=0, columnspan=1, pady=(30, 0), padx=(50, 10))

        note = Text(
            scale_frame,
            height=5,
            width=30,
            bg="#AFB5D6",
            font=("Arial", 14),
        )
        note.insert("1.0", "(Max 300 characters)")
        note.grid(row=5, column=1, columnspan=10, pady=(0, 40))

        Button(
            scale_frame,
            image=save_large_button,
            borderwidth=0,
            highlightthickness=0,
            activebackground="#040B20",
            command=lambda: self.check_entry(
                scale_frame, colour, note, save_button, ok_button, small_return
            ),
        ).grid(row=7, column=6, columnspan=10, pady=40)

        Button(
            scale_frame,
            image=return_button,
            borderwidth=0,
            highlightthickness=0,
            activebackground="#040B20",
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

    def check_entry(
        self, scale_frame, colour, note, save_button, ok_button, small_return
    ):
        """Check if stress level exist for the date. If it should override old\
              data in database."""
        colour = colour.get()
        notes = note.get(1.0, END)
        result = self.db_handler.check_date(self.user, self.date)
        if colour == "1":
            Label(
                scale_frame,
                text="Must choose stress level",
                bg="#040B20",
                fg="#AFB5D6",
                font=("Arial", 14),
            ).grid(row=6, column=1, columnspan=10, ipady=10)
        elif result[1]:
            self.confirm_overide(
                scale_frame, result[0], colour, notes, save_button, small_return
            )
        else:
            self.save_selected(scale_frame, colour, notes, ok_button)

    def confirm_overide(
        self, scale_frame, id_calander, colour, notes, save_button, return_button
    ):
        """Ensure user want to overwrite their old entry."""
        self.top = Toplevel()
        self.top.geometry("280x200")
        self.top.title("Breath")
        self.top.resizable(height=True, width=False)
        self.top.configure(bg="#040B20")
        Label(
            self.top,
            text="Are you sure you \nwant to save changes?",
            font=("Arial", 14),
            bg="#040B20",
            fg="#AFB5D6",
        ).grid(row=1, column=1, columnspan=5, pady=30, padx=(40, 40))
        Button(
            self.top,
            image=save_button,
            borderwidth=0,
            highlightthickness=0,
            activebackground="#040B20",
            command=lambda: self.update_row(
                scale_frame, colour, notes, id_calander, True
            ),
        ).grid(row=2, column=3, pady=(10, 20), padx=(5, 10))
        Button(
            self.top,
            image=return_button,
            borderwidth=0,
            highlightthickness=0,
            activebackground="#040B20",
            command=lambda: self.return_to_user_page(scale_frame, True),
        ).grid(row=2, column=1, pady=(10, 20), padx=(20, 5))

    def save_selected(self, scale_frame, colour, note, ok_button):
        """Handel insert to database."""
        try:
            self.cursor = self.database.connect()
            query = (
                "INSERT INTO stress_calender (date, stress_level, note, user_user_name)"
                "VALUES (%s, %s, %s, %s)"
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
            self.top.title("Breath")
            self.top.resizable(height=True, width=False)
            self.top.configure(bg="#040B20")
            Label(
                self.top,
                text="Stress level saved!",
                font=("Arial", 14),
                bg="#040B20",
                fg="#AFB5D6",
            ).grid(row=1, column=5, pady=40, padx=(40, 40))
            Button(
                self.top,
                image=ok_button,
                borderwidth=0,
                highlightthickness=0,
                activebackground="#040B20",
                command=lambda: self.return_to_user_page(scale_frame, True),
            ).grid(row=2, column=5, pady=(20, 40), padx=(40, 40))

    def update_row(self, scale_frame, colour, notes, id_calender, close_pop_up):
        """Update existing row in database."""
        self.db_handler.update_row(colour, notes, id_calender)
        self.return_to_user_page(scale_frame, close_pop_up)
