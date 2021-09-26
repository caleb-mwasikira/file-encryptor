import pytest
from typing import List
from pathlib import Path

from utils.utils import ROOT_DIR
from utils.file_manager import FileManager

test_dir: Path = Path.joinpath(ROOT_DIR(), "data")


@pytest.fixture
def recursive_dir_list() -> List[Path]:
    dir_list = [
        "empty_dir",
        "nested_dir",
        "nested_dir/deeply_nested_dir",
        "nested_dir/deeply_nested_dir/deeply_nested_file.txt",
        "nested_dir/nested_file.txt",
        "nested_dir/nested_file_2.txt",
        "data.txt",
        "evil.txt"
    ]
    return list(map(lambda _dir: Path.joinpath(test_dir, _dir), dir_list))


@pytest.fixture
def dir_list() -> List[Path]:
    dir_list = [
        "empty_dir",
        "nested_dir",
        "data.txt",
        "evil.txt",
    ]
    return [Path.joinpath(test_dir, _dir) for _dir in dir_list]


def test_list_dir_recursive(recursive_dir_list):
    file_manager = FileManager()

    actual_recursive_dir_list = file_manager.list_dir_recursive(test_dir)
    assert set(actual_recursive_dir_list) == set(recursive_dir_list)


def test_list_dir(dir_list):
    file_manager = FileManager()

    actual_dir_list = file_manager.list_dir(test_dir)
    assert set(actual_dir_list) == set(dir_list)


def test_list_files_in_dir(dir_list):
    file_manager = FileManager()

    expected_files_in_dir = set(filter(lambda _dir: Path(_dir).is_file(), dir_list))
    actual_files_in_dir = file_manager.list_files_in_dir(test_dir)

    assert set(actual_files_in_dir) == set(expected_files_in_dir)
