import socket

import MessageCode
from Deserializer import Deserializer
from Serializer import Serializer

SERVER_PORT = 8282
MESSAGE_SIZE_FIELD_SIZE = 4
MESSAGE_CHUNK_SIZE = 1024

# before login menu
LOG_IN = 1
SIGN_UP = 2


# after login menu
SEND_MESSAGE = 1
LOG_OUT = 2


class ClientMenu:
    def __init__(self):
        # create socket and connect the server
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect(('127.0.0.1', SERVER_PORT))
        self._logged_in = False
        self._username = ""

    def print_menu(self):
        if self._logged_in:
            print(f"{LOG_OUT} - LOG OUT")
            print(f"{SEND_MESSAGE} - SEND_MESSAGE")

        else:
            print(f"{LOG_IN} - LOG IN")
            print(f"{SIGN_UP} - SIGN UP")

    def act_by_user_choice(self, choice: int):
        if self._logged_in:
            if choice == LOG_OUT:
                self.logout()
            elif choice == SEND_MESSAGE:
                self.send_message()
            else:
                print("Invalid choice, try again")

        else:
            if choice == SIGN_UP:
                self.sign_up()
            elif choice == LOG_IN:
                self.login()
            else:
                print("Invalid choice, try again")

    def sign_up(self):
        username = input("Please enter your username: ")
        password = input("Please choose a password: ")
        email = input("Please enter your email: ")

        req_buffer = Serializer.serialize_signup(username, password, email)
        self._send_request(req_buffer)  # send the request to the server

        code, response = self._receive_response()

        if code == MessageCode.MessageCode.SIGN_UP:
            if Deserializer.deserialize_binary_response(response):
                print("Sign up successfully!")
                self._logged_in = True
                self._username = username
            else:
                print("sign up went wrong")

        else:
            print(f"The code message is {code} instead of {MessageCode.MessageCode.SIGN_OUT}")
            print(response)

    def login(self):
        username = input("Please enter your username: ")
        password = input("Please choose a password: ")

        req_buffer = Serializer.serialize_login(username, password)
        self._send_request(req_buffer)  # send the request to the server

        code, response = self._receive_response()

        if code == MessageCode.MessageCode.LOGIN:
            if Deserializer.deserialize_binary_response(response):
                print("Log in successfully!")
                self._logged_in = True
                self._username = username
            else:
                print("Log in went wrong")

        else:
            print(f"The code message is {code} instead of {MessageCode.MessageCode.SIGN_OUT}")
            print(response)

    def logout(self):
        req_buffer = Serializer.serialize_logout()
        self._send_request(req_buffer)  # send the request to the server

        code, response = self._receive_response()

        if code == MessageCode.MessageCode.SIGN_OUT:
            if Deserializer.deserialize_binary_response(response):
                print("Sign out successfully!")
                self._logged_in = False

        else:
            print(f"The code message is {code} instead of {MessageCode.MessageCode.SIGN_OUT}")
            print(response)

    def send_message(self):
        destination = input("Please enter the username you would like to send a message to: ")
        self._send_request(Serializer.serialize_send_message_req(destination))

        code, response = self._receive_response()
        response = Deserializer.deserialize_binary_response(response)

        if code == MessageCode.MessageCode.SEND_MESSAGE_REQ and response:
            message = input("Please enter the message: ")

            # split the message into chunks and send each chunk to the server
            for i in range(0, len(message), MESSAGE_CHUNK_SIZE):
                self._send_request(Serializer.serialize_sending_message(message[i: i + MESSAGE_CHUNK_SIZE]))

            self._send_request(Serializer.serialize_end_message())

            code, response = self._receive_response()
            response = Deserializer.deserialize_binary_response(response)

            if response:
                print("Message were send successfully!")
            else:
                print("Something went wrong while sending the message")

    def get_new_messages(self):
        pass

    def _send_request(self, buffer: bytes):
        buffer = len(buffer).to_bytes(MESSAGE_SIZE_FIELD_SIZE) + buffer
        self._sock.send(buffer)

    def _receive_response(self) -> tuple[MessageCode.MessageCode, bytes]:
        size = int.from_bytes(self._sock.recv(MESSAGE_SIZE_FIELD_SIZE))
        buffer = self._sock.recv(size)

        return (MessageCode.MessageCode(int.from_bytes(buffer[:MessageCode.MESSAGE_CODE_FIELD_SIZE])),
                buffer[MessageCode.MESSAGE_CODE_FIELD_SIZE:])
