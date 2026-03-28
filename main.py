import argparse
import logging
import pandas as pd
from src.config_loader import load_config
from pipelines.run_pipeline import run_pipeline
from pipelines.run_reporting_pipeline import report_pipeline


def main(service_name: str) -> pd.DataFrame:
    """Orchestrates all the configuration needed for the data pipelines.

    Args:
        service_name: name of the service to run the pipeline on

    Returns:
        Parsed logs dataframe
    """

    config_data = load_config()

    logs_dataframe = run_pipeline(service_name, config_data)
    report_pipeline(logs_dataframe)

    return logs_dataframe


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
