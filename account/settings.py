"""This module will handle the settings for the user."""

from tkinter import (
    Button,
    E,
    Entry,
    Frame,
    Label,
    PhotoImage,
    StringVar,
    Tk,
    messagebox,
)

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
        self.setting_frame = Frame(self.window, bg="#040B20")
        return_button = PhotoImage(file=r"account\images\return_small.png")
        Label(
            self.setting_frame,
            text="USER SETTINGS",
            bg="#040B20",
            fg="#FFFFFF",
            font=("Arial", 20),
        ).grid(column=0, row=0, columnspan=2)

        Label(self.setting_frame, text="", bg="#040B20").grid(
            row=1, column=0, columnspan=3
        )

        Label(
            self.setting_frame,
            text="CHANGE YOUR PASSWORD",
            font=("Arial", 14),
            bg="#040B20",
            fg="#FFFFFF",
        ).grid(row=2, column=0, columnspan=2)
        self.old_password = StringVar()
        Label(
            self.setting_frame,
            text="Current password: ",
            font=("Arial", 14),
            bg="#040B20",
            fg="#FFFFFF",
        ).grid(row=3, column=0)
        Entry(
            self.setting_frame, textvariable=self.old_password, font=("Arial", 14)
        ).grid(row=3, column=1)
        self.new_password = StringVar()
        Label(
            self.setting_frame,
            text="New password: ",
            font=("Arial", 14),
            bg="#040B20",
            fg="#FFFFFF",
        ).grid(row=4, column=0)
        self.entry_change = Entry(
            self.setting_frame, textvariable=self.new_password, font=("Arial", 14)
        )
        self.entry_change.grid(row=4, column=1)
        self.entry_change.bind("<Return>", self.press_enter)
        Label(self.setting_frame, text="", bg="#040B20").grid(
            row=5, column=0, columnspan=3
        )
        Button(
            self.setting_frame,
            activebackground="#040B20",
            text="CHANGE",
            bg="#040B20",
            fg="white",
            font="Arial",
            width=8,
            height=1,
            command=lambda: self.change_password(
                self.setting_frame, self.old_password, self.new_password
            ),
        ).grid(row=6, column=1, sticky=E)

        Label(self.setting_frame, text="", bg="#040B20").grid(
            row=7, column=0, columnspan=3
        )

        Label(
            self.setting_frame,
            text="DELETE MY ACCOUNT",
            font=("Arial", 14),
            bg="#040B20",
            fg="#FFFFFF",
        ).grid(row=8, column=0, columnspan=2)
        self.password = StringVar()
        Label(
            self.setting_frame,
            text="Enter your password: ",
            font=("Arial", 14),
            bg="#040B20",
            fg="#FFFFFF",
        ).grid(row=9, column=0)
        self.entry_delete = Entry(
            self.setting_frame, textvariable=self.password, font=("Arial", 14)
        )
        self.entry_delete.grid(row=9, column=1)
        self.entry_delete.bind("<Return>", self.press_enter)
        Label(self.setting_frame, text="", bg="#040B20").grid(
            row=10, column=0, columnspan=3
        )

        Button(
            self.setting_frame,
            activebackground="#040B20",
            text="DELETE",
            bg="#040B20",
            fg="white",
            font="Arial",
            width=8,
            height=1,
            command=lambda: self.delete_account(self.setting_frame, self.password),
        ).grid(row=11, column=1, sticky=E)

        Button(
            self.setting_frame,
            image=return_button,
            borderwidth=0,
            highlightthickness=0,
            activebackground="#040B20",
            command=lambda: main.Main.manager_menu_choice(
                self, self.setting_frame, "USER_MENU", self.user_name, None, None
            ),
        ).grid(row=12, column=1, pady=40, sticky=E)

        self.setting_frame.pack()

        self.window.mainloop()

    def press_enter(self, event):
        if event.widget == self.entry_change:
            self.change_password(
                self.setting_frame, self.old_password, self.new_password
            )
        if event.widget == self.entry_delete:
            self.delete_account(self.setting_frame, self.password)

    def change_password(self, setting_frame, old_password, new_password):
        """This method will allow the user to change their password."""
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
                    messagebox.showinfo("Error!", "You have not changed the password!")
            except Exception as e:
                messagebox.showinfo("Error!", f"An error occured {e}")

            finally:
                self.cursor.close()
                main.Main.manager_menu_choice(
                    self, setting_frame, "USER_MENU", self.user_name, None, None
                )
        else:
            messagebox.showinfo("Error!", "Old password is not correct!")

    def delete_account(self, setting_frame, password):
        """After the user confirms with their password,
        they will delete their account."""
        password = password.get()
        self.cursor = self.database.connect()
        hashed = self.db_handler.get_hashed_pass(self.user_name)
        if hashed and bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8")):
            try:
                query = "DELETE FROM user WHERE user_name = %s"
                print(self.user_name)
                values = (self.user_name,)
                self.cursor.execute(query, values)
                if self.cursor.rowcount == 1:
                    self.database.commit()
                    messagebox.showinfo(
                        "Success!", "Your account has successfully been deleted."
                    )
                    main.Main.manager_menu_choice(
                        self, setting_frame, "MAIN_MENU", None, None, None
                    )
                else:
                    messagebox.showinfo(
                        "Error!",
                        ("Something went wrong, your account has not been deleted!"),
                    )
            except Exception as e:
                messagebox.showinfo("Error!", f"There was an error: {e}")
            finally:
                self.cursor.close()
        else:
            messagebox.showinfo("Error!", "Your password was incorrect!")


if __name__ == "__main__":
    window = Tk()
    user = UserSettings(True, "P", window)
    user.user_setting_gui()
