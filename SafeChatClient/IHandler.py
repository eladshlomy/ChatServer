from abc import ABC
from MessageCode import MessageCode
from DataBaseManager import DataBaseManager
from EncryptionManager import EncryptionManager


class IHandler(ABC):
    def __init__(self, database: DataBaseManager, encryption_manager: EncryptionManager):
        self._database = database
        self._encryption_manager = encryption_manager

    def is_relevant(self, code: MessageCode) -> bool:
        return code in self.switch_dict

    def handle(self, code: MessageCode, buffer: bytes, *params):
        return self.switch_dict[code](self, buffer, *params)

    switch_dict = {}
