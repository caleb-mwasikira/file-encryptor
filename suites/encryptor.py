import re
from os import path


class Encryptor:
    def __init__(self, action: str, password: str):
        self.action = action
        self.password = password.encode("utf-8")

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
