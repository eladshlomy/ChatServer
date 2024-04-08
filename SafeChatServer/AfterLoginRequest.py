import DataBaseManager
import IRequestHandler
import MessageCode
import Serializer


class AfterLoginRequest(IRequestHandler.IRequestHandler):
    def __init__(self, database_manager: DataBaseManager.DataBaseManager, username):
        super().__init__(database_manager)
        self._username = username

    def _sign_out(self, buffer: bytes):
        print("Client sign out!")
        return (IRequestHandler.create_login_handler(self._db),
                Serializer.Serializer.binary_response(MessageCode.MessageCode.SIGN_OUT, True))

    handle_dictionary = {MessageCode.MessageCode.SIGN_OUT: _sign_out, }

