import os
from pathlib import Path
from typing import List

from utils.urls import root_dir


class FileManager:
    def __init__(self, current_dir: Path = None) -> None:
        self.current_dir: Path = current_dir or root_dir()

    @staticmethod
    def list_dir_recursive(_path: Path) -> List[Path]:
        dir_list: list = []

        if _path.is_file():
            dir_list.append(_path)

        else:
            for root, dirs, files in os.walk(_path, topdown=True):
                _root = Path(root)

                for file in files:
                    dir_list.append(Path.joinpath(_root, file))

                for dir_name in dirs:
                    dir_list.append(Path.joinpath(_root, dir_name))

        return dir_list

    @staticmethod
    def list_dir(_path: Path) -> List[Path]:
        # dir_list: list = []
        # for posix_path in _path.iterdir():
        #     dir_list.append(posix_path)
        #
        # return dir_list

        return [posix_path for posix_path in _path.iterdir()]

    @staticmethod
    def list_files_in_dir(_path: Path) -> List[Path]:
        # files_in_dir: list = []
        # for posix_path in _path.iterdir():
        #     if posix_path.is_file():
        #         files_in_dir.append(posix_path)
        #     else:
        #         pass
        # return files_in_dir

        return [posix_path for posix_path in _path.iterdir() if posix_path.is_file()]

    @staticmethod
    def is_empty(_path: Path) -> bool:
        dir_list: list = FileManager.list_dir(_path)
        return dir_list.__len__() == 0
