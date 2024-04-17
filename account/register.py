""" This module will use a tikinte GUI interface and use a mysql connection
so that a user can register to this application. The colors used is: #24334C for bg
and #61FF64 for fg """
from tkinter import *
import mysql.connector
import mysql.connector.cursor
import bcrypt 
from database import db_connection

class register():
    """ This class register a user to this application. """
    window = Tk()

    def __init__(self):
        """ Initializing the window for the GUI """
        self.window.geometry("640x540")
        self.window.resizable(height=True, width=False)
        self.window.config(bg="#24334C")
        self.window.title("Please register your account.")
        self.con = {"user": "root", "password": "KamelKatt3801", "host": "localhost", "port": 3306, 
        "database": "breathe", "raise_on_warnings": True}
        #self.db = db_connection.db_connection("root", "KamelKatt3801")
        self.my_con = mysql.connector.connect(**self.con)
        self.cursor = self.my_con.cursor()

        

    def register_gui(self):
        """ The Graphical interface for the user register """
        register_frame = Frame(self.window)
        register_frame.configure(bg="#24334C")
        Label(register_frame, text="Register your new account", bg="#24334C", 
              fg="#29FF2C", font=("Arial", 15)).grid(row=0, column=0, columnspan=3, sticky=NSEW)
        Label(register_frame, text="", bg="#24334C").grid(row=1, column=1, columnspan=3)
        first_name = StringVar()
        Label(register_frame, text="Your first name:",  bg="#24334C", 
              fg="#29FF2C", font=("Arial", 14)).grid(row=2, column=0, ipady=8, sticky=E)
        Entry(register_frame, textvariable=first_name, width=30, 
            font=("Arial", 13)).grid(row=2, column=2, ipady=8)
        Label(register_frame, text="", bg="#24334C").grid(row=3, column=1, columnspan=3)
        last_name = StringVar()
        Label(register_frame, text="Your last name:",  bg="#24334C", 
              fg="#29FF2C", font=("Arial", 14)).grid(row=4, column=0, ipady=8, sticky=E)
        Entry(register_frame, textvariable=last_name, width=30, 
            font=("Arial", 13)).grid(row=4, column=2, ipady=8)
        Label(register_frame, text="", bg="#24334C").grid(row=5, column=1, columnspan=3)
        user_name = StringVar()
        Label(register_frame, text="Your user name:",  bg="#24334C", 
              fg="#29FF2C", font=("Arial", 14)).grid(row=6, column=0, ipady=8, sticky=W)
        Entry(register_frame, textvariable=user_name, width=30, 
            font=("Arial", 13)).grid(row=6, column=2, ipady=8,)
        Label(register_frame, text="", bg="#24334C").grid(row=7, column=1, columnspan=3)
        password = StringVar()
        Label(register_frame, text="Your password:",  bg="#24334C", 
              fg="#29FF2C", font=("Arial", 14)).grid(row=8, column=0, ipady=8, sticky=E)
        Entry(register_frame, textvariable=password, width=30, 
            font=("Arial", 13)).grid(row=8, column=2, ipady=8)
        Label(register_frame, text="", bg="#24334C").grid(row=9, column=1, columnspan=3)
        Button(register_frame, text="REGISTER", bg="#29FF2C", fg="#24334C", width=30, 
             height=3, command=lambda: self.register_user(first_name, last_name, user_name, password,
                        register_frame)).grid(row=10, column=0, columnspan=3)
        register_frame.pack()
        self.window.mainloop()

    def register_user(self, first_name, last_name, user_name, password, register_frame):
        """ This method will get the users name from the GUI and add their information to the DB. """
        pop=Toplevel(register_frame)
        first_name = first_name.get()
        last_name = last_name.get()
        user_name = user_name.get()
        password = password.get().encode('utf-8')
        hashed_password = self.salt_hash(password)
        if self.check_user_name(user_name):
                query = "INSERT INTO user (first_name, last_name, user_name, password)" \
                "VALUES (%s, %s, %s, %s)"
                values = (first_name, last_name, user_name,hashed_password)
                self.cursor.execute(query, values)

                if self.cursor.rowcount == 1:
                        self.my_con.commit()
                        pop.title("Register successful1")
                        Label(pop, text="Registered user successfully!").pack()
                else:
                        pop.title("Register unsuccesfull!")
                        Label(pop, text="Please try again!").pack()
        else:
                pop.title("Register unsuccesfull!")
                Label(pop, text="Please try again!").pack()
           
    def salt_hash(self, password):
         """ This will transform their password to an encrypte version. """
         salt = bcrypt.gensalt()
         hashed = bcrypt.hashpw(password, salt)
         return hashed
      
    def check_user_name(self, user_name):
           """ This method will check if the username already exists. """
           query = "SELECT user_name FROM user WHERE user_name = %s"
           values =(user_name, )
           self.cursor.execute(query, values)
           result = self.cursor.fetchone()
           if result:
                return False
           else:
                return True
           
reg = register()

reg.register_gui()