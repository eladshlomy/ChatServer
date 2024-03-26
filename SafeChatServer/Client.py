import socket
import LoginRequest
import MessageCode
import ServerError

"""
message protocol:
     4 bytes     |     1 BYTE     |
   MESSAGE_SIZE  |  MESSAGE_CODE  |     DATA    |
"""

MESSAGE_SIZE_FIELD_SIZE = 4  # MESSAGE_SIZE field size (4 bytes)


class Client:
    def __init__(self, client_sock: socket.socket):
        self._socket = client_sock
        self._handler = LoginRequest.LoginRequest()

    def handle(self):
        try:
            while True:
                try:
                    buffer = self._receive_request()
                    new_handler, response_buff = self._handler.handle(buffer)

                    self._handler = new_handler
                    self._send_response(response_buff)

                except ServerError.ServerError as error:
                    # send the error message to the client
                    self._send_response(
                        MessageCode.MessageCode.SERVER_ERROR.to_bytes(MessageCode.MESSAGE_CODE_FIELD_SIZE) +
                        str(error).encode())

        except socket.error as e:
            print(e)

    def _receive_request(self) -> bytes:
        data = self._socket.recv(MESSAGE_SIZE_FIELD_SIZE)
        if not data:  # in case that the client disconnect the bytes will be empty
            raise socket.error("Client disconnected")

        size = int.from_bytes(data)
        request = self._socket.recv(size)  # receive the whole request
        return request

    def _send_response(self, buffer: bytes):
        size = len(buffer).to_bytes(MESSAGE_SIZE_FIELD_SIZE)
        self._socket.send(size + buffer)
