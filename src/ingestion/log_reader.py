from pathlib import Path
from collections.abc import Iterator


def load_all_logs(path: str) -> Iterator[str]:
    """Loads all the logs in the given path.

    Args:
        path: Name of the path where the logs are located.

    Returns:
        Returns a generator containing all the log lines.
    """
    log_paths = _load_path(path)
    log_files = _load_all_files(log_paths)

    for log_file in log_files:
        with log_file.open("r", errors="ignore") as file:
            for line in file:
                yield line


def _load_path(path: str) -> Path:
    """Construct the path where the logs are located.

    Args:
        path: from config file, where logs are located

    Returns:
        Path object with the path for logs.

    Raises:
        ValueError: When the path does not exist.
    """

    root_path = Path(__file__).parents[2]
    log_file_path = (root_path / path).resolve()

    if not log_file_path.is_dir():
        raise ValueError("The log path provided in config file is not valid")

    return log_file_path


def _load_all_files(path: Path) -> list[Path]:
    """Loads all file names.

    Args:
        path: path where logs are located.

    Returns:
        All file names.

    Raises:
        ValueError: When the log dir is empty.
    """

    log_files = []

    for file in path.iterdir():
        if not file.is_file():
            continue
        log_files.append(file)

    if not log_files:
        raise ValueError("The log path is empty")

    log_files.sort()

    return log_files
