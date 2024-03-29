import MessageCode


class Serializer:
    @staticmethod
    def binary_response(mess_code: MessageCode.MessageCode, res: bool) -> bytes:
        return mess_code.value.to_bytes(MessageCode.MESSAGE_CODE_FIELD_SIZE) + res.to_bytes()
