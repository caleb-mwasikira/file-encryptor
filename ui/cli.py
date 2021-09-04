import inquirer
from os import path
from inquirer import errors

from utils.file_manager import FileManager


class CLI:
    """
        CLI class short for (command line interface) is responsible for
        asking end user questions, parsing, validating answers,
        managing hierarchical prompts and providing error feedback
        for our file encryption program.
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_user_auth_info() -> (str, str):
        """This section asks for the users username and password"""

        def validate_username(_, _username):
            if len(_username) < 4:
                raise errors.ValidationError('', reason="Username too short")

            return True

        def validate_password(_, _password):
            if len(_password) < 6:
                raise errors.ValidationError('', reason="Password too short")

            return True

        questions = [
            inquirer.Text(
                'username', message="Please enter your username",
                validate=validate_username
            ),
            inquirer.Password(
                "password", message="Please enter your password",
                validate=validate_password
            )
        ]
        answers: dict = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        username, password = answers.values()

        return username, password

    @staticmethod
    def get_user_action() -> str:
        """Asks the user the action they want executed by the program"""
        qst = [
            inquirer.List(
                "action", message="What do you want to do?",
                choices=['Encrypt', 'Decrypt']
            )
        ]
        answer: dict = inquirer.prompt(qst, raise_keyboard_interrupt=True)

        return answer['action']

    @staticmethod
    def get_dir(action: str):
        def validate_dir(_, directory):
            files_found: list = FileManager.list_dir(directory)

            if not path.exists(directory):
                raise errors.ValidationError('', reason=f"Directory {directory} does not exist")

            elif len(files_found) == 0:
                raise errors.ValidationError('', reason=f"Empty directory")

            else:
                return True

        qst = [
            inquirer.Path(
                "filepath", message=f"Enter the directory you want to {action}",
                normalize_to_absolute_path=True, validate=validate_dir
            )
        ]
        answer: dict = inquirer.prompt(qst, raise_keyboard_interrupt=True)

        return answer['filepath']

    @staticmethod
    def select_files_in_dir(directory):
        """Gets the files the user would like to encrypt/decrypt"""

        files_found: list = FileManager.list_dir(directory)
        default_choice = ['SelectAll']

        qst = [
            inquirer.Checkbox(
                "selected_files",
                message="Press [right arrow key] select file, [left arrow key] deselect file",
                choices=default_choice + files_found,
                default=[]
            )
        ]
        answer = inquirer.prompt(qst, raise_keyboard_interrupt=True)
        selected_files = answer['selected_files']

        if selected_files == default_choice:
            selected_files = files_found

        return selected_files
