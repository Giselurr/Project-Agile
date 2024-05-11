import threading
import time
from datetime import datetime
from tkinter import messagebox


class Reminder:
    """This class will hold the reminder for the user."""

    def __init__(self, username):
        self.user_name = username
        self.tasks = []
        self.lock = threading.Lock()

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
                        messagebox.showinfo("REMINDER!", f"{task}")
                        self.tasks.remove((start, task))
            time.sleep(10)
