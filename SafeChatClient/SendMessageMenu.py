from AfterLoginMenu import AfterLoginMenu, DataBaseManager
from Serializer import Serializer
from enum import Enum

MESSAGE_CHUNK_SIZE = 5


class SendMessageMenu(AfterLoginMenu):
    class Option(Enum):
        SIMPLE_TEXT_MESSAGE = 1
        EXIT_AND_CANCEL = 2

    def __init__(self, communicator, database: DataBaseManager, destination):
        super().__init__(communicator, database)

        self._destination = destination
        self._message = None  # store the message content

    @property
    def message_data(self):
        return self._message

    def _text_message(self):
        self._message = input("Please enter the message: ")

        # split the message into chunks and send each chunk to the server
        for i in range(0, len(self._message), MESSAGE_CHUNK_SIZE):
            self._client_communicator.send(
                Serializer.serialize_sending_message(self._message[i: i + MESSAGE_CHUNK_SIZE].encode()))

        # notifies the server that we have sent all the message chunks
        self._client_communicator.send(Serializer.serialize_end_message())

    def _cancel_message_sending(self):
        self._client_communicator.send(Serializer.serialize_cancel_message())

    menu_dict = {Option.SIMPLE_TEXT_MESSAGE: _text_message,
                 Option.EXIT_AND_CANCEL: _cancel_message_sending}
