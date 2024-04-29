from Deserializer import Deserializer
import IRequestHandler
from MessageCode import MessageCode
from hashlib import md5
from Serializer import Serializer


class LoginRequest(IRequestHandler.IRequestHandler):
    def _login(self, buffer: bytes):
        username, passw = Deserializer.login_deserialize(buffer)
        hash_passw = md5(passw.encode()).digest()  # hash the password

        user_data = self._db.find_user(username)
        res = user_data is not None

        if res:
            u, real_hashed_password, email = user_data
            res = real_hashed_password == hash_passw
            if not res:
                print("wrong password")
        else:
            print("No such user")

        response_buffer = Serializer.binary_response(MessageCode.LOGIN, res)
        new_handler = self if not res else IRequestHandler.create_after_login_handler(self._db, username)

        if res:
            print("Client logged in!")

        return new_handler, response_buffer

    def _sign_up(self, buffer: bytes):
        username, passw, email = Deserializer.signup_deserialize(buffer)
        passw = md5(passw.encode())  # hash the password

        res = self._db.add_user(username, passw.digest(), email)  # add the user into the database
        response_buffer = Serializer.binary_response(MessageCode.SIGN_UP, res)
        new_handler = self if not res else IRequestHandler.create_after_login_handler(self._db, username)

        if res:
            print("Client sign up!")

        return new_handler, response_buffer

    handle_dictionary = {MessageCode.LOGIN: _login,
                         MessageCode.SIGN_UP: _sign_up}
