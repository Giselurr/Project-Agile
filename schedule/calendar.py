import datetime
from tkinter import CENTER, Button, Frame, Label, PhotoImage, Tk

import main
from database import database_handler


class CalendarInt:
    def __init__(self, window, user_name, date, reminder):
        self.window = window
        self.user = user_name
        self.date = datetime.datetime.strptime(date, "%Y-%m-%d")
        self.date_today = datetime.datetime.now()
        self.db_handler = database_handler.DatabaseHandler()
        self.events = self.db_handler.get_daily_schedule(user_name)
        self.sorted_events = sorted(self.events, key=lambda x: x[0])
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
            anchor=CENTER,
            activebackground="#040B20",
            command=self.return_to_user_page,
        ).grid(row=8, column=1, columnspan=5, pady=10)

        month_year_text = self.date_today.strftime("%B %Y")
        Label(
            self.calendar_frame,
            text=month_year_text,
            font=("Arial", 18),
            anchor=CENTER,
            bg="#040B20",
            fg="#AFB5D6",
        ).grid(row=0, column=1, columnspan=5, pady=40)

        self.create_calendar(self.calendar_frame)

        self.calendar_frame.pack()
        self.window.mainloop()

    def create_calendar(self, parent):
        days_in_month = self.days_in_month(self.date.year, self.date.month)
        start_day = datetime.datetime(self.date.year, self.date.month, 1)
        start_day -= datetime.timedelta(days=start_day.isoweekday() - 1)
        foreground = "white"
        for i in range(6):
            for j in range(7):
                current_day = start_day + datetime.timedelta(days=(i * 7) + j)

                if (
                    current_day.month == self.date.month
                    and not current_day.day < self.date_today.day
                ):
                    foreground = "white"
                else:
                    foreground = "#808080"

                day_button = Button(
                    parent,
                    text=str(current_day.day),
                    width=5,
                    height=2,
                    relief="flat",
                    bg="#1E2749" if current_day.month == self.date.month else "#040B20",
                    fg=foreground,
                    command=lambda day=current_day: self.task_gui(day),
                )
                day_button.grid(row=i + 2, column=j, padx=5, pady=5)
                # if current_day.day < self.date_today.day:
                #     day_button["state"] = "disabled"

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

    def task_gui(self, day):
        self.calendar_frame.pack_forget()
        task_frame = Frame(self.window, bg="#040B20")
        task_frame.pack(fill="both", expand=True, padx=10, pady=10)

        str_day = day.strftime("%d").lstrip("0")
        date_and_month = day.strftime(f"%a %b {str_day}")
        Label(
            task_frame,
            text=f"Tasks for: {date_and_month}",
            font=("Arial", 18, "bold"),
            bg="#040B20",
            fg="#AFB5D6",
        ).place(x=320, y=30, anchor=CENTER)

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
        ).place(x=320, y=585, anchor=CENTER)

        y = 100
        number_of_tasks = 0
        for start, stop, task in self.sorted_events:
            if start.date() == day.date():
                start_time = start.strftime("%H:%M")
                stop_time = stop.strftime("%H:%M")
                Label(
                    task_frame,
                    text=f"{task}:  {start_time} - {stop_time}",
                    font=("Arial", 13, "bold"),
                    bg="#040B20",
                    fg="#AFB5D6",
                ).place(x=320, y=y, anchor=CENTER)
                y += 40
                number_of_tasks += 1
                if number_of_tasks == 11:
                    break

    def return_to_calendar_gui(self, task_frame):
        task_frame.destroy()
        self.calendar_frame.pack()
        self.calendar_gui()


if __name__ == "__main__":
    window = Tk()
    calendar_int = CalendarInt(window, "username", "2024-05-12")
    calendar_int.calendar_gui()
