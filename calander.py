import tkinter as tk
from datetime import datetime, timedelta
from tkinter import Button, Entry, Frame, Label, Toplevel, messagebox

from account.user import User


class CalendarPage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg="#040B20")  # Background color added here
        self.parent = parent
        self.pack(fill=tk.BOTH, expand=True)  # Fill and expand to parent size

        self.current_date = datetime.now().date()  # Current date
        self.image_folder = "schedule/images"
        self.notes = {}  # Dictionary to store notes for each date

        self.display_calendar()

    def display_calendar(self):
        title_label = Label(
            self,
            text=f"Week of {self.current_date.strftime('%B %d, %Y')}",
            font=("Helvetica", 16, "bold"),
            bg="#040B20",
        )  # Background color added here
        title_label.grid(row=0, column=0, columnspan=7, pady=(20, 10))

        # Frame for calendar numbers and days
        calendar_frame = Frame(self, bg="#040B20")
        calendar_frame.grid(row=1, column=0, columnspan=7, pady=(0, 10), sticky="nsew")

        # Display days of the week
        days_of_week = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        for i, day in enumerate(days_of_week):
            day_label = Label(
                calendar_frame,
                text=day,
                font=("Helvetica", 12, "bold"),
                bg="#040B20",
                fg="white",
            )
            day_label.grid(row=0, column=i, padx=10, pady=5)

        # Display dates for the week
        self.display_dates(calendar_frame)

        # Set row and column weights for resizing
        self.grid_rowconfigure(1, weight=1)
        for i in range(7):
            calendar_frame.grid_columnconfigure(i, weight=1)

        # Button to show previous week
        prev_week_button = Button(
            self,
            text="Previous Week",
            command=self.show_previous_week,
            font=("Helvetica", 12),
            bg="#040B20",
            fg="white",
            activebackground="#040B20",
        )
        prev_week_button.grid(
            row=2, column=0, columnspan=2, pady=(10, 20), sticky="nsew"
        )

        # Button to show next week
        next_week_button = Button(
            self,
            text="Next Week",
            command=self.show_next_week,
            font=("Helvetica", 12),
            bg="#040B20",
            fg="white",
            activebackground="#040B20",
        )
        next_week_button.grid(
            row=2, column=5, columnspan=2, pady=(10, 20), sticky="nsew"
        )

        # Cancel button
        cancel_button = Button(
            self,
            text="Cancel",
            command=self.cancel,
            font=("Helvetica", 12),
            bg="#040B20",
            fg="white",
            activebackground="#040B20",
        )  # Background color added here
        cancel_button.grid(row=3, column=0, columnspan=7, pady=(10, 20), sticky="nsew")

    def display_dates(self, calendar_frame):
        current_date = self.current_date
        for i in range(7):
            date_label = Label(
                calendar_frame,
                text=current_date.strftime("%d"),
                font=("Helvetica", 12),
                bg="#040B20",
                fg="white",
            )
            date_label.grid(row=1, column=i, padx=10, pady=5, sticky="nsew")
            date_label.bind(
                "<Button-1>",
                lambda event, date=current_date: self.show_note_dialog(date),
            )
            current_date += timedelta(days=1)

    def show_note_dialog(self, date):
        if date in self.notes:
            note_text = "\n".join(self.notes[date])
        else:
            note_text = ""

        note_dialog = Toplevel(self.parent)
        note_dialog.title(f"Notes for {date.strftime('%B %d, %Y')}")

        note_label = Label(note_dialog, text="Enter Note:", font=("Helvetica", 12))
        note_label.pack(pady=10)

        note_entry = Entry(note_dialog, font=("Helvetica", 12), width=30)
        note_entry.pack(pady=10)

        notes_display = Label(note_dialog, text=note_text, font=("Helvetica", 12))
        notes_display.pack(pady=10)

        submit_button = Button(
            note_dialog,
            text="Submit",
            command=lambda: self.submit_note(
                note_entry.get(), note_dialog, date, notes_display
            ),
            font=("Helvetica", 12),
            bg="#040B20",
            fg="white",
            activebackground="#040B20",
        )
        submit_button.pack(pady=10)

        note_dialog.focus_set()
        note_dialog.grab_set()

    def submit_note(self, note, note_dialog, date, notes_display):
        if note.strip() == "":
            messagebox.showerror("Error", "Note cannot be empty.")
        else:
            if date in self.notes:
                self.notes[date].append(note)
            else:
                self.notes[date] = [note]

            note_text = "\n".join(self.notes[date])
            notes_display.config(text=note_text)
            messagebox.showinfo(
                "Note Registered",
                f"Note '{note}' registered for {date.strftime('%B %d, %Y')}.",
            )
            note_dialog.destroy()

    def show_previous_week(self):
        # Update the current date to go back one week
        self.current_date -= timedelta(days=7)

        # Redraw the calendar with the updated date
        for widget in self.winfo_children():
            widget.destroy()
        self.display_calendar()

    def show_next_week(self):
        # Update the current date to go forward one week
        self.current_date += timedelta(days=7)

        # Redraw the calendar with the updated date
        for widget in self.winfo_children():
            widget.destroy()
        self.display_calendar()

    def cancel(self):
        self.pack_forget()  # Hide the calendar page
        user_redirect = User(
            True, "username", self.parent
        )  # Replace "username" with the actual username
        user_redirect.user_gui()

    # Call the user_gui


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Weekly Calendar")
    root.config(bg="#040B20")  # Background color added here
    app = CalendarPage(root)
    root.mainloop()
