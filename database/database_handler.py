"""This modules handles mysql statements."""

import bcrypt

from database import database_connection


class DatabaseHandler:
    """This class handles the connection to the database
    and it handles sql statements and queries."""

    def __init__(self):
        self.db = database_connection.DatabaseConnection()

    def get_hashed_pass(self, user):
        """Retreives the hashed password from the database."""
        query = "SELECT password FROM user WHERE user_name = %s"
        values = (user,)
        curser = self.db.connect()
        try:
            curser.execute(query, values)
            result = curser.fetchone()
            return result[0] if result else None
        finally:
            curser.close()

    def check_user_name(self, user_name):
        """This method will check if the username already exists."""
        query = "SELECT user_name FROM user WHERE user_name = %s"
        values = (user_name,)
        curser = self.db.connect()
        try:
            curser.execute(query, values)
            result = curser.fetchone()
            return bool(result)
        finally:
            curser.close()

    def salt_hash(self, password):
        """This will transform their password to an encrypte version."""
        if isinstance(password, str):
            password = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        return hashed
