from Serializer import Serializer
from MessageCode import MessageCode
from DataBaseManager import DataBaseManager
from AfterLoginRequest import AfterLoginRequest
from IRequestHandler import create_after_login_handler
from LoginManager import LoginManager


class SendingMessageHandler(AfterLoginRequest):
    def __init__(self, database_manager: DataBaseManager, login_manager: LoginManager, socket_reference, from_user: str,
                 send_to: str):
        super().__init__(database_manager, login_manager, socket_reference, from_user)
        self._send_to = send_to
        self._message = b""

    def _cancel_message(self, buffer: bytes):
        return (create_after_login_handler(self._db, self._login_manager, self._socket_reference, self._username),
                Serializer.binary_response(MessageCode.CANCEL_MESSAGE, True))

    def _end_message_and_commit(self, buffer: bytes):
        self._db.add_message(self._username, self._send_to, self._message)  # add the message to the database

        print(self._username, "send to", self._send_to, ":", self._message)

        return (create_after_login_handler(self._db, self._login_manager, self._socket_reference, self._username),
                Serializer.binary_response(MessageCode.END_MESSAGE, True))

    def _message_sending(self, buffer: bytes):
        self._message += buffer
        return self, b""

    handle_dictionary = {MessageCode.SIGN_OUT: AfterLoginRequest._sign_out,
                         MessageCode.GET_UPDATE: AfterLoginRequest._get_messages_update,
                         MessageCode.CANCEL_MESSAGE: _cancel_message,
                         MessageCode.MESSAGE_SENDING: _message_sending,
                         MessageCode.END_MESSAGE: _end_message_and_commit}
