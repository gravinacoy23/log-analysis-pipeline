import argparse
import logging
from pipelines.run_pipeline import run_pipeline


def main(service_name):
    return run_pipeline(service_name)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    parser = argparse.ArgumentParser(
        prog="Main file for the log-analysis pipeline",
        description="File with the main funcion that calls pipelines",
    )
    parser.add_argument(
        "-s",
        "--service",
        type=str,
        default="booking",
        help="Name of the service you wanna analyze",
    )
    arguments = parser.parse_args()
    service_name = arguments.service

    print(main(service_name))
