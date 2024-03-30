import Deserializer
import IRequestHandler
import MessageCode
from hashlib import md5
import Serializer


class LoginRequest(IRequestHandler.IRequestHandler):
    def _login(self, buffer: bytes):
        username, passw = Deserializer.Deserializer.login_deserialize(buffer)
        hash_passw = md5(passw)  # hash the password

        u, real_hashed_password, email = self._db.find_user(username)
        res = real_hashed_password == hash_passw
        response_buffer = Serializer.Serializer.binary_response(MessageCode.MessageCode.LOGIN, res)
        new_handler = self if not res else IRequestHandler.create_after_login_handler(self._db, username)

        return new_handler, response_buffer

    def _sign_up(self, buffer: bytes):
        username, passw, email = Deserializer.Deserializer.signup_deserialize(buffer)
        passw = md5(passw)  # hash the password

        res = self._db.add_user(username, passw.digest(), email)  # add the user into the database
        response_buffer = Serializer.Serializer.binary_response(MessageCode.MessageCode.LOGIN, res)
        new_handler = self if not res else IRequestHandler.create_after_login_handler(self._db, username)

        return new_handler, response_buffer

    handle_dictionary = {MessageCode.MessageCode.LOGIN: _login,
                         MessageCode.MessageCode.SIGN_UP: _sign_up}
