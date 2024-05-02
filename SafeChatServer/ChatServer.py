from IRequestHandler import IRequestHandler
import LoginManager
from MessageCode import MessageCode
import DataBaseManager
from ServerError import ServerError
from Communicator import Communicator
from socket import error

PORT = 8282
MESSAGE_SIZE_FIELD_SIZE = 4  # MESSAGE_SIZE field size (4 bytes)


class ChatServer:
    def __init__(self, port=PORT):
        self._database = DataBaseManager.DataBaseManager()
        self._login_manager = LoginManager.LoginManager(self._database)
        self._communicator = Communicator("", port)
        self._client_generator = self._communicator.client_generator()
        self._clients = {}

    def serve(self):
        for client, new_client in self._client_generator:
            if new_client:
                self._clients[client] = \
                    IRequestHandler.handlers_factory.create_login_handler(self._database,
                                                                          self._login_manager,
                                                                          client)
            else:
                try:
                    buffer = self._communicator.receive_request(client)
                    new_handler, response_buff = self._clients[client].handle(buffer)

                    self._clients[client] = new_handler
                    self._communicator.send_response(client, response_buff)

                except ServerError as e:
                    # send the error message to the client
                    self._communicator.send_response(client, MessageCode.SERVER_ERROR.to_bytes() +
                                                     str(e).encode())
                except error as e:  # client disconnected
                    print(e, client)
                    self._login_manager.log_out_by_socket(client)  # log out the user (if he was logged in)
                    del self._clients[client]  # delete the client state
                    self._communicator.disconnect_client(client)  # remove the client from the clients list
