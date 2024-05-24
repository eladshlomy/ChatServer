import ClientMenu
from enum import Enum
from Serializer import Serializer


class LoginMenu(ClientMenu.ClientMenu):
    class Option(Enum):
        LOG_IN = 1
        SIGN_UP = 2

    def _sign_up(self):
        username = input("Please enter your username: ")
        password = input("Please choose a password: ")
        email = input("Please enter your email: ")

        public_key = self._encryption_manager.create_key_for_new_user_and_load(username)
        req_buffer = Serializer.serialize_signup(username, password, email, public_key)

        self._client_communicator.send(req_buffer)  # send the request to the server

    def _login(self):
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")

        public_key = self._encryption_manager.load_public_key(username)
        if public_key is None:
            print("ERROR: Can not find the private key's of", username)
            public_key = self._encryption_manager.create_key_for_new_user_and_load(username)
        req_buffer = Serializer.serialize_login(username, password, public_key)

        self._client_communicator.send(req_buffer)  # send the request to the server

    menu_dict = {Option.LOG_IN: _login,
                 Option.SIGN_UP: _sign_up}
