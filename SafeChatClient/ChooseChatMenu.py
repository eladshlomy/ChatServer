from AfterLoginMenu import AfterLoginMenu
from enum import Enum
from DataBaseManager import DataBaseManager
from ChatMenu import ChatMenu
from MenuFactory import MenuFactory


class ChooseChatMenu(AfterLoginMenu):
    def __init__(self, communicator, database: DataBaseManager):
        super().__init__(communicator, database)

        enum_values = {}
        count = 0
        for count, username in enumerate(self._database.users_in_chat(), 1):
            enum_values[username] = count

        enum_values["EXIT"] = count + 1

        # create enum dynamically like this -> USERNAME_CHAT = user_choice_number
        self.Option = Enum('Option', enum_values)

    def make_choice(self, choice):
        if choice is self.Option.EXIT:
            return MenuFactory.create_after_login_menu(self._client_communicator, self._database)
        return MenuFactory.create_chat_menu(self._client_communicator, self._database, choice.name)

