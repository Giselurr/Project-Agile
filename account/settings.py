"""This module will handle the settings for the user."""

from tkinter import Button, Entry, Frame, Label, StringVar, Tk, messagebox

import bcrypt

import main
from database import database_connection, database_handler


class UserSettings:
    """This will handle change of password and user deletion."""

    def __init__(self, logged_in, user_name, window):
        self.is_logged_in = logged_in
        self.user_name = user_name
        self.window = window
        self.db_handler = database_handler.DatabaseHandler()
        self.database = database_connection.DatabaseConnection()

    def user_setting_gui(self):
        """The user settings interface."""
        self.window.geometry("640x700")
        self.window.resizable(height=True, width=False)
        self.window.config(bg="#040B20")
        setting_frame = Frame(self.window, bg="#040B20")
        Label(
            setting_frame,
            text="USER SETTINGS",
            bg="#040B20",
            fg="#FFFFFF",
            font=("Arial", 20),
        ).grid(column=0, row=0, columnspan=2)

        Label(setting_frame, text="", bg="#040B20").grid(row=1, column=0, columnspan=3)

        Label(
            setting_frame,
            text="CHANGE YOUR PASSWORD",
            font=("Arial", 14),
            bg="#040B20",
            fg="#FFFFFF",
        ).grid(row=2, column=0, columnspan=2)
        old_password = StringVar()
        Label(
            setting_frame,
            text="Current password: ",
            font=("Arial", 14),
            bg="#040B20",
            fg="#FFFFFF",
        ).grid(row=3, column=0)
        Entry(setting_frame, textvariable=old_password, font=("Arial", 14)).grid(
            row=3, column=1
        )
        new_password = StringVar()
        Label(
            setting_frame,
            text="New password: ",
            font=("Arial", 14),
            bg="#040B20",
            fg="#FFFFFF",
        ).grid(row=4, column=0)
        Entry(setting_frame, textvariable=new_password, font=("Arial", 14)).grid(
            row=4, column=1
        )
        Label(setting_frame, text="", bg="#040B20").grid(row=5, column=0, columnspan=3)
        Button(
            setting_frame,
            text="CHANGE",
            bg="#040B20",
            fg="white",
            font=("Arial", 14),
            width=18,
            height=1,
            command=lambda: self.change_password(
                setting_frame, old_password, new_password
            ),
        ).grid(row=6, column=0, columnspan=2)

        Label(setting_frame, text="", bg="#040B20").grid(row=7, column=0, columnspan=3)

        Label(
            setting_frame,
            text="DELETE MY ACCOUNT",
            font=("Arial", 14),
            bg="#040B20",
            fg="#FFFFFF",
        ).grid(row=8, column=0, columnspan=2)
        Label(setting_frame, text="", bg="#040B20").grid(row=9, column=0, columnspan=3)
        Button(
            setting_frame,
            text="DELETE",
            bg="#040B20",
            fg="white",
            font=("Arial", 14),
            width=18,
            height=1,
            command=lambda: self.delete_account(
                setting_frame, old_password, new_password
            ),
        ).grid(row=10, column=0, columnspan=2)

        setting_frame.pack()

        self.window.mainloop()

    def change_password(self, setting_frame, old_password, new_password):
        old_password = old_password.get()
        new_password = new_password.get()
        new_password.encode("utf-8")
        self.cursor = self.database.connect()
        hashed = self.db_handler.get_hashed_pass(self.user_name)
        if hashed and bcrypt.checkpw(
            old_password.encode("utf-8"), hashed.encode("utf-8")
        ):
            try:
                query = "UPDATE user SET password = %s WHERE user_name = %s"
                hashed_new_password = self.db_handler.salt_hash(new_password)
                values = (hashed_new_password, self.user_name)
                self.cursor.execute(query, values)
                if self.cursor.rowcount == 1:
                    self.database.commit()
                    messagebox.showinfo("Success", "You have changed the password!")
                else:
                    messagebox.showinfo("Fail", "You have not changed the password!")
            except Exception as e:
                messagebox.showinfo("Error", f"An error occured {e}")

            finally:
                self.cursor.close()
                main.Main.manager_menu_choice(
                    self, setting_frame, "USER_MENU", self.user_name
                )
        else:
            messagebox.showinfo("Warning", "Old password is not correct!")

    def delete_account(self):
        pass


if __name__ == "__main__":
    window = Tk()
    user = UserSettings(True, "P", window)
    user.user_setting_gui()
