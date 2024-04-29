import tkinter as tk

from PIL import Image, ImageTk

from account import user


class DisplayExercise:
    def __init__(self, window, user):
        self.window = window
        self.window.geometry("640x700")
        self.window.resizable(height=True, width=False)
        self.window.config(bg="#040B20")
        self.is_not_running = True
        self.user = user

    def display_imagery(self):
        # starting all the frames
        self.box_brathing_frame = tk.Frame(self.window)
        self.box_brathing_frame.config(bg="#040B20")
        self.box_brathing_frame.pack()
        self.button_frame = tk.Frame(self.window)
        self.button_frame.config(bg="#040B20")
        self.button_frame.pack()
        self.start_frame = tk.Frame(self.button_frame, bg="#040B20")
        self.stop_frame = tk.Frame(self.button_frame, bg="#040B20")

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

        tk.Button(
            self.stop_frame,
            text="CANCEL",
            bg="#040B20",
            fg="white",
            font="Arial",
            width=8,
            height=1,
            command=self.cancel,
        ).pack(side="left", padx=10, pady=10)

        # Places and packs the frames for the buttons
        self.start_frame.pack(fill="both", side="left")
        self.stop_frame.pack(fill="both", side="left")
        self.button_frame.place(relx=0.5, rely=0.5, anchor="center", y=220)

    def animate(self):
        self.start_frame.pack_forget()
        self.current_frame += 1
        if self.current_frame == self.frames:
            self.current_frame = 0
        self.gif_label.configure(image=self.gif_objects[self.current_frame])
        self.window.after(50, self.animate)

    def cancel(self):
        self.box_brathing_frame.pack_forget()
        self.button_frame.pack_forget()
        self.button_frame.place_forget()
        user_redirect = user.User(True, self.user, self.window)
        user_redirect.user_gui()


if __name__ == "__main__":
    main_window = tk.Tk()
    exercise = DisplayExercise(main_window, "Pernilla")
    exercise.display_imagery()
    main_window.mainloop()
