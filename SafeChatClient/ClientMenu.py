from ClientCommunicator import ClientCommunicator
from EncryptionManager import EncryptionManager
from enum import Enum
from abc import ABC

MESSAGE_SIZE_FIELD_SIZE = 4


class ClientMenu(ABC):  # abstract class
    class Option(Enum):
        pass

    def __init__(self, client_communicator: ClientCommunicator, encryption_manager: פרןמ):
        self._client_communicator = client_communicator
        self._encryption_manager = encryption_manager

    @property
    def communicator(self):
        return self._client_communicator

    def print_menu(self):
        # print the menu options
        for option in self.Option:
            print(option.value, "-", option.name)

    def get_choice(self) -> Option:
        try:
            choice = self.Option(int(input("Enter your choice: ")))
        except ValueError:
            print("Invalid input, please try again. ")
            return self.get_choice()
        return choice

    def make_choice(self, choice: Option):
        """
        :param choice: the user choice - represent an act that the menu should do
        :return: None - If the menu does not yet know the result of the choice,
         and you have to wait for a response from the server.
         Else - the new menu after the choice
        """
        return self.menu_dict[choice](self)

    menu_dict = {}
