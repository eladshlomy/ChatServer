import MessageCode
from Deserializer import SIZE_FIELD_BYTES_SIZE


class Serializer:
    @staticmethod
    def binary_response(mess_code: MessageCode.MessageCode, res: bool) -> bytes:
        return mess_code.to_bytes() + res.to_bytes()

    @staticmethod
    def new_message_sending(from_user: str) -> bytes:
        return (MessageCode.MessageCode.NEW_MESSAGE_RECEIVED.to_bytes() +
                Serializer._create_string_field(from_user))

    @staticmethod
    def _create_string_field(field: str):
        return len(field).to_bytes(SIZE_FIELD_BYTES_SIZE) + field.encode()
