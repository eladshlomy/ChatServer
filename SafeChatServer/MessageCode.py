import enum

MESSAGE_CODE_FIELD_SIZE = 1


class MessageCode(enum):
    LOGIN = 200
    SIGN_UP = 100
    LOG_OUT = 150
    SERVER_ERROR = 50
