from datetime import datetime, UTC
from pathlib import Path
import random
import yaml
import argparse


def _load_config():
    parent_path = Path(__file__).resolve().parents[1]
    config_file = parent_path / "config" / "config.yaml"

    with config_file.open("r") as f:
        data = yaml.safe_load(f)

        if (
            not data.get("services")
            or not data.get("messages")
            or not data.get("levels")
        ):
            raise ValueError(
                "One or more of your constant variables in the config file is empty or doesn't exist"
            )

        return data


def _generate_log_timestamp():
    return datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _generate_runtimestamp():
    return datetime.now(tz=UTC).strftime("%Y%m%d_%H%M%S")


def _generate_service(services):
    return random.choice(services)


def _generate_message(service, message_list):
    service_messages = message_list[service]
    return random.choice(service_messages)


def _make_raw_directory():
    parent_path = Path(__file__).resolve().parents[1]
    dynamic_dir = parent_path / "data" / "raw"
    dynamic_dir.mkdir(parents=True, exist_ok=True)

    return dynamic_dir


def _make_service_directories(raw_dir, services):
    for service in services:
        service_dir = raw_dir / service
        service_dir.mkdir(parents=True, exist_ok=True)


def _create_files(services, target_path, run_timestamp):
    file_handles = dict()
    for service in services:
        log_file = target_path / service / f"{service}_{run_timestamp}.log"
        handler = log_file.open("a", encoding="utf-8")

        file_handles[service] = handler

    return file_handles


def _close_files(file_handles):
    for handle in file_handles.values():
        handle.close()


def _write_log(file_handles, service, log_line):
    handle = file_handles[service]

    handle.write(log_line + "\n")


def _format_log(timestamp, service, user, cpu, memory, response_time, level, message):
    return f'timestamp={timestamp} service={service} user={user} cpu={cpu} mem={memory} response_time={response_time} level={level} msg="{message}"'


def _generate_user():
    return random.randint(1, 100)


def _generate_memory():
    return random.randint(40, 75)


def _generate_cpu():
    return random.randint(30, 70)


def _generate_response_time(cpu):
    if cpu < 50:
        return random.randint(200, 500)
    elif 50 <= cpu < 70:
        return random.randint(501, 800)
    else:
        return random.randint(801, 1200)


def _determine_level(response_time, levels):
    if response_time < 600:
        level = random.choices(levels, weights=[1, 0, 0])
        return level[0]
    elif 600 <= response_time < 900:
        level = random.choices(levels, weights=[0.8, 0.2, 0])
        return level[0]
    else:
        level = random.choices(levels, weights=[0, 0.5, 0.5])
        return level[0]


def _generator_loop(iterations, raw_data, file_handles):
    services = raw_data["services"]
    levels = raw_data["levels"]
    messages = raw_data["messages"]

    for _ in range(iterations):
        timestamp = _generate_log_timestamp()
        service = _generate_service(services)
        message = _generate_message(service, messages)
        user = _generate_user()
        memory = _generate_memory()
        cpu = _generate_cpu()
        response_time = _generate_response_time(cpu)
        level = _determine_level(response_time, levels)
        log = _format_log(
            timestamp, service, user, cpu, memory, response_time, level, message
        )
        _write_log(file_handles, service, log)


def generate_logs(iterations):
    directory = _make_raw_directory()
    run_timestamp = _generate_runtimestamp()
    raw_data = _load_config()
    _make_service_directories(directory, raw_data["services"])
    file_handles = _create_files(raw_data["services"], directory, run_timestamp)

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
