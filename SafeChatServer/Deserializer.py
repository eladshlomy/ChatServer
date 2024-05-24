SIZE_FIELD_BYTES_SIZE = 2


class Deserializer:
    @staticmethod
    def login_deserialize(buffer: bytes) -> tuple[str, str, bytes]:
        """
            :return: username, password, new_public_key
        """
        username, password, public_key = Deserializer._collect_all_fields(buffer)
        return username.decode(), password.decode(), public_key

    @staticmethod
    def signup_deserialize(buffer: bytes) -> tuple[str, str, str, bytes]:
        """
        :return: username, password, email
        """
        username, password, email, public_key = Deserializer._collect_all_fields(buffer)
        return username.decode(), password.decode(), email.decode(), public_key

    @staticmethod
    def send_message_req_deserialize(buffer: bytes) -> tuple[str, bool]:
        to_user, public_key_request = Deserializer._collect_all_fields(buffer)
        return to_user.decode(), bool.from_bytes(public_key_request)

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
