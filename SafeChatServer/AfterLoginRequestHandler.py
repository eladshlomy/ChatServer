from DataBaseManager import DataBaseManager
from Deserializer import Deserializer
from IRequestHandler import IRequestHandler
from LoginManager import LoginManager
from MessageCode import MessageCode
from Serializer import Serializer


class AfterLoginRequestHandler(IRequestHandler):
    def __init__(self, database_manager: DataBaseManager, login_manager: LoginManager, username):
        super().__init__(database_manager, login_manager)
        self._username = username

    def get_username(self):
        return self._username

    def _sign_out(self, buffer: bytes):
        return (self.handlers_factory.create_login_handler(self._db, self._login_manager),
                Serializer.binary_response(MessageCode.SIGN_OUT, self._login_manager.log_out(self._username)))

    def _send_message_req(self, buffer: bytes):
        print(buffer)
        to_user, public_key_req = Deserializer.send_message_req_deserialize(buffer)
        print(to_user, public_key_req)

        exist_and_valid = self._db.user_exist(to_user) and to_user != self._username

        if public_key_req and exist_and_valid:
            response = Serializer.serialize_send_message_response(exist_and_valid, self._db.get_public_key(to_user))
        else:
            response = Serializer.binary_response(MessageCode.SEND_MESSAGE_REQ, exist_and_valid)

        return (self.handlers_factory.create_sending_message_handler(self._db, self._login_manager, self._username,
                                                                     to_user) if exist_and_valid else self, response)

    handle_dictionary = {MessageCode.SIGN_OUT: _sign_out,
                         MessageCode.SEND_MESSAGE_REQ: _send_message_req}
