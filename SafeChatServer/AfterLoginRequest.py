from DataBaseManager import DataBaseManager
from Deserializer import Deserializer
import IRequestHandler
from LoginManager import LoginManager
from MessageCode import MessageCode
from Serializer import Serializer


class AfterLoginRequest(IRequestHandler.IRequestHandler):
    def __init__(self, database_manager: DataBaseManager, login_manager: LoginManager, socket_reference,
                 username):
        super().__init__(database_manager, login_manager, socket_reference)
        self._username = username

    def _sign_out(self, buffer: bytes):

        return (IRequestHandler.create_login_handler(self._db, self._login_manager, self._socket_reference),
                Serializer.binary_response(MessageCode.SIGN_OUT, self._login_manager.log_out(self._username)))

    def _send_message_req(self, buffer: bytes):
        to_user = Deserializer.send_message_req_deserialize(buffer)

        res = self._db.user_exist(to_user)

        return (IRequestHandler.create_sending_message_handler(self._db, self._login_manager, self._socket_reference,
                                                               self._username, to_user) if res else self,
                Serializer.binary_response(MessageCode.SEND_MESSAGE_REQ, res))

    def _get_messages_update(self, buffer):
        pass

    handle_dictionary = {MessageCode.SIGN_OUT: _sign_out,
                         MessageCode.GET_UPDATE: _get_messages_update,
                         MessageCode.SEND_MESSAGE_REQ: _send_message_req}

