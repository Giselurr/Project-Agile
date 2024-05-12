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
        """Check if the username already exist."""
        query = "SELECT user_name FROM user WHERE user_name = %s"
        values = (user_name,)
        curser = self.db.connect()
        try:
            curser.execute(query, values)
            result = curser.fetchone()
            return bool(result)
        finally:
            curser.close()

    def check_date(self, user_name, current_date):
        """Check if date exist in database for stress-level."""
        query = (
            "SELECT calender_id, date FROM stress_calender WHERE user_user_name = %s"
        )
        new_date = current_date.strftime("%Y-%m-%d")
        values = (user_name,)
        curser = self.db.connect()
        try:
            curser.execute(query, values)
            result = curser.fetchall()
            for calender_id, db_date in result:
                db_dates = db_date.strftime("%Y-%m-%d")
                if db_dates == new_date:
                    return (calender_id, True)
            return ("", False)
        finally:
            curser.close()

    def update_row(self, colour, notes, id):
        """Update exciting row in database."""
        query = "UPDATE stress_calender SET stress_level = %s, note = %s \
              WHERE calender_id = %s"

        values = (colour, notes, id)
        curser = self.db.connect()
        try:
            curser.execute(query, values)
            if curser.rowcount == 1:
                self.db.commit()

        finally:
            curser.close()

    def salt_hash(self, password):
        """This will transform their password to an encrypte version."""
        if isinstance(password, str):
            password = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        return hashed
