import MessageCode
from Deserializer import SIZE_FIELD_BYTES_SIZE


class Serializer:
    @staticmethod
    def binary_response(mess_code: MessageCode.MessageCode, res: bool) -> bytes:
        return mess_code.to_bytes() + res.to_bytes()

    @staticmethod
    def serialize_login_response(res: bool, username: str):
        return (Serializer.binary_response(MessageCode.MessageCode.LOGIN, res) +
                Serializer._create_string_field(username))

    @staticmethod
    def serialize_sign_up_response(res: bool, username: str):
        return (Serializer.binary_response(MessageCode.MessageCode.SIGN_UP, res) +
                Serializer._create_string_field(username))

    @staticmethod
    def serialize_new_message_notify(from_user: str, date: str) -> bytes:
        return (MessageCode.MessageCode.NEW_MESSAGE_RECEIVED.to_bytes() +
                Serializer._all_params_to_string_fields(locals()))

    @staticmethod
    def serialize_chunk_message_sending(message_chunk: bytes):
        return MessageCode.MessageCode.MESSAGE_SENDING.to_bytes() + message_chunk

    @staticmethod
    def serialize_new_message_end():
        return MessageCode.MessageCode.NEW_MESSAGE_END.to_bytes()

    @staticmethod
    def _create_string_field(field: str):
        return len(field).to_bytes(SIZE_FIELD_BYTES_SIZE) + field.encode()

    @staticmethod
    def _all_params_to_string_fields(locals_dict: dict):
        buffer = b''
        for k, v in locals_dict.items():
            buffer += Serializer._create_string_field(v)

        return buffer

