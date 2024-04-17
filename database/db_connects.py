from database import db_connection
import mysql.connector
import mysql.connector.cursor

class db_connnects():
    def __init__(self):
        self.db = db_connection.db_connection("root", "KamelKatt3801")

    def get_hashed_pass(self, user):
        query = "SELECT password FROM user WHERE user_name = %s"
        values = (user, )
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
        
db = db_connnects()
print(db)
print(db.get_hashed_pass("PAW"))
    