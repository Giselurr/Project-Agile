"""This modules handles mysql statements."""

from database import database_connection


class DatabaseHandler:
    """This class handles the connection to the database
    and it handles sql statements and queries."""

    def __init__(self):
        self.db = database_connection.DatabaseConnection(
            "root", "Cbth2468"
        )  # Change to your db username and password.

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
