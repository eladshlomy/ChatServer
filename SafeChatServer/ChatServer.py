from IRequestHandler import IRequestHandler
import LoginManager
from MessageCode import MessageCode
import DataBaseManager
from ServerError import ServerError
from Communicator import Communicator
from MessageNotifier import MessageNotifier
from socket import error
from threading import Thread

PORT = 8282
MESSAGE_SIZE_FIELD_SIZE = 4  # MESSAGE_SIZE field size (4 bytes)


class ChatServer:
    def __init__(self, port=PORT):
        self._database = DataBaseManager.DataBaseManager()
        self._communicator = Communicator("", port)
        self._client_generator = self._communicator.client_generator()
        self._clients = {}
        self._message_notifier = MessageNotifier(self._clients, self._communicator)
        self._login_manager = LoginManager.LoginManager(self._database, self._message_notifier)

        # create a notifier daemon-thread
        t = Thread(target=self._message_notifier.notifier_loop)
        t.daemon = True
        t.start()

    def serve(self):
        for client, new_client in self._client_generator:
            if new_client:
                self._handle_new_client(client)
            else:
                self._handle_client_request(client)

    def _handle_new_client(self, client):
        self._clients[client] = \
            IRequestHandler.handlers_factory.create_login_handler(self._database,
                                                                  self._login_manager)

    def _handle_client_request(self, client):
        try:
            buffer = self._communicator.receive_request(client)
            new_handler, response_buff = self._clients[client].handle(buffer)

            self._clients[client] = new_handler
            self._communicator.send(client, response_buff)

        except ServerError as e:
            # send the error message to the client
            self._communicator.send(client, MessageCode.SERVER_ERROR.to_bytes() +
                                    str(e).encode())
        except error as e:  # client disconnected
            print(e, client)

            # log out the client (if he was logged)
            if self._clients[client].is_logged_in():
                self._login_manager.log_out(self._clients[client].get_username())

            del self._clients[client]  # delete the client state
            self._communicator.disconnect_client(client)  # remove the client from the clients list
