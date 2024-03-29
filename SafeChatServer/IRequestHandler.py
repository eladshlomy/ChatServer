import DataBaseManager
import ServerError
from MessageCode import MessageCode


class IRequestHandler:
    def __init__(self, database_manager: DataBaseManager.DataBaseManager):
        self._db = database_manager

    @staticmethod
    def _split_code_and_data(buffer: bytes) -> type[MessageCode, bytes]:
        return MessageCode(buffer[0]), buffer[1:]

    def _is_relevant(self, message_code: MessageCode) -> bool:
        return message_code in self.handle_dictionary

    def handle(self, request_buffer: bytes):  # -> tuple[IRequestHandler, bytes]
        code, data = IRequestHandler._split_code_and_data(request_buffer)
        if not self._is_relevant(code):
            raise ServerError.ServerError("Request not relevant")
        return self.handle_dictionary[code](data)

    handle_dictionary = {}


# to avoid circular import
def create_login_handler(database: DataBaseManager.DataBaseManager):
    from LoginRequest import LoginRequest
    return LoginRequest(database)


def create_after_login_handler(database: DataBaseManager.DataBaseManager, username):
    from AfterLoginRequest import AfterLoginRequest
    return AfterLoginRequest()
