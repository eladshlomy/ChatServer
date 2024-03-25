import socket


class Client:
    def __init__(self, client_sock: socket.socket):
        self._socket = client_sock

    def handle(self):
        pass
