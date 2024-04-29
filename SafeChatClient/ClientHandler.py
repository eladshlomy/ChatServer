from MessageCode import MessageCode
from ClientCommunicator import ClientCommunicator
from Deserializer import Deserializer
from time import sleep

# menus
from AfterLoginMenu import AfterLoginMenu
from LoginMenu import LoginMenu
from ClientMenu import ClientMenu
from SendMessageMenu import SendMessageMenu


class ClientHandler:
    def __init__(self, client_communicator: ClientCommunicator, menu: ClientMenu):
        self._client_communicator = client_communicator
        self._menu = menu

    def receive_loop(self):
        while True:
            code, buffer = self._client_communicator.receive()
            if code in self.switch_dict.keys():
                ClientHandler.switch_dict[code](self, buffer)
            else:
                print("invalid code received. ", code.name, code.value)

    def menu_loop(self):
        while True:
            sleep(0.1)
            self._menu.get_user_choice()

    def _login(self, buffer: bytes):
        if Deserializer.deserialize_binary_response(buffer):
            print("\nLog in successfully!")
            self._menu = AfterLoginMenu(self._client_communicator)

        else:
            print("\nLog in went wrong")

    def _sign_up(self, buffer: bytes):
        if Deserializer.deserialize_binary_response(buffer):
            print("\nSign up successfully!")
            self._menu = AfterLoginMenu(self._client_communicator)
        else:
            print("\nSign up went wrong")

    def _log_out(self, buffer: bytes):
        if Deserializer.deserialize_binary_response(buffer):
            print("\nSign out successfully!")
            self._menu = LoginMenu(self._client_communicator)

    def _send_message_req(self, buffer: bytes):
        if Deserializer.deserialize_binary_response(buffer):
            self._menu = SendMessageMenu(self._client_communicator)
        else:
            print("\nInvalid send message request - (invalid destination)")

    def _message_ending(self, buffer: bytes):
        if Deserializer.deserialize_binary_response(buffer):
            self._menu = AfterLoginMenu(self._client_communicator)
            print("\nMessage were send successfully!")
        else:
            print("\nSomething went wrong while sending the message")

    def _message_canceling(self, buffer: bytes):
        if Deserializer.deserialize_binary_response(buffer):
            self._menu = AfterLoginMenu(self._client_communicator)
            print("\nMessage sending canceled successfully!")
        else:
            print("\nSomething went wrong while canceling the message")

    def _server_error(self, buffer: bytes):
        print(MessageCode.SERVER_ERROR.name, ": ", buffer.decode())

    switch_dict = {MessageCode.LOGIN: _login,
                   MessageCode.SIGN_OUT: _log_out,
                   MessageCode.SEND_MESSAGE_REQ: _send_message_req,
                   MessageCode.END_MESSAGE: _message_ending,
                   MessageCode.CANCEL_MESSAGE: _message_canceling,
                   MessageCode.SIGN_UP: _sign_up,
                   MessageCode.SERVER_ERROR: _server_error}
