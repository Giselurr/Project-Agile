import tkinter as tk

from PIL import Image, ImageTk


class DisplayExercise:
    def __init__(self, window):
        self.window = window
        self.window.geometry("640x700")
        self.window.resizable(height=True, width=False)
        self.window.config(bg="#040B20")
        self.display_imagery()

    def display_imagery(self):
        file = "BREATHE.gif"
        self.animation = Image.open(file)
        self.frames = self.animation.n_frames

        self.gif_objects = []
        for i in range(self.frames):
            self.animation.seek(i)
            photo = ImageTk.PhotoImage(self.animation)
            self.gif_objects.append(photo)

        self.current_frame = 0
        self.gif_label = tk.Label(
            self.window, image=self.gif_objects[self.current_frame]
        )
        self.gif_label.pack(side="top", pady=70) 

       
        self.button_frame = tk.Frame(self.window, bg="#040B20")
        self.button_frame.pack()

        
        self.start = tk.Button(
            self.button_frame,
            text="START",
            bg="#040B20",
            fg="white",
            font="Arial",
            width=8,
            height=1,
            command=self.animate,
        )
        self.start.pack(side="left", padx=10, pady=10)

        
        self.stop = tk.Button(
            self.button_frame,
            text="CANCEL",
            bg="#040B20",
            fg="white",
            font="Arial",
            width=8,
            height=1,
            command=self.cancel,
        )
        self.stop.pack(side="left", padx=10, pady=10)

        
        self.button_frame.place(relx=0.5, rely=0.5, anchor="center", y=220)

    def animate(self):
        self.current_frame += 1
        if self.current_frame == self.frames:
            self.current_frame = 0
        self.gif_label.configure(image=self.gif_objects[self.current_frame])
        self.window.after(50, self.animate)

    def cancel(self):
        self.window.destroy()



if __name__ == "__main__":
    main_window = tk.Tk()
    exercise = DisplayExercise(main_window)
    main_window.mainloop()
