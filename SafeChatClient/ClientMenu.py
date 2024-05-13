from ClientCommunicator import ClientCommunicator
from enum import Enum
from abc import ABC

MESSAGE_SIZE_FIELD_SIZE = 4


class ClientMenu(ABC):  # abstract class
    class Option(Enum):
        pass

    def __init__(self, client_communicator: ClientCommunicator):
        self._client_communicator = client_communicator

    @property
    def communicator(self):
        return self._client_communicator

    def print_menu(self):
        # print the menu options
        for k in self.menu_dict.keys():
            print(k.value, " - ", k.name.replace("_", " "))

    def choose_option(self):
        try:
            choice = self.Option(int(input("Enter your choice: ")))
        except ValueError:
            print("Invalid input, please try again. ")
            return self.choose_option()
        self.menu_dict[choice](self)

    menu_dict = {}
