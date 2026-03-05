from datetime import datetime, UTC
from pathlib import Path
import random

SERVICES = ["shopping", "pricing", "booking"]

MESSAGES = {
    "shopping": ["FareSearch completed", "AirShopping completed", "No fares available"],
    "pricing": [
        "OfferPrice completed",
        "Dynamic price applied",
        "Fare rules evaluated",
    ],
    "booking": ["Booking confirmed", "Booking failed", "Seat booked"],
}

MESSAGE_TYPE = ["INFO", "WARNING", "ERROR"]


def generate_timestamp():
    return datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def generate_service():
    return random.choice(SERVICES)


def generate_message(service):
    service_messages = MESSAGES[service]
    return random.choice(service_messages)


def make_directory():
    target_path = Path(__file__).resolve().parents[1]
    dynamic_dir = target_path / "data" / "raw"

    dynamic_dir.mkdir(parents=True, exist_ok=True)

    return dynamic_dir


def write_log(target_path, service, log_line):
    file = target_path / f"{service}.log"

    with file.open("a", encoding="utf-8") as f:
        f.write(log_line + "\n")


def format_log(timestamp, service, user, cpu, memory, response, level, message):
    return f'{timestamp} service={service} user={user} cpu={cpu} mem={memory} response={response} level={level} msg="{message}"'


def generate_metrics():
    user = random.randint(1, 100)
    cpu = random.randint(30, 70)
    memory = random.randint(40, 75)
    response = random.randint(200, 900)
    level = random.choice(MESSAGE_TYPE)

    return user, cpu, memory, response, level


def generate_logs(iterations):
    directory = make_directory()
    for _ in range(iterations):
        timestamp = generate_timestamp()
        service = generate_service()
        message = generate_message(service)
        user, cpu, memory, response, level = generate_metrics()
        log = format_log(
            timestamp, service, user, cpu, memory, response, level, message
        )
        write_log(directory, service, log)


if __name__ == "__main__":
    generate_logs(100)
