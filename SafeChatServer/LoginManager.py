from DataBaseManager import DataBaseManager
from hashlib import md5
from socket import socket


class LoginManager:
    def __init__(self, database: DataBaseManager):
        self._db = database
        self._logged_clients = {}

    def login(self, socket_reference: socket, username: str, password: str) -> bool:
        user_data = self._db.find_user(username)

        if user_data is None:
            return False

        username, real_hashed_password, email = user_data

        # varify the password
        if real_hashed_password == md5(password.encode()).digest():
            print("Client logged in!")
            self._logged_clients[username] = socket_reference
            return True
        return False

    def sign_up(self, socket_reference: socket, username: str, password: str, email: str):
        res = self._db.add_user(username, md5(password.encode()).digest(), email)
        if res:
            print("Client sign up!")
            self._logged_clients[username] = socket_reference
            return True
        return False

    def log_out(self, username: str) -> bool:
        print("Client sign out!")
        self._logged_clients.pop(username)
        return True

    def log_out_by_socket(self, socket_reference: socket):
        for key, val in self._logged_clients.copy().items():
            if val == socket_reference:
                print("Client sign out!")
                self._logged_clients.pop(key)

