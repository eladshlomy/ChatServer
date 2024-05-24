from IHandler import *
from Deserializer import Deserializer


class NewMessagesHandler(IHandler):
    def __init__(self, database: DataBaseManager, encryption_manager):
        super().__init__(database, encryption_manager)

        # the message details
        self._message_data = b''
        self._source_username = ""
        self._date = ""

    def _new_message_notify(self, buffer):
        self._source_username, self._date = Deserializer.deserialize_new_message_notification(buffer)

    def _message_data_sending(self, buffer):
        self._message_data += buffer

    def _message_ending(self, buffer):
        decrypted_message = self._encryption_manager.end_to_end_decrypt(self._message_data, self._source_username)

        print("\nYou got a new message!\n" + self._source_username + ": " + decrypted_message)
        self._database.add_received_message(self._source_username, decrypted_message)

        self.__init__(self._database, self._encryption_manager)  # init all the message details

    switch_dict = {MessageCode.NEW_MESSAGE_RECEIVED: _new_message_notify,
                   MessageCode.MESSAGE_SENDING: _message_data_sending,
                   MessageCode.NEW_MESSAGE_END: _message_ending}
