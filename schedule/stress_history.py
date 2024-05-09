from datetime import datetime, timedelta
from tkinter import SW, Button, Canvas, Tk

from PIL import Image, ImageTk


class History:
    def __init__(self, window):
        self.window = window
        self.window.resizable(height=False, width=False)
        self.window.title("Breathe")
        self.window.iconbitmap("account\images\Breathe_icon.ico")
        self.canvas = Canvas(
            self.window, width=640, height=700, bg="#040B20", highlightthickness=0
        )
        self.canvas.pack()

        self.current_date = datetime.now()
        self.monday_date = None
        self.sunday_date = None

    def calculate_current_week(self):
        self.monday_date = self.current_date
        self.monday_date -= timedelta(days=self.current_date.isoweekday() - 1)
        self.sunday_date = self.monday_date
        self.sunday_date += timedelta(days=6)

    def change_week(self, change):
        if change == "NEXT":
            print("next")
        elif change == "PREVIOUS":
            print("previous")

    def draw_buttons(self):
        next_img = ImageTk.PhotoImage(
            Image.open("schedule\images\OK.png")
        )  # Change to new image.
        previous_img = ImageTk.PhotoImage(
            Image.open("schedule\images\Ok_light.png")
        )  # Change to new image.
        return_img = ImageTk.PhotoImage(Image.open("schedule\images\Return.png"))
        notes_img = ImageTk.PhotoImage(
            Image.open("schedule\images\Select.png")
        )  # Change to new image.
        Button(
            self.canvas,
            image=previous_img,
            activebackground="#040B20",
            command=lambda: self.change_week("PREVIOUS"),
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=160, y=60)
        Button(
            self.canvas,
            image=next_img,
            activebackground="#040B20",
            command=lambda: self.change_week("NEXT"),
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=360, y=60)
        Button(
            self.canvas,
            image=return_img,
            activebackground="#040B20",
            command=lambda: print("RETURN"),
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=60, y=630)
        Button(
            self.canvas,
            image=notes_img,
            activebackground="#040B20",
            command=lambda: print("NOTES"),
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            padx=0,
            pady=0,
        ).place(x=350, y=630)

        self.window.mainloop()

    def draw_current_week_text(self):
        print(self.monday_date)
        print(self.sunday_date)
        text = f"Week of {self.monday_date.strftime('%B %d, %Y')}"

        self.canvas.create_text(
            320,
            30,
            text=text,
            font=("Arial", 18),
            fill="#AFB5D6",
        )

    def draw_day_text(self):
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        x = 139
        for day in days:
            self.canvas.create_text(
                x,
                600,
                text=day,
                font=("Arial", 12, "bold"),
                fill="#AFB5D6",
            )
            x += 60

    def draw_scale_text(self):
        x = 90
        y = 540
        for number in range(1, 11):
            self.canvas.create_text(
                x, y, anchor=SW, text=number, font=("Arial", 13, "bold"), fill="#AFB5D6"
            )
            self.canvas.create_text(
                x + 15,
                y - 7,
                anchor=SW,
                text="_" * 47,
                font=("Arial", 13, "bold"),
                fill="#AFB5D6",
            )  # Remove "* 47" in text to remove lines.
            y -= 44

    def draw_barchart(self):
        stress_levels = [6, 9, 4, 7, 3, 5, 1]

        bar_height = 44
        bar_width = 40
        bar_gap = 20
        left_gap = 120
        bottom_gap = 125

        for x, y in enumerate(stress_levels):
            x0 = x * (bar_gap + bar_width) + left_gap
            y0 = 700 - (y * bar_height + bottom_gap)
            x1 = x0 + bar_width
            y1 = 700 - bottom_gap

            color = None
            match y:
                case 10:
                    color = "#BE0808"
                case 9:
                    color = "#922D05"
                case 8:
                    color = "#A83304"
                case 7:
                    color = "#C55206"
                case 6:
                    color = "#E75E04"
                case 5:
                    color = "#F77119"
                case 4:
                    color = "#F88A41"
                case 3:
                    color = "#F79757"
                case 2:
                    color = "#F9BB93"
                case 1:
                    color = "#F8D5BE"
                case _:
                    color = "white"

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def draw_stress_history(self):
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
