import tkinter as tk

from PIL import Image, ImageTk

import main


class DisplayExercise:
    def __init__(self, window, user, reminder):
        self.window = window
        self.is_not_running = True
        self.user = user
        self.window.title("Breathe")
        self.window.iconbitmap("breathing\images\Breathe_icon.ico")
        self.box_brathing_frame = tk.Frame(self.window, bg="#040B20")
        self.box_brathing_frame.pack()
        self.reminder = reminder

    def display_imagery(self):
        # starting all the frames

        self.button_frame = tk.Frame(self.window, bg="#040B20")
        self.button_frame.pack()
        self.start_frame = tk.Frame(self.button_frame, bg="#040B20")
        self.stop_frame = tk.Frame(self.button_frame, bg="#040B20")
        self.cancel_frame = tk.Frame(self.button_frame, bg="#040B20")
        self.restart_frame = tk.Frame(self.button_frame, bg="#040B20")

        file = "breathing\gifs\BREATHE.gif"
        self.animation = Image.open(file)
        self.frames = self.animation.n_frames

        self.gif_objects = []
        for i in range(self.frames):
            self.animation.seek(i)
            photo = ImageTk.PhotoImage(self.animation)
            self.gif_objects.append(photo)

        self.current_frame = 0
        self.gif_label = tk.Label(
            self.box_brathing_frame, image=self.gif_objects[self.current_frame]
        )
        self.gif_label.pack(side="top", pady=70)

        while self.is_not_running:
            tk.Button(
                self.start_frame,
                text="START",
                bg="#040B20",
                fg="white",
                font="Arial",
                width=8,
                height=1,
                command=self.animate,
            ).pack(side="left", padx=10, pady=10)
            self.is_not_running = False

        while not self.is_not_running:
            tk.Button(
                self.stop_frame,
                text="STOP",
                bg="#040B20",
                fg="white",
                font="Arial",
                width=8,
                height=1,
                command=self.stop,
            ).pack(side="left", padx=10, pady=10)
            self.is_not_running = True

        tk.Button(
            self.cancel_frame,
            text="CANCEL",
            bg="#040B20",
            fg="white",
            font="Arial",
            width=8,
            height=1,
            command=self.cancel,
        ).pack(side="left", padx=10, pady=10)

        tk.Button(
            self.restart_frame,
            text="RESTART",
            bg="#040B20",
            fg="white",
            font="Arial",
            width=8,
            height=1,
            command=self.restart,
        ).pack(side="left", padx=10, pady=10)

        # Places and packs the frames for the buttons
        self.start_frame.pack(fill="both", side="left")
        self.cancel_frame.pack(fill="both", side="right")
        self.restart_frame.pack(fill="both", side="right")
        self.button_frame.place(relx=0.5, rely=0.5, anchor="center", y=220)

    def animate(self):
        self.start_frame.pack_forget()
        self.stop_frame.pack(fill="both", side="left")
        self.current_frame += 1
        if self.current_frame == self.frames:
            self.current_frame = 0
        self.gif_label.configure(image=self.gif_objects[self.current_frame])
        self.loop = self.window.after(50, self.animate)

    def cancel(self):
        self.button_frame.pack_forget()
        self.button_frame.place_forget()
        main.Main.manager_menu_choice(
            self, self.box_brathing_frame, "USER_MENU", self.user, None, self.reminder
        )

    def stop(self):
        self.stop_frame.pack_forget()
        self.start_frame.pack(fill="both", side="left")
        self.window.after_cancel(self.loop)

    def restart(self):
        self.current_frame = 0
        tk.Label(
            self.box_brathing_frame, image=self.gif_objects[self.current_frame]
        ).pack(side="top", pady=70)


if __name__ == "__main__":
    main_window = tk.Tk()
    exercise = DisplayExercise(main_window, "Pernilla")
    exercise.display_imagery()
    main_window.mainloop()
