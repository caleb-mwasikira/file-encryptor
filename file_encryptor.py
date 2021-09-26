#!/usr/bin/env python
import sys
import argparse
import colorama as colors
from pathlib import Path
from pyfiglet import Figlet, FigletString
from typing import Tuple, List, Optional

from ui.command_line_interface import CommandLineInterface
from encryption.fernet_encryptor import FernetEncryptor
from utils.user_actions import UserActions


def get_program_args() -> Tuple[Optional[UserActions], str, List[str]]:
    user_action: Optional[UserActions] = None

    parser = argparse.ArgumentParser(
        allow_abbrev=False,
        description='A tool for encrypting and decrypting files'
    )
    parser.version = "1.0.0"

    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument('--encrypt', action="store_true", help="runs the program in encrypt mode")
    action_group.add_argument('--decrypt', action="store_true", help="runs the program in decrypt mode")

    parser.add_argument('-d', '--dir', action="store",
                        help="Directory containing the files to encrypt or decrypt")
    parser.add_argument('-f', '--files', action="store", nargs="+",
                        help="Files to encrypt or decrypt")

    parser.add_argument('-v', '--version', action='version')

    args = parser.parse_args()

    if args.encrypt:
        user_action = UserActions.ENCRYPT

    elif args.decrypt:
        user_action = UserActions.DECRYPT

    return user_action, args.dir, args.files


def start_screen(display_text: str):
    f = Figlet(font="larry3d")
    figlet_string: FigletString = f.renderText(display_text)
    print(f"{colors.Fore.GREEN} {figlet_string} {colors.Style.RESET_ALL}")

    print("Welcome to the file encryptor version 1.0.0")


def init_program() -> Tuple[str, UserActions, List[Path]]:
    try:
        start_screen("Guizzer")

        # username, password = "John Doe", "password"

        CLI = CommandLineInterface()
        action, directory, files = get_program_args()

        action = action or CLI.get_user_action()
        directory = directory or CLI.select_dir()

        selected_files: List[Path] = CLI.select_files_in_dir(Path(directory))

        if files is not None:
            for file in files:
                filepath: Path = Path(file)

                if filepath.exists():
                    selected_files.append(filepath.absolute())

            # selected_files.extend([Path(file).absolute() for file in files if Path(file).exists()])

        # username: str = CLI.get_username()
        password: str = CLI.get_password()
        return password, action, selected_files

    except KeyboardInterrupt:
        print("Cancelled by user")
        sys.exit(1)


def main():
    password, action, selected_files = init_program()
    encryptor = FernetEncryptor(password)

    for file in selected_files:
        if action == UserActions.ENCRYPT:
            encryptor.encrypt_file(file)

        else:
            encryptor.decrypt_file(file)


if __name__ == "__main__":
    main()
