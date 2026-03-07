from datetime import datetime, UTC
from pathlib import Path
import random
import yaml


def load_config():
    parent_path = Path(__file__).resolve().parents[1]
    config_file = parent_path / "config" / "config.yaml"

    with config_file.open("r") as f:
        data = yaml.safe_load(f)
        services = data.get("services")
        messages = data.get("messages")
        message_type = data.get("message_type")

        if not services or not messages or not message_type:
            raise ValueError(
                "One or more of your constant variables in the config file is empty or doesn't exist"
            )

        return services, messages, message_type


def generate_log_timestamp():
    return datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def generate_runtimestamp():
    return datetime.now(tz=UTC).strftime("%Y%m%d_%H%M%S")


def generate_service(services):
    return random.choice(services)


def generate_message(service, message_list):
    service_messages = message_list[service]
    return random.choice(service_messages)


def make_raw_directory():
    parent_path = Path(__file__).resolve().parents[1]
    dynamic_dir = parent_path / "data" / "raw"
    dynamic_dir.mkdir(parents=True, exist_ok=True)

    return dynamic_dir


def make_service_directories(raw_dir, services):
    for service in services:
        service_dir = raw_dir / service
        service_dir.mkdir(parents=True, exist_ok=True)


def write_log(target_path, service, run_timestamp, log_line):
    log_file = target_path / service / f"{service}_{run_timestamp}.log"

    with log_file.open("a", encoding="utf-8") as f:
        f.write(log_line + "\n")


def format_log(timestamp, service, user, cpu, memory, response_time, level, message):
    return f'{timestamp} service={service} user={user} cpu={cpu} mem={memory} response_time={response_time} level={level} msg="{message}"'


def generate_user():
    return random.randint(1, 100)


def generate_memory():
    return random.randint(40, 75)


def generate_cpu():
    return random.randint(30, 70)


def generate_response_time(cpu):
    if cpu < 50:
        return random.randint(200, 500)
    elif 50 <= cpu < 70:
        return random.randint(501, 800)
    else:
        return random.randint(801, 1200)


def determine_level(response_time, messages):
    if response_time < 600:
        level = random.choices(messages, weights=[1, 0, 0])
        return level[0]
    elif 600 <= response_time < 900:
        level = random.choices(messages, weights=[0.8, 0.2, 0])
        return level[0]
    else:
        level = random.choices(messages, weights=[0, 0.5, 0.5])
        return level[0]


def generate_logs(iterations):
    directory = make_raw_directory()
    run_timestamp = generate_runtimestamp()
    services, messages, message_type = load_config()
    make_service_directories(directory, services)

    for _ in range(iterations):
        timestamp = generate_log_timestamp()
        service = generate_service(services)
        message = generate_message(service, messages)
        user = generate_user()
        memory = generate_memory()
        cpu = generate_cpu()
        response_time = generate_response_time(cpu)
        level = determine_level(response_time, message_type)
        log = format_log(
            timestamp, service, user, cpu, memory, response_time, level, message
        )
        write_log(directory, service, run_timestamp, log)


if __name__ == "__main__":
    generate_logs(100)
