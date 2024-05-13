from Deserializer import Deserializer
from IRequestHandler import IRequestHandler
from MessageCode import MessageCode
from Serializer import Serializer


class LoginRequestHandler(IRequestHandler):
    def _login(self, buffer: bytes):
        username, passw = Deserializer.login_deserialize(buffer)
        res = self._login_manager.login(username, passw)

        response_buffer = Serializer.serialize_login_response(res, username)
        new_handler = self if not res else self.handlers_factory.create_after_login_handler(self._db,
                                                                                            self._login_manager,
                                                                                            username)

        return new_handler, response_buffer

    def _sign_up(self, buffer: bytes):
        username, passw, email = Deserializer.signup_deserialize(buffer)

        res = self._login_manager.sign_up(username, passw, email)
        response_buffer = Serializer.serialize_sign_up_response(res, username)
        new_handler = self if not res else self.handlers_factory.create_after_login_handler(self._db,
                                                                                            self._login_manager,
                                                                                            username)

        return new_handler, response_buffer

    handle_dictionary = {MessageCode.LOGIN: _login,
                         MessageCode.SIGN_UP: _sign_up}
