from enum import Enum

MESSAGE_CODE_FIELD_SIZE = 1


class MessageCode(Enum):
    LOGIN = 200
    SIGN_UP = 100
    SIGN_OUT = 150
    SERVER_ERROR = 50

    # GET_USER_PUBLIC_KEY
    GET_UPDATE = 70

    # message sending processes codes
    SEND_MESSAGE_REQ = 10
    MESSAGE_SENDING = 15
    END_MESSAGE = 20
    CANCEL_MESSAGE = 30

    def to_bytes(self):
        return self.value.to_bytes(MESSAGE_CODE_FIELD_SIZE)
