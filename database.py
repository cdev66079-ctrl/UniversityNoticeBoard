import mysql.connector
from mysql.connector import Error


class Database:

    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "root"
        self.database = "university_notice_board"
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            if self.connection.is_connected():
                print("MySQL connected successfully!")
                return self.connection

        except Error as e:
            print("MySQL connection error:", e)
            return None

    def fetch_all(self, query, values=None):
        try:
            cursor = self.connection.cursor(dictionary=True)

            cursor.execute(query, values or ())
            results = cursor.fetchall()

            cursor.close()

            return results

        except Error as e:
            print("Query error:", e)
            return []

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed.")