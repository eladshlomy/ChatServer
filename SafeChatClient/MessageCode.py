from enum import Enum

MESSAGE_CODE_FIELD_SIZE = 1


class MessageCode(Enum):
    LOGIN = 200
    SIGN_UP = 100
    SIGN_OUT = 150
    SERVER_ERROR = 50
    """
    GET_USER_PUBLIC_KEY
    GET_UPDATE
    SEND_MESSAGE
    """

    def to_bytes(self):
        return self.value.to_bytes(MESSAGE_CODE_FIELD_SIZE)
