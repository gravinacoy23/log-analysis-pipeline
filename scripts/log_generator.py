from datetime import datetime, UTC
import random
import os

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


def build_log_line():
    timestamp = generate_timestamp()
    service = generate_service()
    message = generate_message(service)
    return f'{timestamp} service={service} user={random.randint(1,100)} cpu={random.randint(30,70)} mem={random.randint(40,75)} response={random.randint(200,900)} level={random.choice(MESSAGE_TYPE)} msg="{message}"'


def make_directory(base_route):
    new_dir = "data/raw"
    joint_route = os.path.join(base_route, new_dir)

    if not os.path.exists(joint_route):
        os.makedirs(joint_route)

    return joint_route


if __name__ == "__main__":
    for _ in range(5):
        print(build_log_line())

    print(make_directory("/home/gravinacoy23/logs-analysis-pipeline/"))
