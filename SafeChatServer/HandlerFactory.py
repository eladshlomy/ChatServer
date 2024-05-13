from DataBaseManager import DataBaseManager
from LoginManager import LoginManager


class HandlerFactory:
    @staticmethod
    def create_login_handler(database: DataBaseManager, login_manager: LoginManager):
        from LoginRequestHandler import LoginRequestHandler
        return LoginRequestHandler(database, login_manager)

    @staticmethod
    def create_after_login_handler(database: DataBaseManager, login_manager: LoginManager,
                                   username: str):
        from AfterLoginRequestHandler import AfterLoginRequestHandler
        return AfterLoginRequestHandler(database, login_manager, username)

    @staticmethod
    def create_sending_message_handler(database: DataBaseManager, login_manager: LoginManager,
                                       from_user: str, to_user: str):
        from SendingMessageHandler import SendingMessageHandler
        return SendingMessageHandler(database, login_manager, from_user, to_user)
