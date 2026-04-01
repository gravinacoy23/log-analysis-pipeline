from datetime import datetime, UTC
from pathlib import Path
from typing import Any
from io import TextIOWrapper
import random
import yaml
import argparse


def _load_config() -> dict[str, Any]:
    """Load constant variables from the config file.

    Returns:
        Dictionary with all config data for the auxiliary functions.

    Raises:
        ValueError: If the config file is missing at least one of the required keys.
    """

    parent_path = Path(__file__).resolve().parents[1]
    config_file = parent_path / "config" / "config.yaml"

    with config_file.open("r") as f:
        data = yaml.safe_load(f)

        if not data.get("service") or not data.get("messages") or not data.get("level"):
            raise ValueError(
                "One or more of your constant variables in the config file is empty or doesn't exist"
            )

        return data


def _generate_log_timestamp() -> str:
    """Generate the timestamp for the log.

    Returns:
        String with the current date time in GMT time.
    """

    return datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _generate_runtimestamp() -> str:
    """Generate the run timestamp for the name of the file.

    Returns:
        String with the current date time in GMT time.
    """

    return datetime.now(tz=UTC).strftime("%Y%m%d_%H%M%S")


def _generate_service(services: list[str]) -> str:
    """Chooses a random service for the log.

    Args:
        services: List with all the services available.

    Returns:
        A random choice from the list.
    """

    return random.choice(services)


def _generate_message(service: str, message_list: dict[str, list[str]]) -> str:
    """Generates a message available for the given service.

    Args:
        service: A string with the name of the service.
        message_list: A dictionary that matches all the services with the available messages.

    Returns:
        A random choice for the available services.
    """

    service_messages = message_list[service]
    return random.choice(service_messages)


def _make_raw_directory() -> Path:
    """Makes the directory in which we are going to save the service logs.

    Returns:
        Path object with the path to the directory for the .log files.
    """

    parent_path = Path(__file__).resolve().parents[1]
    dynamic_dir = parent_path / "data" / "raw"
    dynamic_dir.mkdir(parents=True, exist_ok=True)

    return dynamic_dir


def _make_service_directories(raw_dir: Path, services: list[str]) -> None:
    """Makes a dedicated directory for each service.

    Args:
        raw_dir: Directory in which we are saving the new dirs.
        services: Contains the name of all the services.
    """

    for service in services:
        service_dir = raw_dir / service
        service_dir.mkdir(parents=True, exist_ok=True)


def _create_files(
    services: list[str], target_path: Path, run_timestamp: str
) -> dict[str, TextIOWrapper]:
    """Creates the files for each service in the dedicated service path and
    opens it.

    Args:
        services: All the available services
        target_path: raw directory where all service directories are
        run_timestamp: timestamp where all the files got generated

    Returns:
        A dict that matches the name of the service with the corresponding file handle.
    """

    file_handles = dict()
    for service in services:
        log_file = target_path / service / f"{service}_{run_timestamp}.log"
        handler = log_file.open("a", encoding="utf-8")

        file_handles[service] = handler

    return file_handles


def _close_files(file_handles: dict[str, TextIOWrapper]) -> None:
    """Closes all the files at the end of the execution.

    Args:
        file_handles: Dict that matches the name of the service with the corresponding handle.
    """

    for handle in file_handles.values():
        handle.close()


def _write_log(
    file_handles: dict[str, TextIOWrapper], service: str, log_line: str
) -> None:
    """Writes the log line in the corresponding file.

    Args:
        file_handles: Dict that matches the name of the service with the corresponding handle.
        service: Name of the service
        log_line: formatted log line ready to go into the .log file
    """

    handle = file_handles[service]

    handle.write(log_line + "\n")


def _format_log(
    timestamp: str,
    service: str,
    user: int,
    cpu: int,
    memory: int,
    response_time: int,
    level: str,
    message: str,
) -> str:
    """Formats the log line with all the required fields.

    Args:
        timestamp: timestamp when the log got generated
        service: from which service is this log
        user: user in the log
        cpu: cpu usage at the time
        memory: mem usage at the time
        response_time: response time
        level: info warning or error
        message: message for the log

    Returns:
        Complete formatted log line, ready to append to the .log file
    """

    return f'timestamp={timestamp} service={service} user={user} cpu={cpu} mem={memory} response_time={response_time} level={level} msg="{message}"'


def _generate_user() -> int:
    """Generate a random user.

    Returns:
        Random int between 1 and 100.
    """

    return random.randint(1, 100)


def _generate_memory() -> int:
    """Generate a random memory usage.

    Returns:
        Random int between 40 and 75.
    """

    return random.randint(40, 75)


def _generate_cpu() -> int:
    """Generate random CPU usage.

    Returns:
        Random int between 30 and 70.
    """

    return random.randint(30, 70)


def _generate_response_time(
    cpu: int, mem: int, thresholds: dict[str, dict[str, int]]
) -> int:
    """Generate the response time based on the CPU and memory usage.

    Args:
        cpu: CPU usage for the given log.
        mem: mem usage for the given log.
        thresholds: buckets for each metric.

    Returns:
        Random integer, range varies depending on the CPU or mem usage.
    """

    cpu_thres = thresholds["cpu"]
    mem_thres = thresholds["mem"]

    if cpu > cpu_thres["normal"] or mem > mem_thres["normal"]:
        return random.randint(801, 1200)

    elif (
        cpu_thres["low"] < cpu <= cpu_thres["normal"]
        or mem_thres["low"] < mem <= mem_thres["normal"]
    ):
        return random.randint(501, 800)
    else:
        return random.randint(200, 500)


def _determine_level(response_time: int, levels: list[str]) -> str:
    """Determine the level for the log based on the response time.

    Args:
        response_time: Response time for the log
        levels: all the available levels

    Returns:
        Level for the log depending on the response time
    """

    if response_time < 600:
        level = random.choices(levels, weights=[1, 0, 0])
        return level[0]
    elif 600 <= response_time < 900:
        level = random.choices(levels, weights=[0.8, 0.2, 0])
        return level[0]
    else:
        level = random.choices(levels, weights=[0, 0.5, 0.5])
        return level[0]


def _generator_loop(
    iterations: int, raw_data: dict[str, Any], file_handles: dict[str, TextIOWrapper]
) -> None:
    """Generates all the log lines for a given number of times and calls the
    corresponding auxiliary functions to generate format and write the log.

    Args:
        iterations: Number of logs to be generated.
        raw_data: contains all the data from the config file
        file_handles: matches the name of a given service with the file handle
    """

    services = raw_data["service"]
    levels = raw_data["level"]
    messages = raw_data["messages"]

    for _ in range(iterations):
        timestamp = _generate_log_timestamp()
        service = _generate_service(services)
        message = _generate_message(service, messages)
        user = _generate_user()
        memory = _generate_memory()
        cpu = _generate_cpu()
        response_time = _generate_response_time(
            cpu, memory, raw_data["metric_thresholds"]
        )
        level = _determine_level(response_time, levels)
        log = _format_log(
            timestamp, service, user, cpu, memory, response_time, level, message
        )
        _write_log(file_handles, service, log)


def generate_logs(iterations: int) -> None:
    """Orchestrates the log generation calling auxiliary functions to generate
    the data needed for the loop that generates the logs.

    Args:
        iterations: number of logs you are generating
    """

    directory = _make_raw_directory()
    run_timestamp = _generate_runtimestamp()
    raw_data = _load_config()
    _make_service_directories(directory, raw_data["service"])
    file_handles = _create_files(raw_data["service"], directory, run_timestamp)

    _generator_loop(iterations, raw_data, file_handles)

    _close_files(file_handles)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Log generator",
        description="Program to generate airline shopping, pricing and booking logs",
    )
    parser.add_argument(
        "-c", "--count", type=int, default=1, help="number of logs you wanna generate"
    )
    arguments = parser.parse_args()
    number_of_logs = arguments.count

    generate_logs(number_of_logs)
