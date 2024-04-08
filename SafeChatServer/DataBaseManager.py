import sqlite3

DB_NAME = "ChatServerDB.sqlite"

USERS = "USERS"
MESSAGES = "MESSAGES"

USERNAME = "USERNAME"
HASHED_PASSWORD = "HASHED_PASSWORD"
EMAIL = "EMAIL"

FROM = "FROM"
TO = "TO"
ENCRYPTED_MESSAGE = "ENCRYPTED_MESSAGE"
DATE = "DATE"


ID = "ID"

"""
USERS
USERNAME|PASSWORD|EMAIL|PUBLIC_KEY

MESSAGES
FROM|TO|ENCRYPTED_MESSAGE|DATE

GROUPS
ID|NAME

GROUP_MEMBERS
USER|GROUP_ID

GROUP_MESSAGES
GROUP_ID|ENCRYPTED_MESSAGE|DATE
"""


class DataBaseManager:
    def __init__(self):
        self._connection = sqlite3.connect(DB_NAME, check_same_thread=False)
        self._cursor = self._connection.cursor()  # create a cursor object

        # create the users table
        self._cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {USERS}"
            f"({ID} INTEGER PRIMARY KEY AUTOINCREMENT, {USERNAME} TEXT UNIQUE NOT NULL,"
            f"{HASHED_PASSWORD} BLOB NOT NULL, {EMAIL} TEXT UNIQUE NOT NULL);",)

        # # create the messages table
        # self._cursor.execute("CREATE TABLE IF NOT EXISTS ? (? INTEGER, ? INTEGER, ? BLOB NOT NULL"
        #                      ", FOREIGN KEY(?) REFERENCES ?(?)"
        #                      ", FOREIGN KEY(?) REFERENCES ?(?));",
        #                      (FROM, TO, ENCRYPTED_MESSAGE,
        #                       FROM, USERS, ID,
        #                       TO, USERS, ID))

        self._connection.commit()  # commit the command

    def add_user(self, username: str, hashed_password: bytes, email: str):
        try:
            self._cursor.execute(f"INSERT INTO {USERS} ({USERNAME}, {HASHED_PASSWORD}, {EMAIL})"
                                 f" VALUES (?, ?, ?);",
                                 (username, sqlite3.Binary(hashed_password), email))
            self._connection.commit()
            return True

        except sqlite3.IntegrityError as e:  # when the user already exist
            print(e)
            return False

    def find_user(self, username):
        self._cursor.execute(f"SELECT {USERNAME}, {HASHED_PASSWORD}, {EMAIL} FROM {USERS} WHERE {USERNAME} = ?;",
                             (username, ))
        return self._cursor.fetchone()  # fetch a tuple (username, hashed_password, email) (without the ID)

    def add_message(self, from_user: str, to_user: str, encrypted_message: bytes):
        pass

    def get_all_messages_after(self, to_user: str, after_date):
        pass
