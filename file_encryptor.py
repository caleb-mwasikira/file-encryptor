#!/usr/bin/env python

from suites.fernet_encryptor import FernetEncryptor
from utils.file_manager import FileManager


ENCRYPT = ['encrypt', 'e', 'E', 'Encrypt']
DECRYPT = ['decrypt', 'd', 'D', 'Decrypt']


def main():
    _, password, action, directory = "John Doe", "password", "e", "./data"
    selected_files: list = FileManager.list_dir(directory)
    encryptor = FernetEncryptor(action, password)

    if action in ENCRYPT:
        for file in selected_files:
            if encryptor.file_is_encrypted(file):
                print(f"Cannot encrypt {file}. File already marked as encrypted")

            else:
                encryptor.encrypt_file(file)

    elif action in DECRYPT:
        for file in selected_files:
            if encryptor.file_is_encrypted(file):
                encryptor.decrypt_file(file)

            else:
                print(f"Cannot decrypt {file}. File already marked as decrypted")

    print("Done")


if __name__ == "__main__":
    main()
