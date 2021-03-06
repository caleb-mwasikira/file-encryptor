"""

Fernet is ideal for encrypting data that easily fits in memory. 
As a design feature it does not expose unauthenticated bytes. 
This means that the complete message contents must be available in memory, 
making Fernet generally unsuitable for very large files at this time.
(ref https://cryptography.io/en/latest/fernet/#limitations)

"""

import os
from base64 import b64encode, b64decode
from pathlib import Path
from typing import Tuple

from cryptography.fernet import Fernet, InvalidToken, InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from encryption.encryptor import Encryptor, file_is_encrypted, get_new_filename
from utils.user_actions import UserActions


def key_derivation_func(password: bytes, salt: bytes = None) -> Tuple[bytes, bytes]:
    BYTES = 16
    salt: bytes = salt or os.urandom(BYTES)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    key = b64encode(kdf.derive(password))
    return key, salt


class FernetEncryptor(Encryptor):
    def __init__(self, password: str):
        super().__init__(password)

    def encrypt_file(self, file: Path):
        if file_is_encrypted(file.name):
            print(f"[+] File {file.__str__()} already marked as encrypted")
            return

        self.key, self.salt = key_derivation_func(self.password)
        cipher = Fernet(self.key)

        new_filename: str = get_new_filename(file.name, action=UserActions.ENCRYPT)
        new_filepath: Path = Path.joinpath(file.parent, new_filename)

        try:
            print(f"[*] Encrypting {file}")
            new_line: bytes = "\n".encode("utf-8")

            with open(file, "rb") as read_file, open(new_filepath, "wb") as write_file:
                self.write_encryption_header(write_file)

                for data_chunk in self.read_plaintext_file_in_chunks(read_file):
                    if data_chunk:
                        encrypted_data: bytes = cipher.encrypt(data_chunk)
                        write_file.write(encrypted_data + new_line)

                write_file.write(self.END_DELIMITER + new_line)

            os.remove(file)

        except FileNotFoundError:
            print(f"[!] File {file} not found")

        except (InvalidToken, InvalidSignature) as error:
            print(f"[!] Error: {error}")

    def decrypt_file(self, file: Path):
        if not file_is_encrypted(file.name):
            print(f"[+] File {file.__str__()} already marked as decrypted")
            return

        new_filename: str = get_new_filename(file.name, action=UserActions.DECRYPT)
        new_filepath: Path = Path.joinpath(file.parent, new_filename)

        try:
            print(f"[*] Decrypting {file}")
            with open(file, "rb") as read_file, open(new_filepath, "wb") as write_file:
                header = self.read_encryption_header(read_file)
                iv: bytes = b64decode(header["IV"].strip("b' '").encode("utf-8"))

                key, salt = key_derivation_func(self.password, iv)
                cipher = Fernet(key)

                for data_chunk in self.read_encrypted_file_in_chunks(read_file):
                    if data_chunk:
                        plain_text: bytes = cipher.decrypt(data_chunk)
                        write_file.write(plain_text)

            os.remove(file)

        except FileNotFoundError:
            print(f"[!] File {file} not found")

        except (InvalidToken, InvalidSignature) as error:
            print(f"[!] Error: {error}")
