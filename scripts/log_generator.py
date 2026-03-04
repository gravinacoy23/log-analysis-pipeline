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


def build_log_line():
    timestamp = generate_timestamp()
    service = generate_service()
    message = generate_message(service)
    log = f'{timestamp} service={service} user={random.randint(1,100)} cpu={random.randint(30,70)} mem={random.randint(40,75)} response={random.randint(200,900)} level={random.choice(MESSAGE_TYPE)} msg="{message}"'
    directory = make_directory()

    write_log(directory, service, log)


if __name__ == "__main__":
    for _ in range(5):
        build_log_line()
