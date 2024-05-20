from Serializer import Serializer
from MessageCode import MessageCode
from DataBaseManager import DataBaseManager
from AfterLoginRequestHandler import AfterLoginRequestHandler
from LoginManager import LoginManager
from datetime import datetime


class SendingMessageHandler(AfterLoginRequestHandler):
    def __init__(self, database_manager: DataBaseManager, login_manager: LoginManager, from_user: str, send_to: str):
        super().__init__(database_manager, login_manager, from_user)
        self._send_to = send_to
        self._message = b""

    def _cancel_message(self, buffer: bytes):
        return (self.handlers_factory.create_after_login_handler(self._db, self._login_manager, self._username),
                Serializer.binary_response(MessageCode.CANCEL_MESSAGE, True))

    def _end_message_and_commit(self, buffer: bytes):
        if self._login_manager.is_online(self._send_to):
            print("The client is online, the message was sent!")
            self._login_manager.message_notifier.notify_a_message(self._username, self._send_to, self._message,
                                                                  datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            print("The client is offline so the message will be save in the database")
            self._db.add_message(self._username, self._send_to, self._message)  # add the message to the database

        print(self._username, "send to", self._send_to, ":", self._message)

        return (self.handlers_factory.create_after_login_handler(self._db, self._login_manager,
                                                                 self._username),
                Serializer.binary_response(MessageCode.END_MESSAGE, True))

    def _message_sending(self, buffer: bytes):
        self._message += buffer
        return self, b""

    handle_dictionary = {MessageCode.SIGN_OUT: AfterLoginRequestHandler._sign_out,
                         MessageCode.CANCEL_MESSAGE: _cancel_message,
                         MessageCode.MESSAGE_SENDING: _message_sending,
                         MessageCode.END_MESSAGE: _end_message_and_commit}
