import Serializer
from MessageCode import MessageCode
from DataBaseManager import DataBaseManager
import IRequestHandler


class SendingMessageHandler(IRequestHandler.IRequestHandler):
    def __init__(self, database_manager: DataBaseManager, from_user: str, send_to: str):
        super().__init__(database_manager)
        self._send_to = send_to
        self._from_user = from_user
        self._message = b""

    def _cancel_message(self, buffer: bytes):
        return (IRequestHandler.create_after_login_handler(self._db, self._from_user),
                Serializer.Serializer.binary_response(MessageCode.CANCEL_MESSAGE, True))

    def _end_message_and_commit(self, buffer: bytes):
        from_id = self._db.get_user_id(self._from_user)
        to_id = self._db.get_user_id(self._send_to)

        self._db.add_message(from_id, to_id, self._message)

        print(self._from_user, "send to", self._send_to, ":", self._message)

        return (IRequestHandler.create_after_login_handler(self._db, self._from_user),
                Serializer.Serializer.binary_response(MessageCode.END_MESSAGE, True))

    def _message_sending(self, buffer: bytes):
        self._message += buffer
        return self, b""

    handle_dictionary = {MessageCode.CANCEL_MESSAGE: _cancel_message,
                         MessageCode.MESSAGE_SENDING: _message_sending,
                         MessageCode.END_MESSAGE: _end_message_and_commit}
