from DataBaseManager import DataBaseManager
from MessageNotifier import MessageNotifier
from hashlib import md5


class LoginManager:
    def __init__(self, database: DataBaseManager, message_notifier: MessageNotifier):
        self._db = database
        self._message_notifier = message_notifier
        self._logged_clients = []

    def login(self, username: str, password: str) -> bool:
        user_data = self._db.find_user(username)

        if user_data is None or self.is_online(username):
            return False

        username, real_hashed_password, email = user_data

        # varify the password
        if real_hashed_password == md5(password.encode()).digest():
            print("Client logged in!")
            self._logged_clients.append(username)

            # notify the messages that sent to the client while he was offline
            self._message_notifier.notify_messages(self._db.pop_messages(username))
            return True
        return False

    def sign_up(self, username: str, password: str, email: str):
        res = self._db.add_user(username, md5(password.encode()).digest(), email)
        if res:
            print("Client sign up!")
            self._logged_clients.append(username)
            return True
        return False

    def log_out(self, username: str) -> bool:
        print("Client sign out!")
        self._logged_clients.remove(username)
        return True

    def is_online(self, username):
        return username in self._logged_clients

    @property
    def message_notifier(self):
        return self._message_notifier
