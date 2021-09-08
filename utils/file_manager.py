from pathlib import Path
from os import walk

from utils.utils import ROOT_DIR


class FileManager:
    def __init__(self, current_dir: Path = None) -> None:
        self.current_dir: Path = current_dir or ROOT_DIR()

    @staticmethod
    def list_dir_recursive(_path: Path) -> set:
        dir_list: list = []

        if _path.is_file():
            dir_list.append(_path.__str__())

        else:
            for root, dirs, files in walk(_path, topdown=True):
                root_dir = Path(root)

                for file in files:
                    dir_list.append(Path.joinpath(root_dir, file).__str__())

                for dir_name in dirs:
                    dir_list.append(Path.joinpath(root_dir, dir_name).__str__())

        return set(dir_list)

    @staticmethod
    def list_dir(_path: Path) -> set:
        # dir_list: list = []
        # for posix_path in _path.iterdir():
        #     dir_list.append(posix_path.__str__())
        #
        # return set(dir_list)

        return set([posix_path.__str__() for posix_path in _path.iterdir()])

    @staticmethod
    def list_files_in_dir(_path: Path) -> set:
        # files_in_dir: list = []
        # for posix_path in _path.iterdir():
        #     if posix_path.is_file():
        #         files_in_dir.append(posix_path.__str__())
        #     else:
        #         pass
        # return set(files_in_dir)

        return set([posix_path.__str__() for posix_path in _path.iterdir() if posix_path.is_file()])

    @staticmethod
    def is_empty(_path: Path) -> bool:
        dir_list: list = list(FileManager.list_dir(_path))
        return dir_list.__len__() == 0
