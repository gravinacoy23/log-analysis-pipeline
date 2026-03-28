from pathlib import Path
from collections.abc import Iterator


def load_service_logs(service: str) -> Iterator[str]:
    """
    Loads the service logs in a raw format for the parser.

    Args:
        service: Name of the service you want to read/load the logs from.

    Returns:
        Returns a generator containing all the log lines.

    Raises:
        ValueError: When the directory for the requested service does not exist.
        FileNotFoundError: When the file for the given service does not exist
    """

    root_path = Path(__file__).resolve().parents[2]
    log_path = root_path / "data" / "raw" / service

    if not log_path.is_dir():
        raise ValueError(f"The service {service} does not exist")

    log_files = [file for file in log_path.iterdir() if file.is_file()]
    log_files.sort()

    if not log_files:
        raise FileNotFoundError(f"There are no logs for {service}")

    for log_file in log_files:
        with log_file.open("r") as file:
            for line in file:
                yield line


def load_all_logs(services: list[str]) -> Iterator[str]:
    """
    Loads the all the logs in the services dirs.

    Args:
        services: Names of all the services.

    Returns:
        Returns a generator containing all the log lines.
    """
    log_paths = _load_all_path_names(services)
    log_files = _load_all_files(log_paths)
    for log_file in log_files:
        with log_file.open("r") as file:
            for line in file:
                yield line


def _load_all_path_names(services: list[str]) -> list[Path]:
    """
    Loads all the service paths.

    Args:
        services: Names of all the services

    Returns:
        All the paths for the files
    """

    root_path = Path(__file__).resolve().parents[2]
    paths = list()

    for service in services:
        paths.append(root_path / "data" / "raw" / service)

    return paths


def _load_all_files(paths: list[Path]) -> list[Path]:
    """
    Loads all file names.

    Args:
        paths: all the path names.

    Returns:
        All file names.
    """

    log_files = list()
    for path in paths:
        for file in path.iterdir():
            if file.is_file():
                log_files.append(file)

    log_files.sort()

    return log_files
