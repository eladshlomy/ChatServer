import ClientMenu
import enum
from Serializer import Serializer

MESSAGE_CHUNK_SIZE = 5


class AfterLoginMenu(ClientMenu.ClientMenu):
    class Option(enum.Enum):
        SEND_MESSAGE = 1
        LOG_OUT = 2

    def __init__(self, communicator, username: str):
        super().__init__(communicator)
        self._username = username

        self._destination = None

        print("Hello", username + "!")
        print("Welcome back")

    @property
    def username(self):
        return self._username

    @property
    def destination(self):
        return self._destination

    def _logout(self):
        req_buffer = Serializer.serialize_logout()
        self._client_communicator.send(req_buffer)  # send the request to the server

    def _send_message(self):
        self._destination = input("Please enter the username you would like to send a message to: ")
        self._client_communicator.send(Serializer.serialize_send_message_req(self._destination))

    menu_dict = {Option.SEND_MESSAGE: _send_message,
                 Option.LOG_OUT: _logout}
