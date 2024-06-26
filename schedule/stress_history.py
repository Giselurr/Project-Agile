from datetime import datetime, timedelta
from tkinter import NW, SW, Button, Canvas, Tk

from PIL import Image, ImageTk

import main
from database import database_handler


class History:
    """The class handeles the creation and functionality
    of the barchart and notes page."""

    def __init__(self, window, user_name, reminder):
        """Init the history class"""
        self.user_name = user_name
        self.db_handler = database_handler.DatabaseHandler()
        self.window = window
        self.window.resizable(height=False, width=False)
        self.window.title("Breathe")
        self.window.iconbitmap("account\images\Breathe_icon.ico")
        self.barchart_canvas = Canvas(
            self.window, width=640, height=700, bg="#040B20", highlightthickness=0
        )
        self.barchart_canvas.pack()

        self.notes_canvas = Canvas(
            self.window, width=640, height=700, bg="#040B20", highlightthickness=0
        )

        self.current_date = datetime.now()
        self.monday_date = None
        self.tuesday_date = None
        self.wednesday_date = None
        self.thursday_date = None
        self.friday_date = None
        self.saturday_date = None
        self.sunday_date = None
        self.reminder = reminder

    def calculate_current_week(self):
        """Calculates the dates of the current week."""
        self.monday_date = self.current_date
        self.monday_date -= timedelta(days=self.current_date.isoweekday() - 1)

        self.tuesday_date = self.monday_date
        self.wednesday_date = self.monday_date
        self.thursday_date = self.monday_date
        self.friday_date = self.monday_date
        self.saturday_date = self.monday_date
        self.sunday_date = self.monday_date

        self.tuesday_date += timedelta(days=1)
        self.wednesday_date += timedelta(days=2)
        self.thursday_date += timedelta(days=3)
        self.friday_date += timedelta(days=4)
        self.saturday_date += timedelta(days=5)
        self.sunday_date += timedelta(days=6)

    def calculate_next_week(self):
        """Calculates the dates for the next week."""
        self.monday_date += timedelta(days=7)
        self.tuesday_date += timedelta(days=7)
        self.wednesday_date += timedelta(days=7)
        self.thursday_date += timedelta(days=7)
        self.friday_date += timedelta(days=7)
        self.saturday_date += timedelta(days=7)
        self.sunday_date += timedelta(days=7)

    def calculate_previous_week(self):
        """Calculates the dates for the previous week."""
        self.monday_date -= timedelta(days=7)
        self.tuesday_date -= timedelta(days=7)
        self.wednesday_date -= timedelta(days=7)
        self.thursday_date -= timedelta(days=7)
        self.friday_date -= timedelta(days=7)
        self.saturday_date -= timedelta(days=7)
        self.sunday_date -= timedelta(days=7)

    def change_week(self, change, page):
        """Changes the weeks in the barchart or notes."""
        self.barchart_canvas.delete("all")
        self.notes_canvas.delete("all")

        if change == "NEXT":
            self.calculate_next_week()
            if page == "BARCHART":
                self.draw_stress_history()
            elif page == "NOTES":
                self.draw_notes_page(False)
        elif change == "PREVIOUS":
            self.calculate_previous_week()
            if page == "BARCHART":
                self.draw_stress_history()
            elif page == "NOTES":
                self.draw_notes_page(False)

    def draw_buttons(self):
        """Draws all the buttons on the barchart page."""
        next_img = ImageTk.PhotoImage(Image.open("schedule\images\Right_arrow.png"))
        previous_img = ImageTk.PhotoImage(Image.open("schedule\images\Left_arrow.png"))
        return_img = ImageTk.PhotoImage(Image.open("schedule\images\Return.png"))
        notes_img = ImageTk.PhotoImage(Image.open("schedule\images\img_notes.png"))
        Button(
            self.barchart_canvas,
            image=previous_img,
            activebackground="#040B20",
            command=lambda: self.change_week("PREVIOUS", "BARCHART"),
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=75, y=641)
        Button(
            self.barchart_canvas,
            image=next_img,
            activebackground="#040B20",
            command=lambda: self.change_week("NEXT", "BARCHART"),
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=545, y=641)
        Button(
            self.barchart_canvas,
            image=return_img,
            activebackground="#040B20",
            command=lambda: main.Main.manager_menu_choice(
                self,
                self.barchart_canvas,
                "USER_MENU",
                self.user_name,
                None,
                self.reminder,
            ),
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=60, y=70)
        Button(
            self.barchart_canvas,
            image=notes_img,
            activebackground="#040B20",
            command=lambda: self.prepare_notes_page(),
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=350, y=70)
        self.window.mainloop()

    def draw_current_week_text(self):
        """Draws the text for the current week."""
        text = f"Week of {self.monday_date.strftime('%B %d, %Y')}"

        self.barchart_canvas.create_text(
            320,
            30,
            text=text,
            font=("Arial", 18),
            fill="#AFB5D6",
        )

    def draw_day_text(self):
        """Draws the text for the days under the barchart."""
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        for i, day in enumerate(days):
            self.barchart_canvas.create_text(
                139 + i * 60,
                650,
                text=day,
                font=("Arial", 12, "bold"),
                fill="#AFB5D6",
            )

    def draw_scale_text(self):
        """Draws the text for the scale and lines in the barchart."""
        x = 90
        for i, number in enumerate(range(1, 11), start=0):
            y = 592 - i * 44
            self.barchart_canvas.create_text(
                x, y, anchor=SW, text=number, font=("Arial", 13, "bold"), fill="#AFB5D6"
            )
            self.barchart_canvas.create_text(
                x + 15,
                y - 9,
                anchor=SW,
                text="_" * 61,
                font=("Arial", 10, "bold"),
                fill="#AFB5D6",
            )  # Remove "* 61" in text to remove lines.

    def draw_barchart(self):
        """Draws the barchart."""
        color_and_scale = {
            "#BE0808": 10,
            "#922D05": 9,
            "#A83304": 8,
            "#C55206": 7,
            "#E75E04": 6,
            "#F77119": 5,
            "#F88A41": 4,
            "#F79757": 3,
            "#F9BB93": 2,
            "#F8D5BE": 1,
        }

        stress_levels = []

        stress_levels.append(
            color_and_scale.get(
                self.db_handler.get_stress_level(
                    self.user_name, self.monday_date.date()
                ),
                0,
            )
        )
        stress_levels.append(
            color_and_scale.get(
                self.db_handler.get_stress_level(
                    self.user_name, self.tuesday_date.date()
                ),
                0,
            )
        )
        stress_levels.append(
            color_and_scale.get(
                self.db_handler.get_stress_level(
                    self.user_name, self.wednesday_date.date()
                ),
                0,
            )
        )
        stress_levels.append(
            color_and_scale.get(
                self.db_handler.get_stress_level(
                    self.user_name, self.thursday_date.date()
                ),
                0,
            )
        )
        stress_levels.append(
            color_and_scale.get(
                self.db_handler.get_stress_level(
                    self.user_name, self.friday_date.date()
                ),
                0,
            )
        )
        stress_levels.append(
            color_and_scale.get(
                self.db_handler.get_stress_level(
                    self.user_name, self.saturday_date.date()
                ),
                0,
            )
        )
        stress_levels.append(
            color_and_scale.get(
                self.db_handler.get_stress_level(
                    self.user_name, self.sunday_date.date()
                ),
                0,
            )
        )

        bar_height = 44
        bar_width = 40
        bar_gap = 20
        left_gap = 120
        bottom_gap = 75

        # Inverted version of the color_and_scale dict.
        scale_and_color = dict([(value, key) for key, value in color_and_scale.items()])

        for x, y in enumerate(stress_levels):
            x0 = x * (bar_gap + bar_width) + left_gap
            y0 = 700 - (y * bar_height + bottom_gap)
            x1 = x0 + bar_width
            y1 = 700 - bottom_gap

            color = scale_and_color.get(y, "white")

            self.barchart_canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def draw_notes_dates(self):
        """Draws the dates in the note page."""
        dates_for_days = [
            self.monday_date,
            self.tuesday_date,
            self.wednesday_date,
            self.thursday_date,
            self.friday_date,
            self.saturday_date,
            self.sunday_date,
        ]
        for i, date in enumerate(dates_for_days):
            x = 90 + i * 75

            str_day = date.strftime("%d").lstrip("0")
            str_month = date.strftime("%m").lstrip("0")
            text = str_day + "/" + str_month

            self.notes_canvas.create_text(
                x,
                75,
                text=text,
                font=("Arial", 15, "bold"),
                fill="#AFB5D6",
            )

    def draw_notes_buttons(self, draw_note_frame):
        """Draws the buttons and images in the note page."""
        return_img = ImageTk.PhotoImage(Image.open("schedule\images\Return.png"))
        next_img = ImageTk.PhotoImage(Image.open("schedule\images\Right_arrow.png"))
        previous_img = ImageTk.PhotoImage(Image.open("schedule\images\Left_arrow.png"))
        right_note_img = ImageTk.PhotoImage(
            Image.open("schedule\images\\notes_right_button.png")
        )
        middle_note_img = ImageTk.PhotoImage(
            Image.open("schedule\images\\notes_middle_button.png")
        )
        left_note_img = ImageTk.PhotoImage(
            Image.open("schedule\images\\notes_left_button.png")
        )
        Button(
            self.notes_canvas,
            image=return_img,
            activebackground="#040B20",
            command=lambda: self.return_to_barchart(),
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=205, y=585)
        Button(
            self.notes_canvas,
            image=previous_img,
            activebackground="#040B20",
            command=lambda: self.change_week("PREVIOUS", "NOTES"),
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=30, y=65)
        Button(
            self.notes_canvas,
            image=next_img,
            activebackground="#040B20",
            command=lambda: self.change_week("NEXT", "NOTES"),
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=582, y=65)
        Button(
            self.notes_canvas,
            image=left_note_img,
            activebackground="#040B20",
            command=lambda: self.draw_note_text(self.monday_date),
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=50, y=100)
        Button(
            self.notes_canvas,
            image=middle_note_img,
            activebackground="#040B20",
            command=lambda: self.draw_note_text(self.tuesday_date),
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=126, y=100)
        Button(
            self.notes_canvas,
            image=middle_note_img,
            activebackground="#040B20",
            command=lambda: self.draw_note_text(self.wednesday_date),
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=202, y=100)
        Button(
            self.notes_canvas,
            image=middle_note_img,
            activebackground="#040B20",
            command=lambda: self.draw_note_text(self.thursday_date),
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=278, y=100)
        Button(
            self.notes_canvas,
            image=middle_note_img,
            activebackground="#040B20",
            command=lambda: self.draw_note_text(self.friday_date),
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=354, y=100)
        Button(
            self.notes_canvas,
            image=middle_note_img,
            activebackground="#040B20",
            command=lambda: self.draw_note_text(self.saturday_date),
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=430, y=100)
        Button(
            self.notes_canvas,
            image=right_note_img,
            activebackground="#040B20",
            command=lambda: self.draw_note_text(self.sunday_date),
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=506, y=100)

        # Border around the note text is located here since
        # all custom images have to be in mainloop.
        if draw_note_frame:
            note_text_frame_img = ImageTk.PhotoImage(
                Image.open("schedule\images\\Note_frame.png")
            )
            self.notes_canvas.create_image(
                95, 175, image=note_text_frame_img, anchor=NW
            )

        self.window.mainloop()

    def draw_note_text(self, date):
        """Draws all the text in the note, including stress level and date."""
        # Border around the text is located in draw_notes_buttons since
        # all custom images have to be in mainloop.
        self.notes_canvas.delete("all")

        stress_level_color = self.db_handler.get_stress_level(
            self.user_name, date.date()
        )
        scale_and_color = {
            "#BE0808": 10,
            "#922D05": 9,
            "#A83304": 8,
            "#C55206": 7,
            "#E75E04": 6,
            "#F77119": 5,
            "#F88A41": 4,
            "#F79757": 3,
            "#F9BB93": 2,
            "#F8D5BE": 1,
        }
        stress_level = scale_and_color.get(stress_level_color, "No score")

        note_text = self.db_handler.get_note(self.user_name, date.date())
        if note_text == "":  # Remove if this gets fixed in scale.
            note_text = "No note"

        self.notes_canvas.create_text(
            110,
            300,
            anchor=NW,
            text=note_text,
            font=("Arial", 14),
            fill="#AFB5D6",
            width=420,
        )

        str_day = date.strftime("%d").lstrip("0")
        str_month = date.strftime("%m").lstrip("0")
        str_year = date.strftime("%Y")
        date_text = "Date:  " + str_day + "/" + str_month + " - " + str_year

        self.notes_canvas.create_text(
            110,
            200,
            anchor=NW,
            text=date_text,
            font=("Arial", 14),
            fill="#AFB5D6",
        )

        stress_level_text = f"Stress level:  {stress_level}"

        self.notes_canvas.create_text(
            110,
            250,
            anchor=NW,
            text=stress_level_text,
            font=("Arial", 14),
            fill="#AFB5D6",
        )

        self.draw_notes_page(True)

    def draw_click_button_text(self):
        """Draws the text that prompts the user to press a button."""
        self.notes_canvas.create_text(
            320,
            375,
            text="Press a button to see the note for that date",
            font=("Arial", 14),
            fill="#AFB5D6",
        )

    def return_to_barchart(self):
        """Closes the notes page and draws redirects to the barchart page."""
        self.notes_canvas.delete("all")
        self.notes_canvas.pack_forget()
        self.barchart_canvas.pack()
        self.draw_stress_history()

    def prepare_notes_page(self):
        """Prepares the notes page for when it is drawn from the barchart page."""
        self.barchart_canvas.pack_forget()
        self.notes_canvas.pack()
        self.draw_notes_page(False)

    def draw_notes_page(self, draw_frame):
        """Draws the note page."""
        self.draw_notes_dates()
        if not draw_frame:
            self.draw_click_button_text()
        self.draw_notes_buttons(draw_frame)

    def draw_stress_history(self):
        """Draws the barchart page."""
        if self.current_date == datetime.now():
            self.calculate_current_week()
        self.draw_scale_text()
        self.draw_barchart()
        self.draw_day_text()
        self.draw_current_week_text()
        self.draw_buttons()


if __name__ == "__main__":
    window = Tk()
    stress_history = History(window)
    stress_history.draw_stress_history()
