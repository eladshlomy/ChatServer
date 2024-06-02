from ClientCommunicator import ClientCommunicator
from NewMessagesHandler import NewMessagesHandler
from ResponseHandler import ResponseHandler
from DataBaseManager import DataBaseManager
from MenuFactory import MenuFactory
from threading import Lock
from EncryptionManager import EncryptionManager


class ClientManager:
    def __init__(self):
        self._communicator = ClientCommunicator()
        self._database = DataBaseManager()
        self._encryption_manager = EncryptionManager(self._database)

        self.__menu = MenuFactory.create_login_menu(self._communicator, self._encryption_manager)
        self._menu_lock = Lock()
        self._new_messages_handler = NewMessagesHandler(self._database, self._encryption_manager)
        self._response_handler = ResponseHandler(self._database, self._encryption_manager)

    @property
    def menu(self):
        return self.__menu

    @menu.setter
    def menu(self, new_menu):
        if new_menu is not None:
            self.__menu = new_menu
            self._menu_lock.release()

    def received_thread(self):
        while True:
            code, buffer = self._communicator.receive()
            if self._new_messages_handler.is_relevant(code):
                self._new_messages_handler.handle(code, buffer)  # handling the new message

            elif self._response_handler.is_relevant(code):
                self.menu = self._response_handler.handle(code, buffer, self.menu)

            else:
                print("Invalid code packet received.\n", code, buffer)

    def menu_thread(self):
        while True:
            self._menu_lock.acquire()  # lock the menu
            self.menu.print_menu()
            self.menu = self.menu.make_choice(self.menu.get_choice())
