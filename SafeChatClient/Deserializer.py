import MessageCode
from Serializer import SIZE_FIELD_BYTES_SIZE


class Deserializer:
    @staticmethod
    def deserialize_binary_response(buffer: bytes):
        return bool(buffer[0])

    @staticmethod
    def deserialize_login_and_signup(buffer: bytes):
        res, (username, buffer) = (Deserializer.deserialize_binary_response(buffer),
                                   Deserializer._collect_field(buffer[1:]))
        return res, username

    @staticmethod
    def deserialize_new_message_notification(buffer: bytes):
        return Deserializer._collect_all_fields(buffer)

    @staticmethod
    def _collect_field(buffer: bytes):
        size = int.from_bytes(buffer[:SIZE_FIELD_BYTES_SIZE])
        field = buffer[SIZE_FIELD_BYTES_SIZE: SIZE_FIELD_BYTES_SIZE + size].decode()
        buffer = buffer[SIZE_FIELD_BYTES_SIZE + size:]
        return field, buffer

    @staticmethod
    def _collect_all_fields(buffer: bytes) -> list:
        fields = []

        while buffer:
            field, buffer = Deserializer._collect_field(buffer)
            fields.append(field)

        return fields
