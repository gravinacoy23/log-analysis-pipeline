from typing import Any
from src.ingestion.log_reader import load_all_logs
from src.processing.log_parser import parse_logs
from src.analysis.log_analysis import convert_to_dataframe, get_metric_thresholds
import pandas as pd


def run_pipeline(raw_data: dict[str, Any]) -> pd.DataFrame:
    """Orchestrates the functions call to process the raw log files and convert
    them to a pandas dataframe.

    Args:
        raw_data: raw data loaded from the config file.

    Returns:
        Dataframe of all the logs for the service.
    """

    raw_logs = load_all_logs(raw_data["paths"]["raw_log"])
    expected_columns = raw_data["columns"]
    expected_values = raw_data["expected_values"]

    parsed_logs, parse_stats = parse_logs(raw_logs, list(expected_columns.keys()))

    logs_dataframe = convert_to_dataframe(
        parsed_logs, expected_columns, expected_values
    )

    return logs_dataframe
