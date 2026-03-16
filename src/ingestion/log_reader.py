from pathlib import Path
from collections.abc import Iterator


def load_service_logs(service: str) -> Iterator[str]:
    """Loads the service logs in a raw format for the parser.

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


if __name__ == "__main__":
    log = load_service_logs("booking")

    print(log)
