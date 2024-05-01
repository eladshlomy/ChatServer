from DataBaseManager import DataBaseManager
from LoginManager import LoginManager
from socket import socket


class HandlerFactory:
    @staticmethod
    def create_login_handler(database: DataBaseManager, login_manager: LoginManager, socket_reference: socket):
        from LoginRequestHandler import LoginRequestHandler
        return LoginRequestHandler(database, login_manager, socket_reference)

    @staticmethod
    def create_after_login_handler(database: DataBaseManager, login_manager: LoginManager, socket_reference: socket,
                                   username: str):
        from AfterLoginRequestHandler import AfterLoginRequestHandler
        return AfterLoginRequestHandler(database, login_manager, socket_reference, username)

    @staticmethod
    def create_sending_message_handler(database: DataBaseManager, login_manager: LoginManager, socket_reference: socket,
                                       from_user: str, to_user: str):
        from SendingMessageHandler import SendingMessageHandler
        return SendingMessageHandler(database, login_manager, socket_reference, from_user, to_user)
