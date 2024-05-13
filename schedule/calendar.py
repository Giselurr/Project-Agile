import datetime
from tkinter import Button, Frame, Label, PhotoImage, Tk

import main


class CalendarInt:
    def __init__(self, window, user_name, date):
        self.window = window
        self.user = user_name
        self.date = datetime.datetime.strptime(date, "%Y-%m-%d")
        self.window.title("Breathe")
        self.window.iconbitmap("schedule\images\Breathe_icon.ico")
        self.calendar_frame = None

    def calendar_gui(self):
        self.calendar_frame = Frame(self.window)
        self.calendar_frame.configure(bg="#040B20")
        return_button = PhotoImage(file=r"schedule\images\Return.png")

        Button(
            self.calendar_frame,
            image=return_button,
            borderwidth=0,
            highlightthickness=0,
            activebackground="#040B20",
            command=self.return_to_user_page,
        ).grid(row=8, column=0, columnspan=10, pady=10, sticky="W")

        Label(
            self.calendar_frame,
            text="Calendar",
            font=("Arial", 14),
            bg="#040B20",
            fg="#AFB5D6",
        ).grid(row=0, column=1, columnspan=10, pady=40)

        self.create_calendar(self.calendar_frame)

        self.calendar_frame.pack()
        self.window.mainloop()

    def create_calendar(self, parent):
        today = datetime.datetime.now()
        days_in_month = self.days_in_month(self.date.year, self.date.month)
        start_day = datetime.datetime(self.date.year, self.date.month, 1)

        for i in range(6):
            for j in range(7):
                current_day = start_day + datetime.timedelta(days=(i * 7) + j)
                day_button = Button(
                    parent,
                    text=str(current_day.day),
                    width=5,
                    height=2,
                    relief="flat",
                    bg="#1E2749" if current_day.month == self.date.month else "#040B20",
                    fg="#FFFFFF" if current_day.month == self.date.month else "#808080",
                    command=lambda day=current_day: self.select_day(day),
                )
                day_button.grid(row=i + 2, column=j, padx=5, pady=5)
                if current_day < today:
                    day_button["state"] = "disabled"

    def days_in_month(self, year, month):
        if month == 12:
            return (
                datetime.datetime(year + 1, 1, 1) - datetime.datetime(year, month, 1)
            ).days
        return (
            datetime.datetime(year, month + 1, 1) - datetime.datetime(year, month, 1)
        ).days

    def return_to_user_page(self):
        self.window.destroy()  # Close current window
        main.Main.manager_menu_choice(
            self, self.calendar_frame, "USER_MENU", self.user, self.date
        )

    def select_day(self, day):
        print("Selected Day:", day)


if __name__ == "__main__":
    window = Tk()
    calendar_int = CalendarInt(window, "username", "2024-05-12")
    calendar_int.calendar_gui()
