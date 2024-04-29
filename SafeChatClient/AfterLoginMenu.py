import ClientMenu
import enum
from Serializer import Serializer


MESSAGE_CHUNK_SIZE = 5


class AfterLoginOptions(enum.Enum):
    SEND_MESSAGE = 1
    LOG_OUT = 2


class AfterLoginMenu(ClientMenu.ClientMenu):
    @staticmethod
    def _input_process(user_choice):
        return AfterLoginOptions(int(user_choice))

    def _logout(self):
        req_buffer = Serializer.serialize_logout()
        self._client_communicator.send(req_buffer)  # send the request to the server

    def _send_message(self):
        destination = input("Please enter the username you would like to send a message to: ")
        self._client_communicator.send(Serializer.serialize_send_message_req(destination))

    menu_dict = {AfterLoginOptions.SEND_MESSAGE: _send_message,
                 AfterLoginOptions.LOG_OUT: _logout}
