import DataBaseManager
from LoginManager import LoginManager
import ServerError
from MessageCode import MessageCode


class IRequestHandler:
    def __init__(self, database_manager: DataBaseManager.DataBaseManager, login_manager: LoginManager, socket_reference):
        self._db = database_manager
        self._socket_reference = socket_reference
        self._login_manager = login_manager

    @staticmethod
    def _split_code_and_data(buffer: bytes) -> type[MessageCode, bytes]:
        return MessageCode(buffer[0]), buffer[1:]

    def _is_relevant(self, message_code: MessageCode) -> bool:
        return message_code in self.handle_dictionary

    def handle(self, request_buffer: bytes):  # -> tuple[IRequestHandler, bytes]
        code, data = IRequestHandler._split_code_and_data(request_buffer)
        if not self._is_relevant(code):
            raise ServerError.ServerError("Request not relevant")
        return self.handle_dictionary[code](self, data)

    handle_dictionary = {}


# to avoid circular import
def create_login_handler(database: DataBaseManager.DataBaseManager, login_manager, socket_reference):
    from LoginRequest import LoginRequest
    return LoginRequest(database, login_manager, socket_reference)


def create_after_login_handler(database: DataBaseManager.DataBaseManager, login_manager, socket_reference, username):
    from AfterLoginRequest import AfterLoginRequest
    return AfterLoginRequest(database, login_manager, socket_reference, username)


def create_sending_message_handler(database: DataBaseManager.DataBaseManager, login_manager, socket_reference,
                                   from_user: str, to_user: str):
    from SendingMessageHandler import SendingMessageHandler
    return SendingMessageHandler(database, login_manager, socket_reference, from_user, to_user)
