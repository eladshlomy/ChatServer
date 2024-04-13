import sqlite3
import datetime

DB_NAME = "ChatServerDB.sqlite"

USERS = "USERS"
MESSAGES = "MESSAGES"

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
ID|FROM|TO|ENCRYPTED_MESSAGE|DATE

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
            f"{HASHED_PASSWORD} BLOB NOT NULL, {EMAIL} TEXT UNIQUE NOT NULL);")  # {PUBLIC_KEY} BLOB NOT NULL

        # create the messages table
        self._cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {MESSAGES} ({ID} INTEGER PRIMARY KEY AUTOINCREMENT"
            f", {FROM} INTEGER NOT NULL, {TO} INTEGER NOT NULL"
            f", {ENCRYPTED_MESSAGE} BLOB NOT NULL, {DATE} TEXT NOT NULL"
            f", FOREIGN KEY({FROM}) REFERENCES {USERS}({ID})"
            f", FOREIGN KEY({TO}) REFERENCES {USERS}({ID}));")

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

    def find_user(self, username: str):
        self._cursor.execute(f"SELECT {USERNAME}, {HASHED_PASSWORD}, {EMAIL} FROM {USERS} WHERE {USERNAME} = ?;",
                             (username,))
        return self._cursor.fetchone()  # fetch a tuple (username, hashed_password, email) (without the ID)

    def user_exist(self, username: str) -> bool:
        self._cursor.execute(f"SELECT * FROM {USERS} WHERE {USERNAME} = ?;", (username,))
        return bool(self._cursor.fetchall())  # check if the result list is empty

    def add_message(self, from_user_id: int, to_user_id: int, encrypted_message: bytes):
        """
        Add a message to the database
        :param from_user_id:
        :param to_user_id:
        :param encrypted_message:
        :return:
        """

        # add the message with the current datetime (in UTC - Coordinated Universal Time)
        self._cursor.execute(f"INSERT INTO {MESSAGES} ({FROM}, {TO}, {ENCRYPTED_MESSAGE}, {DATE})"
                             f" VALUES (?, ?, ?, datetime(\"now\"));",
                             (from_user_id, to_user_id, encrypted_message))
        self._connection.commit()

    def get_user_id(self, username: str) -> int:
        """
        The function returns the id of specific username
        Assume that the user exist
        :param username: the user's username
        :return: the user's ID
        """

        self._cursor.execute(F"SELECT {ID} FROM {USERS} WHERE {USERNAME} = ?;", (username,))
        return int(self._cursor.fetchone()[0])  # raise IndexError if user is not exist

    def get_all_messages_after(self, to_user_id: int, after_date: datetime.datetime):
        """
        Get update of the new messages of specific user
        **The function assume that the user exist**
        :param to_user_id: the destination of the message
        :param after_date: the last updated date
        :return: list of all the messages after this date
        """

        self._cursor.execute(f"SELECT {ID}, {FROM}, {ENCRYPTED_MESSAGE}, {DATE} FROM {MESSAGES} "
                             f"WHERE {TO} = ? AND datetime({DATE}) >= datetime(?);",
                             (to_user_id, str(after_date)))
        return self._cursor.fetchall()
