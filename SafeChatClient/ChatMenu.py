from AfterLoginMenu import AfterLoginMenu, Enum
from MenuFactory import MenuFactory


class ChatMenu(AfterLoginMenu):
    class Option(Enum):
        PRINT_CHAT = 1
        SEND_MESSAGE = 2
        DELETE_CHAT = 3
        EXIT = 4
        # BLOCK_USER = 5

    def __init__(self, communicator, database, encryption_manager, chat_with):
        super().__init__(communicator, database, encryption_manager)
        self._chat_with = chat_with

    def _print_chat(self):
        for source, dest, message in self._database.get_chat(self._chat_with):
            print(source, ":", message)
        return self

    def _send_message(self):
        self._send_message_req(self._chat_with)

    def _delete_chat(self):
        self._database.delete_chat(self._chat_with)
        return self._exit()

    def _exit(self):
        return MenuFactory.create_choose_chat_menu(self._client_communicator, self._database, self._encryption_manager)

    menu_dict = {Option.PRINT_CHAT: _print_chat,
                 Option.SEND_MESSAGE: _send_message,
                 Option.DELETE_CHAT: _delete_chat,
                 Option.EXIT: _exit}
