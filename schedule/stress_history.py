import tkinter as tk


class History:
    def __init__(self, window):
        self.window = window
        self.canvas = tk.Canvas(self.window, width=640, height=700, bg="#040B20")
        self.canvas.pack()
        self.window.title("Breathe")
        self.window.iconbitmap("account\images\Breathe_icon.ico")

    def draw_barchart(self):
        stress_levels = [10, 10, 10, 10, 10, 10, 10]
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        y_stretch = 50
        x_stretch = 20
        bar_width = 40
        left_gap = 120
        bottom_gap = 75

        x_position_day_text = 139
        for day in days:
            self.canvas.create_text(
                x_position_day_text,
                650,
                text=day,
                font=("Arial", 12, "bold"),
                fill="#AFB5D6",
            )
            x_position_day_text += 60

        for x, y in enumerate(stress_levels):
            x0 = x * (x_stretch + bar_width) + left_gap
            y0 = 700 - (y * y_stretch + bottom_gap)
            x1 = x0 + bar_width
            y1 = 700 - bottom_gap

            if y == 10:
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="#BE0808")
                self.canvas.create_text(
                    x0 + 10,
                    y0 - 5,
                    anchor=tk.SW,
                    text=y,
                    font=("Arial", 12, "bold"),
                    fill="#AFB5D6",
                )
            elif y == 9:
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="#922D05")
                self.canvas.create_text(
                    x0 + 10,
                    y0 - 5,
                    anchor=tk.SW,
                    text=y,
                    font=("Arial", 12, "bold"),
                    fill="#AFB5D6",
                )
            elif y == 8:
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="#A83304")
                self.canvas.create_text(
                    x0 + 16,
                    y0 - 5,
                    anchor=tk.SW,
                    text=y,
                    font=("Arial", 12, "bold"),
                    fill="#AFB5D6",
                )
            elif y == 7:
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="#C55206")
                self.canvas.create_text(
                    x0 + 16,
                    y0 - 5,
                    anchor=tk.SW,
                    text=y,
                    font=("Arial", 12, "bold"),
                    fill="#AFB5D6",
                )
            elif y == 6:
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="#E75E04")
                self.canvas.create_text(
                    x0 + 16,
                    y0 - 5,
                    anchor=tk.SW,
                    text=y,
                    font=("Arial", 12, "bold"),
                    fill="#AFB5D6",
                )
            elif y == 5:
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="#F77119")
                self.canvas.create_text(
                    x0 + 16,
                    y0 - 5,
                    anchor=tk.SW,
                    text=y,
                    font=("Arial", 12, "bold"),
                    fill="#AFB5D6",
                )
            elif y == 4:
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="#F88A41")
                self.canvas.create_text(
                    x0 + 16,
                    y0 - 5,
                    anchor=tk.SW,
                    text=y,
                    font=("Arial", 12, "bold"),
                    fill="#AFB5D6",
                )
            elif y == 3:
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="#F79757")
                self.canvas.create_text(
                    x0 + 16,
                    y0 - 5,
                    anchor=tk.SW,
                    text=y,
                    font=("Arial", 12, "bold"),
                    fill="#AFB5D6",
                )
            elif y == 2:
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="#F9BB93")
                self.canvas.create_text(
                    x0 + 16,
                    y0 - 5,
                    anchor=tk.SW,
                    text=y,
                    font=("Arial", 12, "bold"),
                    fill="#AFB5D6",
                )
            elif y == 1:
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="#F8D5BE")
                self.canvas.create_text(
                    x0 + 16,
                    y0 - 5,
                    anchor=tk.SW,
                    text=y,
                    font=("Arial", 12, "bold"),
                    fill="#AFB5D6",
                )
            else:
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")
                self.canvas.create_text(
                    x0 + 16,
                    y0 - 5,
                    anchor=tk.SW,
                    text=y,
                    font=("Arial", 12, "bold"),
                    fill="#AFB5D6",
                )

        self.window.mainloop()


if __name__ == "__main__":
    window = tk.Tk()
    stress_history = History(window)
    stress_history.draw_barchart()
