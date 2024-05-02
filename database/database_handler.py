"""This modules handles mysql statements."""

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

    def check_date(self, user_name, date):
        """Later."""
        query = (
            "SELECT calender_id, date FROM stress_calender WHERE user_user_name = %s"
        )
        date.strftime("%Y-%m-%d")
        values = (user_name,)
        curser = self.db.connect()
        try:
            curser.execute(query, values)
            result = curser.fetchall()
            for calender_id, db_dates in result:
                if db_dates == date:
                    return (calender_id, True)
            return ("", False)
        finally:
            curser.close()

    def update_row(self, top, colour, notes, id):
        """Later."""
        top.destroy()
        query = "UPDATE stress_calender SET stress_level = %s, note = %s \
            WHERE calender_id = %s"
        values = (colour, notes, id)
        curser = self.db.connect()
        try:
            curser.execute(query, values)
            result = curser.fetchone()

        finally:
            curser.close()
