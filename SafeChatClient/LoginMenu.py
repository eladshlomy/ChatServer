import ClientMenu
import enum
from Serializer import Serializer


class LoginOptions(enum.Enum):
    LOG_IN = 1
    SIGN_UP = 2


class LoginMenu(ClientMenu.ClientMenu):
    @staticmethod
    def _input_process(user_choice):
        return LoginOptions(int(user_choice))

    def _sign_up(self):
        self._username = input("Please enter your username: ")
        password = input("Please choose a password: ")
        email = input("Please enter your email: ")

        req_buffer = Serializer.serialize_signup(self._username, password, email)

        self._client_communicator.send(req_buffer)  # send the request to the server

    def _login(self):
        self._username = input("Please enter your username: ")
        password = input("Please choose a password: ")

        req_buffer = Serializer.serialize_login(self._username, password)

        self._client_communicator.send(req_buffer)  # send the request to the server

    def get_username(self) -> str or None:
        return self._username

    menu_dict = {LoginOptions.LOG_IN: _login,
                 LoginOptions.SIGN_UP: _sign_up}
