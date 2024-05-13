import ClientMenu
from enum import Enum
from Serializer import Serializer


class LoginMenu(ClientMenu.ClientMenu):
    class Option(Enum):
        LOG_IN = 1
        SIGN_UP = 2

    def _sign_up(self):
        self._username = input("Please enter your username: ")
        password = input("Please choose a password: ")
        email = input("Please enter your email: ")

        req_buffer = Serializer.serialize_signup(self._username, password, email)

        self._client_communicator.send(req_buffer)  # send the request to the server

    def _login(self):
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")

        req_buffer = Serializer.serialize_login(username, password)

        self._client_communicator.send(req_buffer)  # send the request to the server

    menu_dict = {Option.LOG_IN: _login,
                 Option.SIGN_UP: _sign_up}
