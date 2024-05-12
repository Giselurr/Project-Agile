import threading
import time
from datetime import datetime
from tkinter import messagebox

import main


class Reminder:
    """This class will hold the reminder for the user."""

    def __init__(self, window, frame, username, reminder_obj):
        self.window = window
        self.frame = frame
        self.user_name = username
        self.tasks = []
        self.lock = threading.Lock()
        self.reminder_obj = reminder_obj

    def add_tasks(self, start, task):
        """Adds tasks to to the task list."""
        with self.lock:
            self.tasks.append((start, task))

    def checks_for_reminders(self):
        while True:
            now = datetime.now()
            with self.lock:
                for start, task in list(self.tasks):
                    if isinstance(start, datetime) and now >= start:
                        if task == "BREATHE":
                            messagebox.showinfo("REMINDER!", f"{task}")
                            self.tasks.remove((start, task))
                            for widget in self.window.winfo_children():
                                widget.destroy()
                            m = main.Main(self.window)
                            m.manager_menu_choice(
                                self.frame,
                                "BREATHE",
                                self.user_name,
                                datetime.now(),
                                self.reminder_obj,
                            )
                        else:
                            messagebox.showinfo("REMINDER!", f"{task}")
                            self.tasks.remove((start, task))
            time.sleep(10)
