#!/usr/bin/env python

from ui.cli import CLI
from suites.fernet_encryptor import FernetEncryptor
from utils.file_manager import FileManager


ENCRYPT = ['encrypt', 'e', 'E', 'Encrypt']
DECRYPT = ['decrypt', 'd', 'D', 'Decrypt']


def init_program() -> (str, str, str, str):
    username, password = CLI.get_user_auth_info()

    action = CLI.get_user_action()
    directory = CLI.get_dir(action)
    files_in_directory: list = FileManager.list_dir(directory)

    selected_files: list = []
    while len(selected_files) == 0:
        print(f"\nThe directory {directory} has {len(files_in_directory)} files")
        print(f"Please select the files you would like to {action}")
        selected_files: list = CLI.select_files_in_dir(directory)

    print("\nGreat! Now wait for file encryptor to work on your files ...")
    return username, password, action, selected_files


def main():
    # _, password, action, directory = "John Doe", "password", "e", "./data"

    username, password, action, selected_files = init_program()
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
