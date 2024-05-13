from IHandler import *
from Deserializer import Deserializer


class NewMessagesHandler(IHandler):
    def __init__(self, database: DataBaseManager):
        super().__init__(database)

        # the message details
        self._message_data = b''
        self._source_username = ""
        self._date = ""

    def _new_message_notify(self, buffer):
        self._source_username, self._date = Deserializer.deserialize_new_message_notification(buffer)

    def _message_data_sending(self, buffer):
        self._message_data += buffer

    def _message_ending(self, buffer):
        print("\nYou got a new message!")
        print(self._source_username, ": ", self._message_data)

        # TODO: save the message in the database

        self.__init__(self._database)  # init all the message details

    switch_dict = {MessageCode.NEW_MESSAGE_RECEIVED: _new_message_notify,
                   MessageCode.MESSAGE_SENDING: _message_data_sending,
                   MessageCode.NEW_MESSAGE_END: _message_ending}
