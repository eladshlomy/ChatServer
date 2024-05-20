class MenuFactory:
    @staticmethod
    def create_login_menu(communicator):
        from LoginMenu import LoginMenu
        return LoginMenu(communicator)

    @staticmethod
    def create_after_login_menu(communicator, database):
        from AfterLoginMenu import AfterLoginMenu
        return AfterLoginMenu(communicator, database)

    @staticmethod
    def create_send_message_menu(communicator, database, destination):
        from SendMessageMenu import SendMessageMenu
        return SendMessageMenu(communicator, database, destination)

    @staticmethod
    def create_choose_chat_menu(communicator, database):
        from ChooseChatMenu import ChooseChatMenu
        return ChooseChatMenu(communicator, database)

    @staticmethod
    def create_chat_menu(communicator, database, chat_with):
        from ChatMenu import ChatMenu
        return ChatMenu(communicator, database, chat_with)
