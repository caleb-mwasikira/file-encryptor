import re
import time
from os import path
from datetime import date
from typing.io import BinaryIO
from uuid import uuid4
from base64 import b64encode


class Encryptor:
    def __init__(self, password: str):
        self.password = password.encode("utf-8")
        self.key = self.salt = None

        self.begin_delimiter: bytes = "-----BEGIN ENCRYPTION-----".encode("utf-8")
        self.end_delimiter: bytes = "-----END ENCRYPTION-----".encode("utf-8")

    @staticmethod
    def get_encrypted_filename(filename):
        parent_dir: str = path.dirname(filename)
        new_filename: str = "(encrypted)" + path.basename(filename)
        return path.join(parent_dir, new_filename)

    @staticmethod
    def get_decrypted_filename(filename):
        parent_dir: str = path.dirname(filename)
        pattern = re.compile(r"[(]encrypted[)]")
        new_filename: str = re.sub(pattern, "", path.basename(filename))
        return path.join(parent_dir, new_filename)

    @staticmethod
    def file_is_encrypted(file):
        """Checks whether file is marked as encrypted or not"""

        pattern = re.compile(r"[(]encrypted[)]")
        return re.match(pattern, path.basename(file)) or False

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

        file.write(self.begin_delimiter + new_line)

        for detail in list(encryption_header.items()):
            line: bytes = f"{detail[0]}: {detail[1]}".encode("utf-8")
            file.write(line + new_line)

        file.write(new_line)

    def read_encryption_header(self, file: BinaryIO) -> dict:
        encryption_header: dict = {}
        begin_pattern = re.compile(self.begin_delimiter)
        end_pattern = re.compile(self.end_delimiter)

        while True:
            line: bytes = file.readline().strip()

            if not line or re.match(end_pattern, line):
                break

            elif re.match(begin_pattern, line):
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
        end_pattern = re.compile(self.end_delimiter)

        while True:
            line: bytes = file.readline().strip()
            if not line or re.match(end_pattern, line):
                break

            yield line
