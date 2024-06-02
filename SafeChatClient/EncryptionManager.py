from DataBaseManager import DataBaseManager
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import dh
from os import urandom, path

BYTE_SIZE_IN_BITS = 8  # bits
IV_LENGTH = 16  # bytes
AES_KEY_LENGTH = 32  # bytes
DH_KEY_LENGTH = 2048  # bits


class EncryptionManager:
    PRIVATE_FILE_EXTENSION = "_private.pem"

    def __init__(self, database: DataBaseManager):
        self._db = database
        self._default_private = None

        with open("dh_parameters.pem", "rb") as f:
            self._dh_parameters = serialization.load_pem_parameters(f.read())

    def load_public_key(self, username) -> bytes:
        """
        Load encryption private key for a user and create public key (in log in) and return the public key
        :param username: the user
        :return: the public key
        """
        filename = username + EncryptionManager.PRIVATE_FILE_EXTENSION
        if path.exists(filename):  # log-in
            with open(filename, 'rb') as key_file:
                self._default_private = serialization.load_pem_private_key(key_file.read(), password=None)
            public = self._default_private.public_key()

            return public.public_numbers().y.to_bytes(public.key_size // BYTE_SIZE_IN_BITS, 'big')

    def create_key_for_new_user_and_load(self, username) -> bytes:
        """
        Create encryption keys for a user (in sign up) and return the public one
        :param username: the user
        :return: the public key
        """
        filename = username + EncryptionManager.PRIVATE_FILE_EXTENSION
        self._default_private, public = self._generate_keys_pair()
        pem_private_key = self._default_private.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        with open(filename, 'wb') as key_file:
            key_file.write(pem_private_key)

        return public.public_numbers().y.to_bytes(public.key_size // BYTE_SIZE_IN_BITS, 'big')

    def end_to_end_decrypt(self, encrypted_message: bytes, source: str) -> str:
        # split the source public key and the message
        source_public_bytes, encrypted_message = (
            encrypted_message[:DH_KEY_LENGTH // BYTE_SIZE_IN_BITS],
            encrypted_message[DH_KEY_LENGTH // BYTE_SIZE_IN_BITS:])

        # update the last source public key
        self._db.set_last_other_public_key(source, source_public_bytes)

        # get the last private key that used to encrypt
        last_private_bytes = self._db.get_last_private_key(source)

        # switch to the right public key
        # (if there is no public key that saved - user the default one)
        if last_private_bytes:
            last_private_key = serialization.load_der_private_key(
                last_private_bytes, password=None)
        else:
            last_private_key = self._default_private

        # convert the peer public key bytes into public key object
        source_public_key = dh.DHPublicNumbers(
            int.from_bytes(source_public_bytes, 'big'),
            self._dh_parameters.parameter_numbers()).public_key()

        # deffie-hellman key exchange
        shared_key = last_private_key.exchange(source_public_key)

        # key derivation function to reduce AES shared key
        aes_key = HKDF(algorithm=hashes.SHA256(), length=AES_KEY_LENGTH,
                       salt=None, info=b"AES key derivation").derive(shared_key)

        return EncryptionManager._decrypt_data(aes_key, encrypted_message).decode()

    def end_to_end_encrypt(self, message: str, destination: str,
                           destination_public: bytes) -> bytes:
        private, public = self._generate_keys_pair()

        # convert the peer public-key from bytes into DHPublicKey
        destination_public = dh.DHPublicNumbers(
            int.from_bytes(destination_public, 'big'),
            self._dh_parameters.parameter_numbers()).public_key()

        # convert the private key into bytes using the DER encoding
        private_bytes = private.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        # update the last private key that use to encrypt in this conversation
        self._db.set_last_private_key(destination, private_bytes)

        # deffie-hellman key exchange
        shared_key = private.exchange(destination_public)

        # key derivation function to reduce AES shared key
        aes_key = HKDF(algorithm=hashes.SHA256(), length=AES_KEY_LENGTH, salt=None,
                       info=b"AES key derivation").derive(shared_key)

        # get the public key bytes (256 bytes length)
        public_bytes = public.public_numbers().y.to_bytes(
            DH_KEY_LENGTH // BYTE_SIZE_IN_BITS, 'big')

        return public_bytes + EncryptionManager._encrypt_data(aes_key, message.encode())

    def _generate_keys_pair(self) -> tuple[dh.DHPrivateKey, dh.DHPublicKey]:
        private = self._dh_parameters.generate_private_key()
        return private, private.public_key()

    @staticmethod
    def _encrypt_data(key, data):
        iv = urandom(IV_LENGTH)
        encryptor = Cipher(algorithms.AES(key), modes.CFB(iv)).encryptor()
        cipher_text = encryptor.update(data) + encryptor.finalize()
        return iv + cipher_text

    @staticmethod
    def _decrypt_data(key, data):
        iv, data = data[:IV_LENGTH], data[IV_LENGTH:]
        decryptor = Cipher(algorithms.AES(key), modes.CFB(iv)).decryptor()
        decrypted_data = decryptor.update(data) + decryptor.finalize()
        return decrypted_data
