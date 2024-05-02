from ClientMenu import ClientMenu
from Serializer import Serializer
from enum import Enum

MESSAGE_CHUNK_SIZE = 512


class SendMessageOptions(Enum):
    SIMPLE_TEXT_MESSAGE = 1
    EXIT_AND_CANCEL = 2


class SendMessageMenu(ClientMenu):
    @staticmethod
    def _input_process(user_choice):
        return SendMessageOptions(int(user_choice))

    def _text_message(self):
        message = input("Please enter the message: ")

        # split the message into chunks and send each chunk to the server
        for i in range(0, len(message), MESSAGE_CHUNK_SIZE):
            self._client_communicator.send(Serializer.serialize_sending_message(message[i: i + MESSAGE_CHUNK_SIZE]))

        # notifies the server that we have sent all the message chunks
        self._client_communicator.send(Serializer.serialize_end_message())

    def _cancel_message_sending(self):
        self._client_communicator.send(Serializer.serialize_cancel_message())

    menu_dict = {SendMessageOptions.SIMPLE_TEXT_MESSAGE: _text_message,
                 SendMessageOptions.EXIT_AND_CANCEL: _cancel_message_sending}
