import sqlite3

"""
For each connected user there is different database. (username.sqlite)
The database contains all the messages that the user sent and received
Each database look like this:

USERS:
    USERNAME    |   LAST_PUBLIC_KEY

MESSAGES:
    FROM    |   TO  | MESSAGE
"""


class DataBaseManager:
    def __init__(self):
        self._connection = None
        self._cursor = None

    def connect(self, username):
        self._connection = sqlite3.connect(username + ".sqlite", check_same_thread=False)
        self._cursor = self._connection.cursor()  # create a cursor object

    def pop_and_replace_user_public_key(self, new_public_key):  # -> the last public key
        pass

    def add_message(self, from_user: str, to_user: str, message: str):
        pass

    def get_chat(self, username: str) -> list[tuple[str, str]]:
        pass
