import inquirer
from typing import List, Tuple
from pathlib import Path
from inquirer import errors

from utils.file_manager import FileManager
from utils.file_selection_options import FileSelectionOptions
from utils.user_actions import UserActions
from utils.urls import HOME_DIR


class CommandLineInterface:
    """
        CommandLineInterface class is responsible for asking end user questions,
        parsing, validating answers, managing hierarchical prompts
        and providing error feedback for our file encryption program.
    """

    def __init__(self) -> None:
        self.selected_files: List[Path] = []

    @staticmethod
    def get_username() -> str:
        def validate_username(_, _username):
            if len(_username) < 4:
                raise errors.ValidationError('', reason="Username too short")

            return True

        qst = [
            inquirer.Text(
                'username', message="Enter your username",
                validate=validate_username
            )
        ]
        answers: dict = inquirer.prompt(qst, raise_keyboard_interrupt=True)
        return answers['username']

    @staticmethod
    def get_password() -> str:
        password = None

        def validate_password(_, _password):
            if len(_password) < 6:
                raise errors.ValidationError('', reason="Password too short")
            return True

        def validate_password_confirm(_, confirmation_password):
            if password != confirmation_password:
                raise errors.ValidationError('', reason="Confirm password and password must be identical")
            return True

        qst = [
            inquirer.Password(
                "password", message="Enter your password",
                validate=validate_password
            ),
        ]
        answer: dict = inquirer.prompt(qst)
        password = answer['password']

        inquirer.prompt([
            inquirer.Password(
                "password_confirm", message="Confirm Password",
                validate=validate_password_confirm
            )
        ])
        return password

    def get_user_auth_info(self) -> Tuple[str, str]:
        return self.get_username(), self.get_password()

    @staticmethod
    def get_user_action() -> UserActions:
        """Asks the user the action they want executed by the program"""
        qst = [
            inquirer.List(
                "user_action", message="What do you want to do?",
                choices=['Encrypt', 'Decrypt']
            )
        ]
        answer: dict = inquirer.prompt(qst, raise_keyboard_interrupt=True)
        user_action: str = answer['user_action']

        if user_action.lower() == UserActions.ENCRYPT.value:
            return UserActions.ENCRYPT

        else:
            return UserActions.DECRYPT

    @staticmethod
    def select_dir() -> Path:
        def validate_dir(_, directory: str):
            _dir: Path = Path(directory)

            if not _dir.exists():
                raise errors.ValidationError('', reason=f"Directory {_dir.__str__()} does not exist")

            elif FileManager.is_empty(_dir):
                raise errors.ValidationError('', reason="Empty directory")

            else:
                return True

        qst = [
            inquirer.Path(
                "selected_dir", message="Where are the files located?",
                normalize_to_absolute_path=True, validate=validate_dir,
                default=HOME_DIR.__str__()
            )
        ]
        answer: dict = inquirer.prompt(qst, raise_keyboard_interrupt=True)
        return Path(answer['selected_dir'])

    def select_files_in_dir(self, directory: Path) -> List[Path]:
        dir_list: List[Path] = FileManager.list_dir(directory)
        files_in_dir: List[Path] = FileManager.list_files_in_dir(directory)

        default_choice = [(option.value, option.name) for option in FileSelectionOptions]

        num_of_files: int = len(files_in_dir)
        num_of_folders: int = len(dir_list) - num_of_files

        qst = [
            inquirer.Checkbox(
                "selected_files",
                message=f"Found {num_of_files} file(s) and {num_of_folders} folder(s) in directory: {directory.name}",
                choices=default_choice + [(_dir.name, _dir.__str__()) for _dir in dir_list],
                default=[]
            ),
        ]
        answer: dict = inquirer.prompt(qst, raise_keyboard_interrupt=True)
        selected: list = answer['selected_files']

        if FileSelectionOptions.DIR_FILES.name in selected:
            self.selected_files.extend(files_in_dir)

        elif FileSelectionOptions.ALL_FILES.name in selected:
            dir_list_recursive: List[Path] = FileManager.list_dir_recursive(directory)
            all_files_in_dir: List[Path] = [_dir for _dir in dir_list_recursive if _dir.is_file()]
            self.selected_files.extend(all_files_in_dir)

        elif FileSelectionOptions.PREV_DIR.name in selected:
            self.select_files_in_dir(directory.parent)

        else:
            for select in selected:
                _dir = Path(select)

                if _dir.is_file():
                    self.selected_files.append(_dir)

                else:
                    if not FileManager.is_empty(_dir):
                        self.select_files_in_dir(_dir)

        return self.selected_files

