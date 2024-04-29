from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from os import path, urandom

PUBLIC_NAME_FILE = "_public.pem"
PRIVATE_NAME_FILE = "_private.pem"

AES_KEY_LENGTH = 32  # bytes
IV_LENGTH = 16
"""
EncryptionManager

+ diffie_hellman_parameters
+ server_public_key

- public_key
- private_key

* EncryptionManager(username)
* EncryptionManager(username, sign_up)
* end_to_end_encrypt(peer_public_key, bytes)
* end_to_end_decrypt(peer_public_key, bytes)
* server_encrypt(bytes)
* server_decrypt(bytes)
"""


class EncryptionManager:
    with open("dh_parameters.pem", "rb") as f:
        DH_PARAMETERS = serialization.load_pem_parameters(f.read())

    with open("server_public_key.pem", "rb") as public_key_file:
        SERVER_RSA_PUBLIC_KEY = serialization.load_pem_public_key(public_key_file.read())

    def __init__(self, username: str):
        self._username = username

        if path.isfile(self._username + PUBLIC_NAME_FILE) and path.isfile(self._username + PRIVATE_NAME_FILE):
            self._load_keys()

        else:
            # generate new keys
            self._private_key = EncryptionManager.DH_PARAMETERS.generate_private_key()
            self._public_key = self._private_key.public_key()
            self._save_keys()  # save the new keys in pem format

    def _load_keys(self):
        with (open(self._username + PUBLIC_NAME_FILE, "rb") as public_file,
              open(self._username + PRIVATE_NAME_FILE, "rb") as private_file):
            self._public_key = serialization.load_pem_public_key(public_file.read())
            self._private_key = serialization.load_pem_private_key(private_file.read(), None)

    def _save_keys(self):
        with (open(self._username + PUBLIC_NAME_FILE, "wb") as public_file,
              open(self._username + PRIVATE_NAME_FILE, "wb") as private_file):
            public_file.write(self._public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                            format=serialization.PublicFormat.SubjectPublicKeyInfo))
            private_file.write(self._private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                               format=serialization.PrivateFormat.PKCS8,
                                                               encryption_algorithm=serialization.NoEncryption()))

    def get_public_key(self):
        return self._public_key

    def _deffie_hellman_aes(self, peer_public_key):
        shared_key = self._private_key.exchange(peer_public_key)
        return HKDF(
            algorithm=hashes.SHA256(), length=AES_KEY_LENGTH, salt=None, info=b"AES key derivation").derive(shared_key)

    def end_to_end_encrypt(self, peer_public_key, data: bytes) -> bytes:
        iv = urandom(IV_LENGTH)
        encryptor = Cipher(algorithms.AES(self._deffie_hellman_aes(peer_public_key)), modes.CFB(iv)).encryptor()
        ct = encryptor.update(data) + encryptor.finalize()
        return iv + ct

    def end_to_end_decrypt(self, peer_public_key, data: bytes) -> bytes:
        iv, data = data[:IV_LENGTH], data[IV_LENGTH:]

        decryptor = Cipher(algorithms.AES(self._deffie_hellman_aes(peer_public_key)), modes.CFB(iv)).decryptor()
        decrypted_data = decryptor.update(data) + decryptor.finalize()
        return decrypted_data

    def server_encrypt(self):
        pass

    def server_decrypt(self):
        pass
