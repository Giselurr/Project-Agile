from datetime import datetime, timedelta
from tkinter import SW, Button, Canvas, Tk

from PIL import Image, ImageTk

import main
from database import database_handler


class History:
    def __init__(self, window, user_name):
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

    def calculate_current_week(self):
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
        self.monday_date += timedelta(days=7)
        self.tuesday_date += timedelta(days=7)
        self.wednesday_date += timedelta(days=7)
        self.thursday_date += timedelta(days=7)
        self.friday_date += timedelta(days=7)
        self.saturday_date += timedelta(days=7)
        self.sunday_date += timedelta(days=7)

    def calculate_previous_week(self):
        self.monday_date -= timedelta(days=7)
        self.tuesday_date -= timedelta(days=7)
        self.wednesday_date -= timedelta(days=7)
        self.thursday_date -= timedelta(days=7)
        self.friday_date -= timedelta(days=7)
        self.saturday_date -= timedelta(days=7)
        self.sunday_date -= timedelta(days=7)

    def temp_print_dates_for_testing(self):
        print(self.monday_date)
        print(self.tuesday_date)
        print(self.wednesday_date)
        print(self.thursday_date)
        print(self.friday_date)
        print(self.saturday_date)
        print(self.sunday_date)
        print()

    def change_week(self, change, page):
        self.barchart_canvas.delete("all")
        self.notes_canvas.delete("all")

        if change == "NEXT":
            self.calculate_next_week()
            if page == "BARCHART":
                self.draw_stress_history()
            elif page == "NOTES":
                self.draw_notes_page()
        elif change == "PREVIOUS":
            self.calculate_previous_week()
            if page == "BARCHART":
                self.draw_stress_history()
            elif page == "NOTES":
                self.draw_notes_page()

    def draw_buttons(self):
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
                self, self.barchart_canvas, "USER_MENU", self.user_name, None
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
            command=lambda: self.draw_notes_page(),
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=350, y=70)
        self.window.mainloop()

    def draw_current_week_text(self):
        text = f"Week of {self.monday_date.strftime('%B %d, %Y')}"

        self.barchart_canvas.create_text(
            320,
            30,
            text=text,
            font=("Arial", 18),
            fill="#AFB5D6",
        )

    def draw_day_text(self):
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
        stress_levels = [6, 9, 4, 7, 3, 5, 1]

        bar_height = 44
        bar_width = 40
        bar_gap = 20
        left_gap = 120
        bottom_gap = 75

        scale_and_color = {
            10: "#BE0808",
            9: "#922D05",
            8: "#A83304",
            7: "#C55206",
            6: "#E75E04",
            5: "#F77119",
            4: "#F88A41",
            3: "#F79757",
            2: "#F9BB93",
            1: "#F8D5BE",
        }

        for x, y in enumerate(stress_levels):
            x0 = x * (bar_gap + bar_width) + left_gap
            y0 = 700 - (y * bar_height + bottom_gap)
            x1 = x0 + bar_width
            y1 = 700 - bottom_gap

            color = scale_and_color.get(y, "white")

            self.barchart_canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def draw_notes_dates(self):
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

    def draw_notes_buttons(self):
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
        ).place(x=205, y=610)
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
            command=lambda: self.return_to_barchart(),
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
            command=lambda: self.return_to_barchart(),
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
            command=lambda: self.return_to_barchart(),
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
            command=lambda: self.return_to_barchart(),
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
            command=lambda: self.return_to_barchart(),
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
            command=lambda: self.return_to_barchart(),
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
            command=lambda: self.return_to_barchart(),
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=506, y=100)
        self.window.mainloop()

    def return_to_barchart(self):
        self.notes_canvas.pack_forget()
        self.barchart_canvas.pack()
        self.draw_stress_history()

    def draw_notes_page(self):
        """Stops showing the barchart page and creates and shows the notes page."""
        self.barchart_canvas.pack_forget()
        self.notes_canvas.pack()

        self.draw_notes_dates()
        self.draw_notes_buttons()

    def draw_stress_history(self):
        """Displays the barchart page."""
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
