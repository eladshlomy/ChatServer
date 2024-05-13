from threading import Condition
from socket import socket
from Serializer import Serializer
from Communicator import Communicator

MESSAGE_CHUNK_SIZE = 5

# Message details indexes
FROM_USERNAME = 0
TO_USERNAME = 1
MESSAGE_DATA = 2
DATE = 3


class MessageNotifier:
    def __init__(self, clients_dictionary_reference: dict, communicator: Communicator):
        self._clients = clients_dictionary_reference
        self._communicator = communicator
        self._messages_queue = []
        self._new_messages_condition = Condition()

    def notify_a_message(self,from_user: str, to_user: str, message: bytes, date: str):
        with self._new_messages_condition:  # lock the queue and release when finish
            self._messages_queue.append((from_user, to_user, message, date))
            self._new_messages_condition.notify()

    def notify_messages(self, messages: list[tuple[int, str, str, bytes, str]]):
        with self._new_messages_condition:
            for message in messages:
                self._messages_queue.append(message)
            self._new_messages_condition.notify()

    def notifier_loop(self):
        """
        A thread function that waiting to the '_new_messages_condition' condition to notify
        and then pop the new message from the queue and send the message to the target
        """
        while True:
            with self._new_messages_condition:  # lock the queue and release when finish
                if self._new_messages_condition.wait():  # wait for notifying
                    while self._messages_queue:  # handle all the messages
                        message_details = self._messages_queue.pop(0)
                        target = self._find_online_user_socket(message_details[TO_USERNAME])

                        if target:  # if the target is online and was found
                            self._handle_message_and_send(message_details[FROM_USERNAME],
                                                          target, message_details[MESSAGE_DATA], message_details[DATE])

    def _handle_message_and_send(self,from_username, target: socket, message: bytes, date):
        self._communicator.send(target, Serializer.serialize_new_message_notify(from_username, date))

        # split the message into chunks and send each chunk to the server
        for i in range(0, len(message), MESSAGE_CHUNK_SIZE):
            self._communicator.send(target, Serializer.serialize_chunk_message_sending(message[i: i + MESSAGE_CHUNK_SIZE]))

        # notifies the client that we have sent all the message chunks
        self._communicator.send(target, Serializer.serialize_new_message_end())

    def _find_online_user_socket(self, username: str) -> socket:
        """
        this method gets online-user and return the username socket
        :param username: the online-user's username
        :return: the user socket
        """
        for k, v in self._clients.items():
            if v.is_logged_in() and v.get_username() == username:
                return k
