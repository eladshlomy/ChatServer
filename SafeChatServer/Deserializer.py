import json


class Deserializer:
    @staticmethod
    def deserialize(buffer: bytes):
        return json.loads(buffer)
