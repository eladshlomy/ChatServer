import socket
import Client
import threading

PORT = 8282


class ChatServer:
    def __init__(self, port=PORT):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # define TCP server socket
        self._sock.bind(('', port))  # bind the server to the listening socket

    def serve(self):
        self._sock.listen()  # start listening

        print("The server up and running.")

        while True:
            client_socket, client_address = self._sock.accept()
            print("A client accepted")

            client = Client.Client(client_socket)

            client_thread = threading.Thread(target=client.handle)
            client_thread.daemon = True
            client_thread.start()


if __name__ == '__main__':
    server = ChatServer()
    server.serve()
