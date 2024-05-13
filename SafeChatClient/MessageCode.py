from enum import Enum

MESSAGE_CODE_FIELD_SIZE = 1


class MessageCode(Enum):
    LOGIN = 200
    SIGN_UP = 100
    SIGN_OUT = 150
    SERVER_ERROR = 50

    # client sending new messages
    NEW_MESSAGE_RECEIVED = 40
    # MESSAGE_SENDING = 15  -> can use the same code for sending the message back to the client
    NEW_MESSAGE_END = 60

    # message sending processes codes
    SEND_MESSAGE_REQ = 10
    MESSAGE_SENDING = 15
    END_MESSAGE = 20
    CANCEL_MESSAGE = 30

    def to_bytes(self):
        return self.value.to_bytes(MESSAGE_CODE_FIELD_SIZE)
