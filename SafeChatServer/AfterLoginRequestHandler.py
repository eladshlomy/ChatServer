from DataBaseManager import DataBaseManager
from Deserializer import Deserializer
from IRequestHandler import IRequestHandler
from LoginManager import LoginManager
from MessageCode import MessageCode
from Serializer import Serializer


class AfterLoginRequestHandler(IRequestHandler):
    def __init__(self, database_manager: DataBaseManager, login_manager: LoginManager, socket_reference,
                 username):
        super().__init__(database_manager, login_manager, socket_reference)
        self._username = username

    def _sign_out(self, buffer: bytes):

        return (self.handlers_factory.create_login_handler(self._db, self._login_manager, self._socket_reference),
                Serializer.binary_response(MessageCode.SIGN_OUT, self._login_manager.log_out(self._username)))

    def _send_message_req(self, buffer: bytes):
        to_user = Deserializer.send_message_req_deserialize(buffer)

        res = self._db.user_exist(to_user)

        return (self.handlers_factory.create_sending_message_handler(self._db, self._login_manager, self._socket_reference,
                                                               self._username, to_user) if res else self,
                Serializer.binary_response(MessageCode.SEND_MESSAGE_REQ, res))

    handle_dictionary = {MessageCode.SIGN_OUT: _sign_out,
                         MessageCode.SEND_MESSAGE_REQ: _send_message_req}

