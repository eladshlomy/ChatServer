import DataBaseManager
from Deserializer import Deserializer
import IRequestHandler
from MessageCode import MessageCode
import Serializer


class AfterLoginRequest(IRequestHandler.IRequestHandler):
    def __init__(self, database_manager: DataBaseManager.DataBaseManager, username):
        super().__init__(database_manager)
        self._username = username

    def _sign_out(self, buffer: bytes):
        print("Client sign out!")
        return (IRequestHandler.create_login_handler(self._db),
                Serializer.Serializer.binary_response(MessageCode.SIGN_OUT, True))

    def _send_message_req(self, buffer: bytes):
        to_user = Deserializer.send_message_req_deserialize(buffer)

        res = self._db.user_exist(to_user)

        return (IRequestHandler.create_sending_message_handler(self._db, self._username, to_user) if res else self,
                Serializer.Serializer.binary_response(MessageCode.SEND_MESSAGE_REQ, res))

    handle_dictionary = {MessageCode.SIGN_OUT: _sign_out,
                         MessageCode.SEND_MESSAGE_REQ: _send_message_req}

