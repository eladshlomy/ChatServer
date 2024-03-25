import ServerError
from MessageCode import MessageCode


class IRequestHandler:
    def __init__(self):
        pass

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
