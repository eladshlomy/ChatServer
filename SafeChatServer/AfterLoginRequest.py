import DataBaseManager
import IRequestHandler
import MessageCode
import Serializer


class AfterLoginRequest(IRequestHandler.IRequestHandler):
    def __init__(self, database_manager: DataBaseManager.DataBaseManager, username):
        super().__init__(database_manager)
        self._username = username

    def _sign_out(self, buffer):
        return (IRequestHandler.create_login_handler(self._db),
                Serializer.Serializer.binary_response(MessageCode.MessageCode.LOG_OUT, True))


