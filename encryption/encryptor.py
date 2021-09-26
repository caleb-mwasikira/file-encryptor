import re
import time
from datetime import date
from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO
from uuid import uuid4
from base64 import b64encode

from utils.user_actions import UserActions


def get_new_filename(filename: str, action: UserActions = UserActions.ENCRYPT) -> str:
    if action == UserActions.ENCRYPT:
        new_filename: str = "(encrypted)" + filename

    else:
        pattern = re.compile(r"[(]encrypted[)]")
        new_filename: str = re.sub(pattern, "", filename)

    return new_filename


def file_is_encrypted(filename: str) -> bool:
    """Checks whether file is marked as encrypted or not"""

    pattern = re.compile(r"[(]encrypted[)]")
    return re.match(pattern, filename) or False
    

class Encryptor(ABC):
    def __init__(self, password: str):
        self.password = password.encode("utf-8")
        self.key = self.salt = None

        self.BEGIN_DELIMITER: bytes = "-----BEGIN ENCRYPTION-----".encode("utf-8")
        self.END_DELIMITER: bytes = "-----END ENCRYPTION-----".encode("utf-8")

        self.begin_pattern = re.compile(self.BEGIN_DELIMITER)
        self.end_pattern = re.compile(self.END_DELIMITER)

    @abstractmethod
    def encrypt_file(self, file: Path):
        """"""

    @abstractmethod
    def decrypt_file(self, file: Path):
        """"""

    def write_encryption_header(self, file: BinaryIO):
        today = date.today()
        t = time.localtime()
        date_time: str = today.strftime("%b-%d-%Y") + " " + time.strftime("%H:%M:%S", t)

        new_line: bytes = "\n".encode("utf-8")

        encryption_header = {
            "File-ID": f"{uuid4()}".upper(),
            "Encryption-Type": "FERNET-SYMMETRIC-ENCRYPTION",
            "IV": b64encode(self.salt),
            "Date-Time": date_time,
        }

        file.write(self.BEGIN_DELIMITER + new_line)

        for detail in list(encryption_header.items()):
            line: bytes = f"{detail[0]}: {detail[1]}".encode("utf-8")
            file.write(line + new_line)

        file.write(new_line)

    def read_encryption_header(self, file: BinaryIO) -> dict:
        encryption_header: dict = {}

        while True:
            line: bytes = file.readline().strip()

            if not line or re.match(self.end_pattern, line):
                break

            elif re.match(self.begin_pattern, line):
                continue

            else:
                data: list = line.decode("utf-8").split(":")
                key, value = data[0], data[1]
                encryption_header[key] = value

        return encryption_header

    @staticmethod
    def read_plaintext_file_in_chunks(file: BinaryIO):
        """Lazy reads a file chunk by chunk"""
        CHUNK_SIZE = 1024

        while True:
            buffer: bytes = file.read(CHUNK_SIZE)
            if not buffer:  # End of file...no more data left to read
                break

            yield buffer

    def read_encrypted_file_in_chunks(self, file: BinaryIO):
        while True:
            buffer: bytes = file.readline().strip()
            if not buffer or re.match(self.end_pattern, buffer):
                break

            yield buffer
