from typing import Any
import pandas as pd
import logging


logger = logging.getLogger(__name__)


def _verify_columns(
    log_dicts: list[dict[str, Any]], expected_columns: list[str]
) -> None:
    """Verifies that the parsed logs are not empty and contain the required columns.

    Args:
        log_dicts: Parsed logs.
        expected_columns: All the required columns loaded from the config file.

    Raises:
        ValueError: When at least one of the required columns is missing, or when the list is empty
    """

    if not log_dicts:
        raise ValueError("The parsed logs list is empty")

    current_columns = log_dicts[0].keys()
    for column_name in expected_columns:
        if column_name not in current_columns:
            raise ValueError(
                f"The required column {column_name} is missing in the parsed logs."
            )


def _verify_col_dtype(
    log_dicts: list[dict[str, Any]], expected_cols: dict[str, str]
) -> list[dict[str, Any]]:
    """Verify all the cols have the correct data type

    Args:
        log_dicts: List of parser logs
        expected_cols: Expected cols with Dtypes from the config file

    Returns:
        List of dicts with all the verified logs, drops the lines that have an incorrect data type.
    """

    _verify_columns(log_dicts, list(expected_cols.keys()))

    int_type_cols = list()
    verified_log_dicts = list()

    for col, data_type in expected_cols.items():
        if data_type == "int":
            int_type_cols.append(col)

    for line_number, log in enumerate(log_dicts, start=1):
        line_verified = True
        for int_col in int_type_cols:
            if not isinstance(log[int_col], int):
                logger.warning(
                    f"The column {int_col} does not contain int data type at line {line_number}"
                )
                line_verified = False
                break

        if line_verified:
            verified_log_dicts.append(log)

    return verified_log_dicts


def convert_to_dataframe(
    log_dicts: list[dict[str, Any]], expected_columns: dict[str, str]
) -> pd.DataFrame:
    """Converts the list of parsed logs into a dataframe.

    Args:
        log_dicts: Parsed logs.
        expected_columns: All the required columns loaded from the config file.

    Returns:
        Logs in a pd.dataframe object."""

    verified_log_dicts = _verify_col_dtype(log_dicts, expected_columns)
    logs_dataframe = pd.DataFrame(verified_log_dicts)

    return logs_dataframe


def convert_corr_matrix(logs_dataframe: pd.DataFrame) -> pd.DataFrame:
    """Converts the numeric type cols to a correlation matrix

    Args:
        logs_dataframe: DF of parsed logs.

    Returns:
        DF of the correlation matrix
    """
    numeric_cols = logs_dataframe.select_dtypes(include="number")

    return numeric_cols.corr("pearson")


def filter_loglevel(logs_dataframe: pd.DataFrame, level: str) -> pd.DataFrame:
    """Filters all the logs that match the input level.

    Args:
        logs_dataframe: DF of parsed logs.
        level: level of the log.

    Returns:
        A new DF with the selected log level
    """

    return logs_dataframe.loc[logs_dataframe["level"] == level]


def select_col(
    logs_dataframe: pd.DataFrame, column_name: str
) -> pd.DataFrame | pd.Series:
    """Selects the required column by name.

    Args:
        logs_dataframe: DF of parsed logs.
        column_name: Name of the column to select

    Returns:
        The intention is for this function to return a series, will return a DF in case there are two cols with the same name
    """

    return logs_dataframe[column_name]


def count_by_level(logs_dataframe: pd.DataFrame, level: str) -> int:
    """Counts the the occurrences of a given log level in the dataframe

    Args:
        logs_dataframe: DF of parsed logs
        level: level of the log

    Returns:
        Amount of occurrences of the given level"""

    return (logs_dataframe["level"] == level).sum()


def count_by_level_all(logs_dataframe: pd.DataFrame) -> pd.Series:
    """Counts the occurrences per level in all the DataFrame

    Args:
        logs_dataframe: DF of parsed logs

    Returns:
        A series with the occurences per level.
    """

    return logs_dataframe.value_counts("level")


def count_by_service(logs_dataframe: pd.DataFrame, service: str) -> int:
    """Counts the occurrences of a given service

    Args:
        logs_dataframe: DF of parsed logs
        service: Name of the service

    Returns:
        Occurences if the given service in the DF
    """

    return (logs_dataframe["service"] == service).sum()


def count_by_service_all(logs_dataframe: pd.DataFrame) -> pd.Series:
    """Counts the number of occurrences of all the services in the DF

    Args:
        logs_dataframe: DF of parsed logs.

    Returns:
        Series with the number of occurences
    """

    return logs_dataframe.value_counts("service")


def mean_rt_by_service(logs_dataframe: pd.DataFrame) -> pd.Series:
    """Calculates the mean response time by service.

    Args:
        logs_dataframe: DF of parsed logs.

    Returns:
        Series with the mean response time per service
    """

    return logs_dataframe.groupby("service")["response_time"].mean()  # type: ignore[return-value]


def mean_cpu_by_level(logs_dataframe: pd.DataFrame) -> pd.Series:
    """Calculates the mean CPU usage by level.

    Args:
        logs_dataframe: DF of parsed logs.

    Returns:
        Series with the mean CPU usage per level.
    """

    return logs_dataframe.groupby("level")["cpu"].mean()  # type: ignore[return-value]


def get_metric_thresholds(
    logs_dataframe: pd.DataFrame,
    metric: str,
    thresholds: dict[str, dict[str, list[int]]],
) -> None:
    """Adds a column that based on predefined thresholds assigns a value of the status of the given metric.

    Args:
        logs_dataframe: DF of parsed logs.
        metric: name of the metric
        Thresholds: To clasify the logs per metric
    """

    metric_thresholds = dict(thresholds[metric])

    edges = [logs_dataframe[metric].min()]
    labels = list()

    for label, edge in metric_thresholds.items():
        edges.append(edge)
        labels.append(label)

    logs_dataframe[f"{metric}_bucket"] = pd.cut(
        select_col(logs_dataframe, metric),
        bins=edges,
        labels=labels,
        include_lowest=True,
    )


if __name__ == "__main__":
    log_dicts = [
        {
            "timestamp": "2026-03-09T23:13:29Z",
            "service": "booking",
            "user": 11,
            "cpu": 35,
            "mem": 49,
            "response_time": 378,
            "level": "INFO",
            "msg": "Seat booked",
        },
        {
            "timestamp": "2026-03-09T23:13:29Z",
            "service": "booking",
            "user": 96,
            "cpu": 38,
            "mem": 72,
            "response_time": 351,
            "level": "INFO",
            "msg": "Booking failed",
        },
        {
            "timestamp": "2026-03-09T23:13:29Z",
            "service": "booking",
            "user": 65,
            "cpu": 57,
            "mem": 40,
            "response_time": 624,
            "level": "WARNING",
            "msg": "Seat booked",
        },
        {
            "timestamp": "2026-03-09T23:13:29Z",
            "service": "booking",
            "user": 35,
            "cpu": 58,
            "mem": 52,
            "response_time": 698,
            "level": "WARNING",
            "msg": "Booking confirmed",
        },
        {
            "timestamp": "2026-03-09T23:13:29Z",
            "service": "booking",
            "user": 60,
            "cpu": 40,
            "mem": 73,
            "response_time": 207,
            "level": "INFO",
            "msg": "Seat booked",
        },
        {
            "timestamp": "2026-03-09T23:13:29Z",
            "service": "booking",
            "user": 60,
            "cpu": 40,
            "mem": 73,
            "response_time": 207,
            "level": "ERROR",
            "msg": "Seat booked",
        },
    ]

    expected_columns = {
        "timestamp": "str",
        "service": "str",
        "user": "int",
        "cpu": "int",
        "mem": "int",
        "response_time": "int",
        "level": "int",
        "msg": "str",
    }

    logs_dataframe = convert_to_dataframe(log_dicts, expected_columns)
