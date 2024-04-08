from MessageCode import MessageCode

SIZE_FIELD_BYTES_SIZE = 2


class Serializer:
    @staticmethod
    def serialize_signup(username: str, password: str, email: str):
        return MessageCode.SIGN_UP.to_bytes() + Serializer._all_params_to_string_fields(locals())

    @staticmethod
    def serialize_login(username: str, password: str):
        return MessageCode.LOGIN.to_bytes() + Serializer._all_params_to_string_fields(locals())

    @staticmethod
    def serialize_logout():
        return MessageCode.SIGN_OUT.to_bytes()

    @staticmethod
    def serialize_send_message(to: str, message: str):
        pass

    @staticmethod
    def serialize_get_update(from_date):
        pass

    @staticmethod
    def _create_string_field(field: str):
        return len(field).to_bytes(SIZE_FIELD_BYTES_SIZE) + field.encode()

    @staticmethod
    def _all_params_to_string_fields(locals_dict: dict):
        buffer = b''
        for k, v in locals_dict.items():
            buffer += Serializer._create_string_field(v)

        return buffer
