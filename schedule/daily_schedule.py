"""This module handles and displays the users daily schedule."""

from datetime import datetime
from tkinter import (
    Button,
    Entry,
    Frame,
    Label,
    PhotoImage,
    Spinbox,
    StringVar,
    Tk,
    messagebox,
)

import database.database_connection
import database.database_handler
import main


class DailyScheduele:
    """This handles the schedule for the day and here you can also
    add tasks and breaks for the day."""

    def __init__(self, window, user_name, date, reminder):
        self.date = date
        self.user_name = user_name
        self.window = window
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - 640) // 2
        y = (screen_height - 700) // 2
        self.window.geometry(f"640x700+{x}+{y}")
        self.db_handler = database.database_handler.DatabaseHandler()
        self.database = database.database_connection.DatabaseConnection()
        self.window.title("Breathe")
        self.window.iconbitmap("schedule\images\Breathe_icon.ico")
        self.calendar_frame = Frame(self.window, bg="#040B20")
        self.calendar_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.events = self.db_handler.get_daily_schedule(self.user_name)
        self.reminder_obj = reminder

    def daily_schedule_gui(self):
        self.return_img = PhotoImage(file="schedule\images\\return_small_light.png")
        self.save_img = PhotoImage(file="schedule\images\Save.png")
        Label(
            self.calendar_frame,
            text="Your daily schedule",
            bg="#040B20",
            fg="#FFFFFF",
            font=("Arial", 20),
        ).pack()
        if not all(self.events):
            Label(
                self.calendar_frame,
                text="",
                bg="#040B20",
                fg="#FFFFFF",
                font=("Arial", 15),
            ).pack()
            Label(
                self.calendar_frame,
                text="You have nothing scheduled for today.",
                bg="#040B20",
                fg="#FFFFFF",
                font=("Arial", 15),
            ).pack()
            Label(
                self.calendar_frame,
                text="",
                bg="#040B20",
                fg="#FFFFFF",
                font=("Arial", 15),
            ).pack()
        else:
            schedule_frame = Frame(self.calendar_frame, bg="#040B20")
            schedule_frame.pack()
            Label(
                self.calendar_frame,
                text="",
                bg="#040B20",
                fg="#FFFFFF",
                font=("Arial", 15),
            ).pack()
            for i, (start, stop, task) in enumerate(self.events):
                start_time = start.time()
                stop_time = stop.time()
                Label(
                    schedule_frame,
                    text=start_time.strftime("%H:%M"),
                    bg="#040B20",
                    fg="#FFFFFF",
                    font=("Arial", 15),
                ).grid(row=i, column=0)
                Label(
                    schedule_frame,
                    text=" - ",
                    bg="#040B20",
                    fg="#FFFFFF",
                    font=("Arial", 15),
                ).grid(row=i, column=1)
                Label(
                    schedule_frame,
                    text=stop_time.strftime("%H:%M"),
                    bg="#040B20",
                    fg="#FFFFFF",
                    font=("Arial", 15),
                ).grid(row=i, column=1)
                Label(
                    schedule_frame,
                    text=task,
                    bg="#040B20",
                    fg="#FFFFFF",
                    font=("Arial", 13),
                ).grid(row=i, column=2, columnspan=3, padx=10, pady=10, sticky="W")
        Button(
            self.calendar_frame,
            text="ADD ITEM",
            bg="#040B20",
            fg="#FFFFFF",
            font=("Arial", 15),
            command=lambda: self.add_task(),
        ).pack()

        Button(
            self.calendar_frame,
            text="RETURN",
            bg="#040B20",
            fg="#FFFFFF",
            font=("Arial", 15),
            command=lambda: main.Main.manager_menu_choice(
                self,
                self.calendar_frame,
                "USER_MENU",
                self.user_name,
                None,
                self.reminder_obj,
            ),
        ).pack()

    def add_task(self):
        self.calendar_frame.pack_forget()
        add_task_frame = Frame(self.window, bg="#040B20")
        add_task_frame.pack(fill="both", expand=True, padx=10, pady=10)

        Label(
            add_task_frame,
            text="Add tasks for today",
            bg="#040B20",
            fg="#FFFFFF",
            font=("Arial", 14),
        ).pack()
        Label(
            add_task_frame, text="", bg="#040B20", fg="#FFFFFF", font=("Arial", 14)
        ).pack()
        Label(
            add_task_frame,
            text="Start time: ",
            bg="#040B20",
            fg="#FFFFFF",
            font=("Arial", 14),
        ).place(x=20, y=50)
        start_hour = Spinbox(
            add_task_frame, from_=00, to=23, width=5, font=("Arial", 14)
        )
        start_hour.place(x=120, y=50)
        start_minute = Spinbox(
            add_task_frame, from_=00, to=59, width=5, font=("Arial", 14)
        )
        start_minute.place(x=210, y=50)
        Label(
            add_task_frame,
            text="Stop time: ",
            bg="#040B20",
            fg="#FFFFFF",
            font=("Arial", 14),
        ).place(x=330, y=50)
        stop_hour = Spinbox(
            add_task_frame, from_=00, to=23, width=5, font=("Arial", 14)
        )
        stop_hour.place(x=430, y=50)
        stop_minute = Spinbox(
            add_task_frame, from_=00, to=59, width=5, font=("Arial", 14)
        )
        stop_minute.place(x=520, y=50)
        Label(
            add_task_frame,
            text="Add task: ",
            bg="#040B20",
            fg="#FFFFFF",
            font=("Arial", 14),
        ).place(x=20, y=100)
        task = StringVar()
        Entry(add_task_frame, textvariable=task, font=("Arial", 16), width=39).place(
            x=120, y=100
        )
        Button(
            add_task_frame,
            image=self.return_img,
            activebackground="#040B20",
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            command=lambda: main.Main.manager_menu_choice(
                self, add_task_frame, "SCHEDULE", self.user_name, None
            ),
            pady=0,
        ).place(x=180, y=150)
        Button(
            add_task_frame,
            image=self.save_img,
            activebackground="#040B20",
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            command=lambda: self.save_task(
                add_task_frame, start_hour, start_minute, stop_hour, stop_minute, task
            ),
            pady=0,
        ).place(x=320, y=150)

    def save_task(self, frame, start_hour, start_minute, stop_hour, stop_minute, task):
        start_hour = int(start_hour.get())
        start_minute = int(start_minute.get())
        stop_hour = int(stop_hour.get())
        stop_minute = int(stop_minute.get())

        start = datetime.now().replace(
            hour=start_hour, minute=start_minute, second=0, microsecond=0
        )
        stop = datetime.now().replace(
            hour=stop_hour, minute=stop_minute, second=0, microsecond=0
        )
        task = task.get()

        success = self.db_handler.add_task(self.user_name, start, stop, task)

        if success:
            messagebox.showinfo("Success", f"Successfully saved your task. {start}")

            self.reminder_obj.add_tasks(start, task)
            main.Main.manager_menu_choice(
                self, frame, "SCHEDULE", self.user_name, None, self.reminder_obj
            )
        else:
            messagebox.showinfo(
                "Error", "Your task has not been saved, please try again"
            )


if __name__ == "__main__":
    main_window = Tk()
    d_s = DailyScheduele(main_window, "Pernilla", datetime.now)
    d_s.daily_schedule_gui()
    main_window.mainloop()
