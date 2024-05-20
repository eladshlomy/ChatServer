import socket
import MessageCode
from threading import Lock

SERVER_PORT = 8282
MESSAGE_SIZE_FIELD_SIZE = 4


class ClientCommunicator:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect(('127.0.0.1', SERVER_PORT))
        self._socket_lock = Lock()

    def send(self, buffer: bytes):
        buffer = len(buffer).to_bytes(MESSAGE_SIZE_FIELD_SIZE) + buffer
        self._sock.send(buffer)

    def receive(self) -> tuple[MessageCode.MessageCode, bytes]:
        size = int.from_bytes(self._sock.recv(MESSAGE_SIZE_FIELD_SIZE))
        buffer = self._sock.recv(size)

        return (MessageCode.MessageCode(int.from_bytes(buffer[:MessageCode.MESSAGE_CODE_FIELD_SIZE])),
                buffer[MessageCode.MESSAGE_CODE_FIELD_SIZE:])
