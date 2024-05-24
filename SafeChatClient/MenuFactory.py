class MenuFactory:
    @staticmethod
    def create_login_menu(communicator, encryption_manager):
        from LoginMenu import LoginMenu
        return LoginMenu(communicator, encryption_manager)

    @staticmethod
    def create_after_login_menu(communicator, database, encryption_manager):
        from AfterLoginMenu import AfterLoginMenu
        return AfterLoginMenu(communicator, database, encryption_manager)

    @staticmethod
    def create_send_message_menu(communicator, database, encryption_manager, destination, public_key):
        from SendMessageMenu import SendMessageMenu
        return SendMessageMenu(communicator, database, encryption_manager, destination, public_key)

    @staticmethod
    def create_choose_chat_menu(communicator, database, encryption_manager):
        from ChooseChatMenu import ChooseChatMenu
        return ChooseChatMenu(communicator, database, encryption_manager)

    @staticmethod
    def create_chat_menu(communicator, database, encryption_manager, chat_with):
        from ChatMenu import ChatMenu
        return ChatMenu(communicator, database, encryption_manager, chat_with)
