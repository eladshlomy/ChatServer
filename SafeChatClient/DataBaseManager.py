import sqlite3

"""
For each connected user there is different database. (username.sqlite)
The database contains all the messages that the user sent and received
Each database look like this:

USERS:
    USERNAME    |   LAST_PUBLIC_KEY     |   LAST_PUBLIC_K   |

MESSAGES:
    SOURCE    |   DESTINATION  | MESSAGE
"""

USERS = "USERS"
MESSAGES = "MESSAGES"

USERNAME = "USERNAME"
LAST_PRIVATE_KEY = "LAST_PRIVATE_K"  # my private
LAST_PUBLIC_KEY = "LAST_PUBLIC_K"  # the other user public

SOURCE = "SOURCE"
DESTINATION = "DESTINATION"
CONTENT = "CONTENT"


class DataBaseManager:
    def __init__(self):
        self._connection = None
        self._cursor = None
        self._username = None

    @property
    def username(self):
        return self._username

    def is_connected(self):
        return self._connection is not None

    def connect(self, username):
        self._connection = sqlite3.connect(username + ".sqlite", check_same_thread=False)
        self._cursor = self._connection.cursor()  # create a cursor object
        self._username = username

        self._init()  # init the db

    def disconnect(self):
        if self.is_connected():
            self._connection.close()
            self._connection = None

    def _init(self):
        if self.is_connected():
            self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {USERS} ({USERNAME} TEXT PRIMARY KEY,"
                                 f"{LAST_PUBLIC_KEY} BLOB, {LAST_PRIVATE_KEY} BLOB);")

            self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {MESSAGES} ({SOURCE} TEXT NOT NULL,"
                                 f"{DESTINATION} TEXT NOT NULL, {CONTENT} TEXT NOT NULL);")

    # ############################# users table handling #############################
    def get_last_private_key(self, username: str) -> bytes:
        self._cursor.execute(f"SELECT {LAST_PRIVATE_KEY} FROM {USERS} WHERE {USERNAME} = ?;", (username,))
        res = self._cursor.fetchone()
        return res[0] if res else res

    def get_last_other_public_key(self, username: str) -> bytes:
        self._cursor.execute(f"SELECT {LAST_PUBLIC_KEY} FROM {USERS} WHERE {USERNAME} = ?;", (username,))
        res = self._cursor.fetchone()
        return res[0] if res else res

    def set_last_private_key(self, username: str, new_private_key: bytes):
        self._cursor.execute(f"INSERT INTO {USERS} ({USERNAME}, {LAST_PUBLIC_KEY}, {LAST_PRIVATE_KEY}) "
                             f"VALUES (?, ?, ?) ON "
                             f"CONFLICT({USERNAME}) DO UPDATE SET {LAST_PRIVATE_KEY} = excluded.{LAST_PRIVATE_KEY};",
                             (username, None, new_private_key))
        self._connection.commit()

    def set_last_other_public_key(self, username: str, new_public_key: bytes):
        self._cursor.execute(f"INSERT INTO {USERS} ({USERNAME}, {LAST_PUBLIC_KEY}, {LAST_PRIVATE_KEY}) "
                             f"VALUES (?, ?, ?) ON "
                             f"CONFLICT({USERNAME}) DO UPDATE SET {LAST_PUBLIC_KEY} = excluded.{LAST_PUBLIC_KEY};",
                             (username, new_public_key, None))
        self._connection.commit()

    # ############################ message table handling ############################

    def add_message(self, from_user: str, to_user: str, message: str):
        self._cursor.execute(f"INSERT INTO {MESSAGES} ({SOURCE}, {DESTINATION}, {CONTENT}) VALUES (?, ?, ?);",
                             (from_user, to_user, message))
        self._connection.commit()

    def add_sent_message(self, to_user: str, message: str):
        self.add_message(self._username, to_user, message)

    def add_received_message(self, from_user: str, message: str):
        self.add_message(from_user, self._username, message)

    def get_chat(self, username: str) -> list[tuple[str, str, str]]:
        self._cursor.execute(f"SELECT * FROM {MESSAGES} WHERE ({SOURCE} = ? OR {DESTINATION} = ?);",
                             (username, username))
        return self._cursor.fetchall()

    def delete_chat(self, username: str):
        self._cursor.execute(f"DELETE FROM {MESSAGES} WHERE ({SOURCE} = ? OR {DESTINATION} = ?);",
                             (username, username))
        self._connection.commit()

    def users_in_chat(self):
        self._cursor.execute(f"SELECT DISTINCT VALUE FROM "
                             f"(SELECT {SOURCE} AS VALUE FROM {MESSAGES} UNION "
                             f"SELECT {DESTINATION} AS VALUE FROM {MESSAGES}) WHERE VALUE != ?;", (self._username, ))
        return [username[0] for username in self._cursor.fetchall()]

