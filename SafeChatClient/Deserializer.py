import MessageCode


class Deserializer:
    @staticmethod
    def deserialize_binary_response(buffer: bytes):
        return bool.from_bytes(buffer)

    @staticmethod
    def deserialize_update(buffer: bytes):
        pass
