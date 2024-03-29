import sqlite3

DB_NAME = "ChatServerDB.sqlite"

USERS = "USERS"

USERNAME = "USERNAME"
HASHED_PASSWORD = "HASHED_PASSWORD"
EMAIL = "EMAIL"


class DataBaseManager:
    def __init__(self):
        self._connection = sqlite3.connect(DB_NAME)
        self._cursor = self._connection.cursor()  # create a cursor object

        # create the users table
        self._cursor.execute(
            "CREATE TABLE IF NOT EXIST ? (? TEXT PRIMARY KEY, ? BLOB NOT NULL, ? TEXT NOT NULL);",
            (USERS, USERNAME, HASHED_PASSWORD, EMAIL))

        self._connection.commit()  # commit the command

    def add_user(self, username: str, hashed_password: bytes, email: str):
        try:
            self._cursor.execute("INSERT INTO ? (?, ?, ?) VALUES ('?', ?, '?');",
                                 (USERS, USERNAME, HASHED_PASSWORD, EMAIL,
                                  username, sqlite3.Binary(hashed_password), email))
            self._connection.commit()
            return True

        except sqlite3.IntegrityError:  # when the user already exist
            return False

    def find_user(self, username):
        self._cursor.execute("SELECT * FROM ? WHERE ? = ?;", (USERS, USERNAME, username))
        return self._cursor.fetchone()  # fetch a tuple (username, hashed_password, email)
