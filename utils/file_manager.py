from os import path, walk


class FileManager:
    def __init__(self) -> None:
        pass

    @staticmethod
    def list_dir(directory) -> list:
        dir_list = []

        if path.isfile(directory):
            dir_list.append(path.abspath(directory))

        else:
            for root, _, files in walk(directory, topdown=True):
                for file in files:
                    dir_list.append(path.join(root, file))

        return dir_list
