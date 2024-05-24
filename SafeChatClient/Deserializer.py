from Serializer import SIZE_FIELD_BYTES_SIZE


class Deserializer:
    @staticmethod
    def deserialize_binary_response(buffer: bytes) -> bool:
        return bool(buffer[0])

    @staticmethod
    def deserialize_login_and_signup(buffer: bytes) -> tuple[bool, str]:
        res, username = Deserializer.deserialize_binary_response(buffer), buffer[1:].decode()
        return res, username

    @staticmethod
    def deserialize_new_message_notification(buffer: bytes) -> tuple[str, str]:
        source_username, date = Deserializer._collect_all_fields(buffer)
        return source_username.decode(), date.decode()

    @staticmethod
    def deserialize_send_message_response(buffer: bytes) -> tuple[bool, bytes]:
        return Deserializer.deserialize_binary_response(buffer), buffer[1:]

    @staticmethod
    def _collect_field(buffer: bytes) -> tuple[bytes, bytes]:
        size = int.from_bytes(buffer[:SIZE_FIELD_BYTES_SIZE])
        field = buffer[SIZE_FIELD_BYTES_SIZE: SIZE_FIELD_BYTES_SIZE + size]
        buffer = buffer[SIZE_FIELD_BYTES_SIZE + size:]
        return field, buffer

    @staticmethod
    def _collect_all_fields(buffer: bytes) -> list[bytes]:
        fields = []

        while buffer:
            field, buffer = Deserializer._collect_field(buffer)
            fields.append(field)

        return fields
