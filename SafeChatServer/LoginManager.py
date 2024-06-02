from DataBaseManager import DataBaseManager
from MessageNotifier import MessageNotifier
from hashlib import md5


class LoginManager:
    def __init__(self, database: DataBaseManager, message_notifier: MessageNotifier):
        self._db = database
        self._message_notifier = message_notifier
        self._logged_clients = []

    def login(self, username: str, password: str, public_key: bytes) -> bool:
        user_data = self._db.find_user(username)

        if user_data is None or self.is_online(username):
            return False

        username, real_hashed_password, email = user_data

        # varify the password
        if real_hashed_password == md5(password.encode()).digest():
            print("Client logged in!", username)
            self._db.update_public_key(username, public_key)

            self._logged_clients.append(username)

            # notify the messages that sent to the client while he was offline
            self._message_notifier.notify_messages(self._db.pop_messages(username))
            return True
        return False

    def sign_up(self, username: str, password: str, email: str, public_key: bytes) -> bool:
        res = self._db.add_user(username, md5(password.encode()).digest(), email, public_key)

        if res:
            print("Client sign up!", username)
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
