"""This class creates the connection to the database."""

import mysql.connector
import mysql.connector.cursor


class DatabaseConnection:
    """Creates the basic database connection add your own information."""

    def __init__(self):
        """Initialize the db_connection class with the connection login information."""
        user = "root"  # Change to your username.
        password = ""  # Change to your password.
        self.con = {
            "user": user,
            "password": password,
            "host": "localhost",
            "port": 3306,
            "database": "breathe",
            "raise_on_warnings": True,
        }
        self.my_con = None
        self.cursor = None

    def connect(self):
        """Makes the connection to the database and return the database curser."""
        if self.my_con is None or not self.my_con.is_connected():
            self.my_con = mysql.connector.connect(**self.con)
        return self.my_con.cursor()

    def commit(self):
        """Commits the changes to the database."""
        if self.my_con:
            self.my_con.commit()

    def close(self):
        """Closes the database."""
        if self.my_con:
            self.my_con.close()
            self.my_con = None
