"""This modules handles mysql statements."""

from database import db_connection


class DbConnnects:
    """This class handles the connection to the database
    and it handles sql statements and queries."""

    def __init__(self):
        self.db = db_connection.DbConnection("root", "KamelKatt3801")

    def get_hashed_pass(self, user):
        """Retreives the hashed password from the database."""
        query = "SELECT password FROM user WHERE user_name = %s"
        values = (user,)
        self.curser = self.db.connect()
        try:
            self.curser.execute(query, values)
            result = self.curser.fetchone()
            if result:
                return result[0]
            else:
                return None
        finally:
            if self.curser:
                self.curser.close()

    def check_user_name(self, user_name):
        """This method will check if the username already exists."""
        query = "SELECT user_name FROM user WHERE user_name = %s"
        values = (user_name,)
        self.curser.execute(query, values)
        result = self.curser.fetchone()
        if result:
            return False
        else:
            return True
