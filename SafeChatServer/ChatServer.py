import socket
from IRequestHandler import IRequestHandler
from select import select

import LoginManager
from MessageCode import MessageCode
import DataBaseManager
from ServerError import ServerError

PORT = 8282
MESSAGE_SIZE_FIELD_SIZE = 4  # MESSAGE_SIZE field size (4 bytes)


class ChatServer:
    def __init__(self, port=PORT):
        self._database = DataBaseManager.DataBaseManager()
        self._login_manager = LoginManager.LoginManager(self._database)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # define TCP server socket
        self._clients = {}
        self._sock.bind(('', port))  # bind the server to the listening socket

    def serve(self):
        self._sock.listen()  # start listening

        print("The server up and running.")

        while True:
            readable_sockets, _, _ = select([self._sock] + list(self._clients.keys()), [], [])

            for sock in readable_sockets:
                # if it is a new client that try to connect
                if sock is self._sock:
                    client_socket, client_address = sock.accept()
                    print("A client accepted from", client_address)

                    # add the client to the clients dictionary with login handler
                    self._clients[client_socket] = \
                        IRequestHandler.handlers_factory.create_login_handler(self._database,
                                                                              self._login_manager,
                                                                              client_socket)
                else:
                    try:
                        buffer = self.receive_request(sock)
                        new_handler, response_buff = self._clients[sock].handle(buffer)

                        self._clients[sock] = new_handler
                        self.send_response(sock, response_buff)

                    except ServerError as error:
                        # send the error message to the client
                        self.send_response(sock, MessageCode.SERVER_ERROR.to_bytes() +
                                           str(error).encode())
                    except socket.error as e:
                        print(e, sock)
                        self._login_manager.log_out_by_socket(sock)
                        del self._clients[sock]

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
