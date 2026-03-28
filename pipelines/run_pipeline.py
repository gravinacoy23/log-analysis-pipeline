from typing import Any
from src.ingestion.log_reader import load_service_logs
from src.processing.log_parser import parse_logs
from src.analysis.log_analysis import convert_to_dataframe, get_metric_thresholds
import pandas as pd


def run_pipeline(service: str, raw_data: dict[str, Any]) -> pd.DataFrame:
    """
    Orchestrates the functions call to process the raw log files and convert
    them to a pandas dataframe.

    Args:
        service: name of the service to process.
        raw_data: raw data loaded from the config file.

    Returns:
        Dataframe of all the logs for the service.
    """

    raw_logs = load_service_logs(service)
    expected_columns = raw_data["columns"]
    expected_values = {
        "service": raw_data["service"],
        "level": raw_data["level"],
    }

    parsed_logs, parse_stats = parse_logs(raw_logs, list(expected_columns.keys()))
    logs_dataframe = convert_to_dataframe(
        parsed_logs, expected_columns, expected_values
    )

    get_metric_thresholds(logs_dataframe, "cpu", raw_data["metric_thresholds"])
    get_metric_thresholds(logs_dataframe, "mem", raw_data["metric_thresholds"])
    return logs_dataframe
