from ClientHandler import ClientHandler
from threading import Thread

handler = ClientHandler()

received_thread = Thread(target=handler.receive_loop)
received_thread.daemon = True  # this thread in running at the background all the time!
received_thread.start()

handler.menu_loop()

# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.kdf.hkdf import HKDF
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.primitives import serialization
# from os import urandom
#
#
# def encrypt_data(key, data):
#     iv = urandom(16)
#     encryptor = Cipher(algorithms.AES(key), modes.CFB(iv)).encryptor()
#     ct = encryptor.update(data) + encryptor.finalize()
#     return iv + ct
#
#
# def decrypt_data(key, data):
#     iv, data = data[:16], data[16:]
#
#     decryptor = Cipher(algorithms.AES(key), modes.CFB(iv)).decryptor()
#     decrypted_data = decryptor.update(data) + decryptor.finalize()
#     return decrypted_data
#
#
# with open("dh_parameters.pem", "rb") as f:
#     parameters = serialization.load_pem_parameters(f.read())
#
#
# private_key1 = parameters.generate_private_key()
# private_key2 = parameters.generate_private_key()
#
# public_key1 = private_key1.public_key()
# public_key2 = private_key2.public_key()
#
# shared_key1 = private_key1.exchange(public_key2)
# shared_key2 = private_key2.exchange(public_key1)
#
# print("Shared key 1:", shared_key1)
# print("Shared key 2:", shared_key2)
# print("Are shared keys equal?", shared_key1 == shared_key2)
#
# aes_key1 = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"AES key derivation").derive(shared_key1)
# aes_key2 = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"AES key derivation").derive(shared_key2)
# print("AES Key 1:", aes_key1)
# print("AES Key 2:", aes_key2)
# print("Are AES keys equal?", aes_key1 == aes_key2)
#
# # Encrypt data using shared keys
# data_to_encrypt = b"Hello, this is a secret message"
# encrypted_data1 = encrypt_data(aes_key1, data_to_encrypt)
# encrypted_data2 = encrypt_data(aes_key2, data_to_encrypt)
#
# print("Encrypted data 1:", encrypted_data1)
# print("Encrypted data 2:", encrypted_data2)
#
# # Decrypt data using shared keys
# decrypted_data1 = decrypt_data(aes_key1, encrypted_data1)
# decrypted_data2 = decrypt_data(aes_key2, encrypted_data2)
#
# print("Decrypted data 1:", decrypted_data1)
# print("Decrypted data 2:", decrypted_data2)

