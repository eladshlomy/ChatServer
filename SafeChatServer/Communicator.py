import socket
from select import select

MESSAGE_SIZE_FIELD_SIZE = 4  # MESSAGE_SIZE field size (4 bytes)


class Communicator:
    def __init__(self, address, port):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # define TCP server socket
        self._clients_sockets = []
        self._sock.bind((address, port))  # bind the server to the listening socket

    def client_generator(self):
        """
        generator function that return readable client that approach to the server
        :return: client socket, if it is a new client or a client that already was connected
        """
        self._sock.listen()
        print("The server up and running.")

        while True:
            readable_sockets, _, _ = select([self._sock] + self._clients_sockets, [], [])

            for sock in readable_sockets:
                if sock is self._sock:
                    client_socket, client_address = sock.accept()
                    self._clients_sockets.append(client_socket)
                    print("A client accepted from", client_address)

                    yield client_socket, True
                else:
                    yield sock, False

    def disconnect_client(self, client: socket.socket):
        try:
            client.close()
        except socket.error:
            pass
        self._clients_sockets.remove(client)

    @staticmethod
    def receive_request(client_socket) -> bytes:
        data = client_socket.recv(MESSAGE_SIZE_FIELD_SIZE)
        if not data:  # in case that the client disconnect the bytes will be empty
            raise socket.error("Client disconnected")

        size = int.from_bytes(data)
        request = client_socket.recv(size)  # receive the whole request
        return request

    @staticmethod
    def send_response(client_socket, buffer: bytes):
        if buffer:
            size = len(buffer).to_bytes(MESSAGE_SIZE_FIELD_SIZE)
            client_socket.send(size + buffer)
