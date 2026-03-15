from pathlib import Path


def load_service_logs(service):
    root_path = Path(__file__).resolve().parents[2]
    log_path = root_path / "data" / "raw" / service

    if not log_path.is_dir():
        raise ValueError(f"The service {service} does not exist")

    log_files = [file for file in log_path.iterdir() if file.is_file()]
    log_files.sort()

    if not log_files:
        raise FileNotFoundError(f"There are no logs for {service}")

    with log_files[0].open("r") as file:
        for line in file:
            yield line


if __name__ == "__main__":
    log = load_service_logs("booking")
