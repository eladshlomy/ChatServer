from ClientCommunicator import ClientCommunicator
from NewMessagesHandler import NewMessagesHandler
from ResponseHandler import ResponseHandler
from DataBaseManager import DataBaseManager
from threading import Lock
from LoginMenu import LoginMenu


class ClientManager:
    def __init__(self):
        self._communicator = ClientCommunicator()
        self._database = DataBaseManager()

        self._new_messages_handler = NewMessagesHandler(self._database)
        self._response_handler = ResponseHandler(self._database, LoginMenu(self._communicator))
        self._menu_lock = Lock()

    def received_thread(self):
        while True:
            code, buffer = self._communicator.receive()
            if self._new_messages_handler.is_relevant(code):
                self._new_messages_handler.handle(code, buffer)  # handling the new message

            elif self._response_handler.is_relevant(code):
                self._response_handler.handle(code, buffer)
                self._menu_lock.release()  # release the menu
            else:
                print("Invalid code packet received.\n", code, buffer)

    def menu_thread(self):
        while True:
            self._menu_lock.acquire()  # lock the menu
            self._response_handler.menu.print_menu()
            self._response_handler.menu.choose_option()
