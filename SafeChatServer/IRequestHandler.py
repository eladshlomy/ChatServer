import DataBaseManager
from LoginManager import LoginManager
import ServerError
from MessageCode import MessageCode
from HandlerFactory import HandlerFactory
from abc import ABC


class IRequestHandler(ABC):  # define as abstract class
    handlers_factory = HandlerFactory()

    def __init__(self, database_manager: DataBaseManager.DataBaseManager, login_manager: LoginManager):
        self._db = database_manager
        self._login_manager = login_manager

    def is_logged_in(self):
        from AfterLoginRequestHandler import AfterLoginRequestHandler
        return isinstance(self, AfterLoginRequestHandler)

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
