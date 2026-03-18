from src.config_loader import load_config
from src.ingestion.log_reader import load_service_logs
from src.processing.log_parser import parse_logs
from src.analysis.log_analysis import convert_to_dataframe, get_metric_thresholds
import pandas as pd


def run_pipeline(service: str) -> pd.DataFrame:
    """Orchestrates the functions call to process the raw log files and convert them to a pandas dataframe.

    Args:
        service: name of the service to process.

    Returns:
        Dataframe of all the logs for the service."""

    raw_data = load_config()
    raw_logs = load_service_logs(service)
    parsed_logs = parse_logs(raw_logs)
    logs_dataframe = convert_to_dataframe(parsed_logs, raw_data["columns"])

    get_metric_thresholds(logs_dataframe, "cpu", raw_data["metric_thresholds"])
    get_metric_thresholds(logs_dataframe, "mem", raw_data["metric_thresholds"])
    return logs_dataframe


if __name__ == "__main__":
    print(run_pipeline("booking"))
