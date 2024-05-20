import ClientMenu
from enum import Enum
from Serializer import Serializer
from DataBaseManager import DataBaseManager
from MenuFactory import MenuFactory

MESSAGE_CHUNK_SIZE = 5


class AfterLoginMenu(ClientMenu.ClientMenu):
    class Option(Enum):
        SEND_MESSAGE = 1
        VIEW_CHAT = 2
        LOG_OUT = 3

    def __init__(self, communicator, database: DataBaseManager):
        super().__init__(communicator)
        self._database = database

        self._destination = None

    @property
    def destination(self):
        return self._destination

    def _logout(self):
        req_buffer = Serializer.serialize_logout()
        self._client_communicator.send(req_buffer)  # send the request to the server

    def _send_message_req(self, dest):
        self._destination = dest
        self._client_communicator.send(Serializer.serialize_send_message_req(self._destination))

    def _send_message(self):
        self._send_message_req(input("Please enter the username you would like to send a message to: "))

    def _view_chat(self):
        return MenuFactory.create_choose_chat_menu(self._client_communicator, self._database)

    menu_dict = {Option.SEND_MESSAGE: _send_message,
                 Option.VIEW_CHAT: _view_chat,
                 Option.LOG_OUT: _logout}
