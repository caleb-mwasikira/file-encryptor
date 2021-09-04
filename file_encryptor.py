#!/usr/bin/env python
import sys

from ui.cli import CLI
from suites.fernet_encryptor import FernetEncryptor

ENCRYPT = ['encrypt', 'e', 'E', 'Encrypt']
DECRYPT = ['decrypt', 'd', 'D', 'Decrypt']


def init_program() -> (str, str, str, str):
    try:
        # username, password, directory = "John Doe", "password", "./data"
        username, password = CLI.get_user_auth_info()

        action = CLI.get_user_action()
        directory = CLI.get_dir(action)

        selected_files: list = []
        while len(selected_files) == 0:
            print(f"Please select the files you would like to {action}")
            selected_files: list = CLI.select_files_in_dir(directory)

        return username, password, action, selected_files

    except KeyboardInterrupt:
        print("Cancelled by user")
        sys.exit(1)


def main():
    username, password, action, selected_files = init_program()
    encryptor = FernetEncryptor(password)

    if action in ENCRYPT:
        for file in selected_files:
            if encryptor.file_is_encrypted(file):
                print(f"[?] Cannot encrypt {file}. File already marked as encrypted")

            else:
                encryptor.encrypt_file(file)

    elif action in DECRYPT:
        for file in selected_files:
            if encryptor.file_is_encrypted(file):
                encryptor.decrypt_file(file)

            else:
                print(f"[?] Cannot decrypt {file}. File already marked as decrypted")


if __name__ == "__main__":
    main()
