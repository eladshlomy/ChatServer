from MessageCode import MessageCode

SIZE_FIELD_BYTES_SIZE = 2


class Serializer:
    @staticmethod
    def serialize_signup(username: str, password: str, email: str, public_key: bytes):
        username, password, email = username.encode(), password.encode(), email.encode()
        return MessageCode.SIGN_UP.to_bytes() + Serializer._create_fields(locals())

    @staticmethod
    def serialize_login(username: str, password: str, public_key: bytes):
        username, password = username.encode(), password.encode()
        return MessageCode.LOGIN.to_bytes() + Serializer._create_fields(locals())

    @staticmethod
    def serialize_logout():
        return MessageCode.SIGN_OUT.to_bytes()

    @staticmethod
    def serialize_send_message_req(to: str, public_key_request: bool):
        to, public_key_request = to.encode(), public_key_request.to_bytes()
        return MessageCode.SEND_MESSAGE_REQ.to_bytes() + Serializer._create_fields(locals())

    @staticmethod
    def serialize_sending_message(message_chunk: bytes):
        return MessageCode.MESSAGE_SENDING.to_bytes() + message_chunk

    @staticmethod
    def serialize_end_message():
        return MessageCode.END_MESSAGE.to_bytes()

    @staticmethod
    def serialize_cancel_message():
        return MessageCode.CANCEL_MESSAGE.to_bytes()

    @staticmethod
    def _create_field(field: bytes):
        return len(field).to_bytes(SIZE_FIELD_BYTES_SIZE) + field

    @staticmethod
    def _create_fields(locals_dict: dict):
        buffer = b''
        for k, v in locals_dict.items():
            buffer += Serializer._create_field(v)

        return buffer
