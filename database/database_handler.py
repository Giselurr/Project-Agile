"""This modules handles mysql statements."""

import bcrypt

import database.database_connection as database_connection


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

    def get_daily_schedule(self, user_name):
        """Checks and retreives the daily schedule for a user."""
        query = (
            "SELECT start_time, stop_time, task FROM daily_schedule "
            "WHERE user_user_name = %s"
        )
        values = (user_name,)
        curser = self.db.connect()
        self.events = []
        try:
            curser.execute(query, values)
            result = curser.fetchall()
            if result:
                for start, stop, task in result:
                    to_add = (start, stop, task)
                    self.events.append(to_add)
                return self.events
            else:
                self.events = []
                return self.events
        finally:
            curser.close()

    def add_task(self, user_name, start, stop, task):
        """Adds new tasks into the database."""
        query = (
            "INSERT INTO daily_schedule (user_user_name, start_time, stop_time, task)"
            "VALUES (%s, %s, %s, %s)"
        )
        values = (user_name, start, stop, task)
        curser = self.db.connect()
        try:
            curser.execute(query, values)
            if curser.rowcount == 1:
                self.db.commit()
                return True
            else:
                return False

        finally:
            curser.close()

    def get_stress_level(self, user_name, date):
        """Retreives the stress level from the database."""
        query = "SELECT stress_level FROM stress_calender \
        WHERE user_user_name = %s AND date = %s"
        values = (user_name, date)
        curser = self.db.connect()
        try:
            curser.execute(query, values)
            result = curser.fetchone()
            return result[0] if result else 0
        finally:
            curser.close()

    def get_note(self, user_name, date):
        """Retreives the note from the database."""
        query = "SELECT note FROM stress_calender \
        WHERE user_user_name = %s AND date = %s"
        values = (user_name, date)
        curser = self.db.connect()
        try:
            curser.execute(query, values)
            result = curser.fetchone()
            return result[0] if result else "No note"
        finally:
            curser.close()
