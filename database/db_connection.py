""" This class creates the connection to the database """
import mysql.connector
import mysql.connector.cursor

class db_connection:
    """ Creates the basic database connection add your own information. """
    def __init__(self, user, password):
        """ Initialize the db_connection class with the connection login information """
        self.con = {"user": user, "password": password, "host": "localhost", "port": 3306, 
        "database": "breathe", "raise_on_warnings": True}

    def connect(self):
        """ Makes the connection to the database and return the database curser """
        my_con = mysql.connector.connect(**self.con)
        cursor = my_con.cursor()
        return cursor