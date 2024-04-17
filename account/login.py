""" This module will use a tikinter GUI interface
so that a user can login to this application. The colors used is: #040B20 for bg
and #8ddf00 for fg """
from tkinter import *
from database import db_connects
import bcrypt

class login():
    """ This class will login the user """
    window = Tk()

    def __init__(self):
        self.window.geometry("640x540")
        self.window.resizable(height=True, width=False)
        self.window.config(bg="#040B20")
        self.window.title("Please login to your account.")
        self.db_connects = db_connects.db_connnects()
    
    def login_GUI(self):
        """ This is the login graphical interface """
        login_frame = Frame(self.window)
        login_frame.configure(bg="#040B20")
        Label(login_frame, text="Please fill in your login information below",
              font=("Courier", 14), bg="#040B20", fg="#8ddf00").grid(row=0, column=0, columnspan=3, pady=15)
        user_name = StringVar()
        Label(login_frame, text="User Name:",
              font=("Courier", 14), bg="#040B20", fg="#8ddf00").grid(row=2, column=0, pady=15)
        Entry(login_frame, font=("Courier", 14), textvariable=user_name).grid(row=2, column=2, sticky=W)
        password = StringVar()
        Label(login_frame, text="Password:",
              font=("Courier", 14), bg="#040B20", fg="#8ddf00").grid(row=4, column=0, pady=15)
        Entry(login_frame, font=("Courier", 14), textvariable=password).grid(row=4, column=2, sticky=W)
        Button(login_frame, text="LOGIN", bg="#040B20", fg="#8ddf00",
             height=2, width=20, command=lambda: self.login_user(user_name, password,
                        login_frame)).grid(row=6, column=0, columnspan=3)
        login_frame.pack()
        self.window.mainloop()
      
    def login_user(self, user_name, password, login_frame):
        pop_up = Toplevel(login_frame)
        user_name = user_name.get()
        password = password.get().encode('utf-8')
        hashed = self.db_connects.get_hashed_pass(user_name)
        if hashed and bcrypt.checkpw(password, hashed.encode('utf-8')):
            pop_up.title("Login successfull!")
            Label(pop_up, text="Login Successfull!", font=("Courier", 15),
                   bg="#040B20", fg="#8ddf00").pack()
            login_frame.pack_forget()
        else:
            pop_up.title("Login not successful!")
            Label(pop_up, text="The login was unsuccessfull!", font=("Courier", 15),
                   bg="#040B20", fg="#8ddf00").pack()

    



    

login_user = login()
login_user.login_GUI()