from ClientCommunicator import ClientCommunicator
from threading import Lock
from abc import ABC

MESSAGE_SIZE_FIELD_SIZE = 4


class ClientMenu(ABC):  # abstract class
    def __init__(self, client_communicator: ClientCommunicator):
        self._client_communicator = client_communicator
        self._username = None

    def get_user_choice(self):
        self._print_menu()
        try:
            choice = self._input_process(input("Enter your choice: "))
        except ValueError:
            self.get_user_choice()
            return
        self.menu_dict[choice](self)

    @staticmethod
    def _input_process(user_choice):
        return user_choice

    def _print_menu(self):
        # print the menu options
        for k in self.menu_dict.keys():
            print(k.value, " - ", k.name.replace("_", " "))

    menu_dict = {}
