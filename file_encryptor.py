#!/usr/bin/env python
import sys
import argparse

from ui.cli import CLI
from suites.fernet_encryptor import FernetEncryptor

ENCRYPT = ['encrypt', 'e', 'E', 'Encrypt']
DECRYPT = ['decrypt', 'd', 'D', 'Decrypt']


def get_program_args():
    parser = argparse.ArgumentParser(
        allow_abbrev=False,
        description='A tool for encrypting and decrypting files'
    )
    parser.version = "1.0.0"

    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('-e', '--encrypt', action="store_true", help="runs the program in encrypt mode")
    action_group.add_argument('-d', '--decrypt', action="store_true", help="runs the program in decrypt mode")

    parser.add_argument('-p', '--path', action="store", nargs="+",
                        help="directory(ies) to select files for encryption/decryption")
    parser.add_argument('-v', '--version', action='version')

    args = parser.parse_args()

    user_action = "encrypt" if args.encrypt else "decrypt"
    directory = args.path
    return user_action, directory


def init_program() -> (str, str, str, str):
    try:
        # username, password, directory = "John Doe", "password", "./data"

        username, password = CLI.get_user_auth_info()
        action, directory = get_program_args()

        if directory is None:
            directory = CLI.get_dir(action)

        selected_files: list = CLI.select_files_in_dir(directory)
        return username, password, action, selected_files

    except KeyboardInterrupt:
        print("Cancelled by user")
        sys.exit(1)


def main():
    username, password, action, selected_files = init_program()
    encryptor = FernetEncryptor(password)

    for file in selected_files:
        if action in ENCRYPT:
            encryptor.encrypt_file(file)

        else:
            encryptor.decrypt_file(file)


if __name__ == "__main__":
    main()
