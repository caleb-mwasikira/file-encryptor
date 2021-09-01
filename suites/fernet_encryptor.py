"""

Fernet is ideal for encrypting data that easily fits in memory. 
As a design feature it does not expose unauthenticated bytes. 
This means that the complete message contents must be available in memory, 
making Fernet generally unsuitable for very large files at this time.
(ref https://cryptography.io/en/latest/fernet/#limitations)

"""

import os
from base64 import b64encode, b64decode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

from suites.encryptor import Encryptor


class FernetEncryptor(Encryptor):
    def __init__(self, action: str, password: str):
        super().__init__(action, password)
        self.delimiter: bytes = "::".encode("utf-8")
        self.key = self.salt = None

    @staticmethod
    def key_derivation_func(password: bytes, salt: bytes = None) -> (bytes, bytes):
        BYTES = 16
        salt = salt or os.urandom(BYTES)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        key = b64encode(kdf.derive(password))
        return key, salt

    def encrypt_file(self, file):
        self.key, self.salt = self.key_derivation_func(self.password)
        cipher = Fernet(self.key)

        try:
            new_filename: str = self.get_encrypted_filename(file)

            with open(file, "rb") as read_file, open(new_filename, "wb") as write_file:
                plain_text_data: bytes = read_file.read()

                if plain_text_data:
                    print(f"Encrypting data from [ {file} ]")
                    encrypted_data: bytes = cipher.encrypt(plain_text_data)
                    cipher_text: bytes = b64encode(self.salt) + self.delimiter + encrypted_data

                    write_file.write(cipher_text)
                    print(f"File {file} encrypted successfully")

            os.remove(file)

        except FileNotFoundError:
            print(f"File {file} does not exist")

    def decrypt_file(self, file):
        try:
            new_filename: str = self.get_decrypted_filename(file)

            with open(file, "rb") as read_file, open(new_filename, "wb") as write_file:
                cipher_text: bytes = read_file.read()

                if cipher_text:
                    salt, encrypted_data = cipher_text.split(self.delimiter)

                    self.key, self.salt = self.key_derivation_func(self.password, b64decode(salt))
                    cipher = Fernet(self.key)

                    print(f"Decrypting data from [ {file} ]")
                    plain_text: bytes = cipher.decrypt(encrypted_data)

                    write_file.write(plain_text)
                    print(f"File {file} decrypted successfully")

            os.remove(file)

        except FileNotFoundError:
            print(f"File {file} does not exist")
