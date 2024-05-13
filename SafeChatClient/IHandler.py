from abc import ABC
from MessageCode import MessageCode
from DataBaseManager import DataBaseManager


class IHandler(ABC):
    def __init__(self, database: DataBaseManager):
        self._database = database

    def is_relevant(self, code: MessageCode) -> bool:
        return code in self.switch_dict

    def handle(self, code: MessageCode, buffer: bytes) -> None:
        self.switch_dict[code](self, buffer)

    switch_dict = {}
