import sqlite3

DB_NAME = "ChatServerDB.sqlite"

USERS = "USERS"
MESSAGES_FOR_OFFLINE_USERS = "MESSAGES"

USERNAME = "USERNAME"
HASHED_PASSWORD = "HASHED_PASSWORD"
EMAIL = "EMAIL"
PUBLIC_KEY = "PUBLIC_KEY"

FROM = "FROM_USER"
TO = "TO_USER"
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
            f"CREATE TABLE IF NOT EXISTS {USERS} ({USERNAME} TEXT PRIMARY KEY,"
            f"{HASHED_PASSWORD} BLOB NOT NULL, {EMAIL} TEXT UNIQUE NOT NULL);")

        # create the messages table
        self._cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {MESSAGES_FOR_OFFLINE_USERS} "
            f"({FROM} TEXT NOT NULL, {TO} TEXT NOT NULL"
            f", {ENCRYPTED_MESSAGE} BLOB NOT NULL, {DATE} TEXT NOT NULL"
            f", FOREIGN KEY({FROM}) REFERENCES {USERS}({USERNAME})"
            f", FOREIGN KEY({TO}) REFERENCES {USERS}({USERNAME}));")

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

    def find_user(self, username: str) -> tuple[str, bytes, str] or None:
        self._cursor.execute(f"SELECT {USERNAME}, {HASHED_PASSWORD}, {EMAIL} FROM {USERS} WHERE {USERNAME} = ?;",
                             (username,))
        return self._cursor.fetchone()  # fetch a tuple (username, hashed_password, email) (without the ID)

    def user_exist(self, username: str) -> bool:
        self._cursor.execute(f"SELECT * FROM {USERS} WHERE {USERNAME} = ?;", (username,))
        return bool(self._cursor.fetchall())  # check if the result list is empty

    def add_message(self, from_user: str, to_user: str, encrypted_message: bytes):
        """
        Add a message to the database
        **The function assume that the users exist**
        :param from_user:
        :param to_user:
        :param encrypted_message:
        :return:
        """

        # add the message with the current datetime (in UTC - Coordinated Universal Time)
        self._cursor.execute(f"INSERT INTO {MESSAGES_FOR_OFFLINE_USERS} ({FROM}, {TO}, {ENCRYPTED_MESSAGE}, {DATE})"
                             f" VALUES (?, ?, ?, datetime(\"now\"));",
                             (from_user, to_user, sqlite3.Binary(encrypted_message)))
        self._connection.commit()  # commit the change

    def pop_messages(self, user: str):
        """
        Pop messages that intended for a specific user
        :param user: the user's username
        :return: the messages List[FROM(string), TO(string), ENCRYPTED_MESSAGE(bytes), DATE(string)]
        """
        # select the messages that sent to the user
        self._cursor.execute(
            f"SELECT * FROM {MESSAGES_FOR_OFFLINE_USERS} WHERE {TO} = ?;", (user, ))
        res = self._cursor.fetchall()

        # delete the messages after fetching
        self._cursor.execute(f"DELETE FROM {MESSAGES_FOR_OFFLINE_USERS} WHERE {TO} = ?;", (user, ))
        self._connection.commit()
        return res
