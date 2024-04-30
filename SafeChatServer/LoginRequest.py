from Deserializer import Deserializer
import IRequestHandler
from MessageCode import MessageCode
from Serializer import Serializer


class LoginRequest(IRequestHandler.IRequestHandler):
    def _login(self, buffer: bytes):
        username, passw = Deserializer.login_deserialize(buffer)
        res = self._login_manager.login(self._socket_reference, username, passw)

        response_buffer = Serializer.binary_response(MessageCode.LOGIN, res)
        new_handler = self if not res else IRequestHandler.create_after_login_handler(self._db, self._login_manager,
                                                                                      self._socket_reference, username)

        return new_handler, response_buffer

    def _sign_up(self, buffer: bytes):
        username, passw, email = Deserializer.signup_deserialize(buffer)

        res = self._login_manager.sign_up(self._socket_reference, username, passw, email)
        response_buffer = Serializer.binary_response(MessageCode.SIGN_UP, res)
        new_handler = self if not res else IRequestHandler.create_after_login_handler(self._db, self._login_manager,
                                                                                      self._socket_reference, username)

        return new_handler, response_buffer

    handle_dictionary = {MessageCode.LOGIN: _login,
                         MessageCode.SIGN_UP: _sign_up}
