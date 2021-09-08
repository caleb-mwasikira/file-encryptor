from pathlib import Path


HOME_DIR = Path.home()


def ROOT_DIR() -> Path:
    return Path(__file__).parent