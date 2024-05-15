import datetime
from tkinter import Button, Frame, Label, PhotoImage, Tk

import main
from database import database_handler


class CalendarInt:
    def __init__(self, window, user_name, date, reminder):
        self.window = window
        self.user = user_name
        self.date = datetime.datetime.strptime(date, "%Y-%m-%d")
        self.db_handler = database_handler.DatabaseHandler()
        self.events = self.db_handler.get_daily_schedule(user_name)
        self.window.title("Breathe")
        self.window.iconbitmap("schedule\images\Breathe_icon.ico")
        self.calendar_frame = None
        self.reminder = reminder
        self.return_image = PhotoImage(file=r"schedule\images\Return.png")
        self.calendar_frame = Frame(self.window)
        self.calendar_frame.configure(bg="#040B20")

    def calendar_gui(self):
        Button(
            self.calendar_frame,
            image=self.return_image,
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
        start_day -= datetime.timedelta(days=start_day.isoweekday() - 1)

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
                    command=lambda day=current_day: self.task_gui(day),
                )
                day_button.grid(row=i + 2, column=j, padx=5, pady=5)
                current_day += datetime.timedelta(days=1)
                # No clue why but +1day fixed problem of the current day being wrong.
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
        self.calendar_frame.destroy()  # Close current window
        main.Main.manager_menu_choice(
            self, self.calendar_frame, "USER_MENU", self.user, self.date, self.reminder
        )

    def select_day(self, day):
        print("Selected Day:", day)

    def task_gui(self, day):
        self.calendar_frame.pack_forget()
        task_frame = Frame(self.window, bg="#040B20")
        task_frame.pack(fill="both", expand=True, padx=10, pady=10)

        str_day = day.strftime("%d").lstrip("0")
        date_and_month = day.strftime(f"%a, %b, {str_day}")
        Label(
            task_frame,
            text=f"Tasks for: {date_and_month}",
            font=("Arial", 14),
            bg="#040B20",
            fg="#AFB5D6",
        ).place(x=200, y=200)

        Button(
            task_frame,
            image=self.return_image,
            activebackground="#040B20",
            command=lambda: self.return_to_calendar_gui(task_frame),
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=205, y=585)

        for start, stop, task in self.events:
            print(start.date())
            print(day.date())
            if start.date() == day.date():
                print(f"Task: {task}\nStart time: {start}\nEnd time: {stop}")

    def return_to_calendar_gui(self, task_frame):
        task_frame.destroy()
        self.calendar_frame.pack()
        self.calendar_gui()


if __name__ == "__main__":
    window = Tk()
    calendar_int = CalendarInt(window, "username", "2024-05-12")
    calendar_int.calendar_gui()
