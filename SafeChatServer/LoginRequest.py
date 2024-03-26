import Deserializer
import IRequestHandler
import MessageCode


class LoginRequest(IRequestHandler.IRequestHandler):
    def _login(self, buffer):
        req = Deserializer.Deserializer.deserialize(buffer)
        user, passw = req["username"], req["password"]

        # database check...

        # return result
        return

    def _sign_up(self, buffer):
        req = Deserializer.Deserializer.deserialize(buffer)
        user, passw, email = req["username"], req["password"], req["email"]

        # database check...

        # return result
        return

    handle_dictionary = {MessageCode.MessageCode.LOGIN: _login,
                         MessageCode.MessageCode.SIGN_UP: _sign_up}
