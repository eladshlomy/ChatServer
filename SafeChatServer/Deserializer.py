SIZE_FIELD_BYTES_SIZE = 2


class Deserializer:
    @staticmethod
    def login_deserialize(buffer: bytes):
        """
            :return: username, password
        """
        username, password = Deserializer._collect_all_fields(buffer)
        return username, password

    @staticmethod
    def signup_deserialize(buffer: bytes):
        """
        :return: username, password, email
        """
        username, password, email = Deserializer._collect_all_fields(buffer)
        return username, password, email

    @staticmethod
    def send_message_req_deserialize(buffer: bytes):
        to_user, buffer = Deserializer._collect_field(buffer)  # collect the receiving username
        return to_user

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
