from pathlib import Path


HOME_DIR = Path.home()


def root_dir() -> Path:
    return Path(__file__).parent.parent
