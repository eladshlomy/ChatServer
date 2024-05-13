from IHandler import *
from Deserializer import Deserializer

# menus
from ClientMenu import ClientMenu
from LoginMenu import LoginMenu
from AfterLoginMenu import AfterLoginMenu
from SendMessageMenu import SendMessageMenu


class ResponseHandler(IHandler):
    def __init__(self, database: DataBaseManager, menu: ClientMenu):
        super().__init__(database)
        self._menu = menu  # The 'response generator' (because it sends the requests from another thread)

    @property
    def menu(self):
        return self._menu

    def _login_and_signup(self, buffer: bytes):
        res, username = Deserializer.deserialize_login_and_signup(buffer)
        if res:
            self._menu = AfterLoginMenu(self._menu.communicator, username)
            print("\nLogged in successfully!", username)
        else:
            print("\nLog in went wrong.", username)

    def _log_out(self, buffer: bytes):
        if Deserializer.deserialize_binary_response(buffer):
            self._menu = LoginMenu(self._menu.communicator)
            print("\nSign out successfully!")
        else:
            print("\nSign out in went wrong.")

    def _send_message_req(self, buffer: bytes):
        if (Deserializer.deserialize_binary_response(buffer) and
                isinstance(self._menu, AfterLoginMenu)):  # obvious - only for safety
            self._menu = SendMessageMenu(self._menu.communicator, self._menu.username, self._menu.destination)
            print("Valid message request!")
        else:
            print("\nInvalid send message request - (invalid destination)")

    def _message_ending(self, buffer: bytes):
        if (Deserializer.deserialize_binary_response(buffer) and
                isinstance(self._menu, SendMessageMenu)):  # obvious - only for safety

            # TODO: store the message in the database
            self._menu = AfterLoginMenu(self._menu.communicator, self._menu.username)
            print("\nMessage were send successfully!")
        else:
            print("\nSomething went wrong while sending the message")

    def _message_canceling(self, buffer: bytes):
        if Deserializer.deserialize_binary_response(buffer):
            if isinstance(self._menu, SendMessageMenu):  # obvious - only for safety
                self._menu = AfterLoginMenu(self._menu.communicator, self._menu.username)
                print("\nMessage sending canceled successfully!")
        else:
            print("\nSomething went wrong while canceling the message")

    def _server_error(self, buffer: bytes):
        print(MessageCode.SERVER_ERROR.name, ": ", buffer.decode())

    switch_dict = {MessageCode.LOGIN: _login_and_signup,
                   MessageCode.SIGN_UP: _login_and_signup,
                   MessageCode.SIGN_OUT: _log_out,
                   MessageCode.SEND_MESSAGE_REQ: _send_message_req,
                   MessageCode.END_MESSAGE: _message_ending,
                   MessageCode.CANCEL_MESSAGE: _message_canceling,
                   MessageCode.SERVER_ERROR: _server_error}
