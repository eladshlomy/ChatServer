from IHandler import *
from Deserializer import Deserializer
from MenuFactory import MenuFactory

# menus
from ClientMenu import ClientMenu
from AfterLoginMenu import AfterLoginMenu
from SendMessageMenu import SendMessageMenu


class ResponseHandler(IHandler):
    def _login_and_signup(self, buffer: bytes, menu: ClientMenu):
        res, username = Deserializer.deserialize_login_and_signup(buffer)
        if res:
            # connect and init the database
            self._database.connect(username)

            print("\nLogged in successfully!\n", username)

            print("Hello", username + "!")
            print("Welcome back!")

            return MenuFactory.create_after_login_menu(menu.communicator, self._database)

        print("\nLog in went wrong.", username)
        return menu

    def _log_out(self, buffer: bytes, menu: ClientMenu):
        if Deserializer.deserialize_binary_response(buffer):
            self._database.disconnect()
            print("\nSign out successfully!")

            return MenuFactory.create_login_menu(menu.communicator)

        print("\nSign out is went wrong.")
        return menu

    def _send_message_req(self, buffer: bytes, menu: ClientMenu):
        if (Deserializer.deserialize_binary_response(buffer) and
                isinstance(menu, AfterLoginMenu)):  # obvious - only for safety

            print("Valid message request!")
            return MenuFactory.create_send_message_menu(menu.communicator, self._database, menu.destination)

        print("\nInvalid send message request - (invalid destination)")
        return menu

    def _message_ending(self, buffer: bytes, menu: ClientMenu):
        if (Deserializer.deserialize_binary_response(buffer) and
                isinstance(menu, SendMessageMenu)):  # obvious - only for safety
            # store the message in the database
            self._database.add_sent_message(menu.destination, menu.message_data)

            print("\nMessage were send successfully!")
            return MenuFactory.create_after_login_menu(menu.communicator, self._database)

        print("\nSomething went wrong while sending the message")
        return menu

    def _message_canceling(self, buffer: bytes, menu: ClientMenu):
        if Deserializer.deserialize_binary_response(buffer):
            print("\nMessage sending canceled successfully!")
            return MenuFactory.create_after_login_menu(menu.communicator, self._database)

        print("\nSomething went wrong while canceling the message")
        return menu

    def _server_error(self, buffer: bytes, menu: ClientMenu):
        print(MessageCode.SERVER_ERROR.name, ": ", buffer.decode(), ". In menu: " + str(type(menu)))
        return menu

    switch_dict = {MessageCode.LOGIN: _login_and_signup,
                   MessageCode.SIGN_UP: _login_and_signup,
                   MessageCode.SIGN_OUT: _log_out,
                   MessageCode.SEND_MESSAGE_REQ: _send_message_req,
                   MessageCode.END_MESSAGE: _message_ending,
                   MessageCode.CANCEL_MESSAGE: _message_canceling,
                   MessageCode.SERVER_ERROR: _server_error}
