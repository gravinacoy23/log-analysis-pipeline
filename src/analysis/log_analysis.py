from typing import Any
from collections.abc import KeysView
import pandas as pd
import logging


logger = logging.getLogger(__name__)


def convert_to_dataframe(
    log_dicts: list[dict[str, Any]],
    expected_columns: dict[str, str],
    expected_values: dict[str, list[str]],
) -> pd.DataFrame:
    """Converts the list of parsed logs into a dataframe.

    Args:
        log_dicts: Parsed logs.
        expected_columns: All the required columns loaded from the config file.
        expected_values: dict that maps a set of columns to their expected values, ie level.

    Returns:
        Logs in a pd.dataframe object.
    """

    verified_log_dicts = _validation_orchestrator(
        log_dicts, expected_columns, expected_values
    )

    logs_dataframe = pd.DataFrame(verified_log_dicts)

    return logs_dataframe


def _validation_orchestrator(
    log_dicts: list[dict[str, Any]],
    expected_columns: dict[str, str],
    expected_values: dict[str, list[str]],
) -> list[dict[str, Any]]:
    """Orchestrates the validation of the log dicts before converting to
    Dataframe.

    Args:
        log_dicts: Parsed logs
        expected_columns: All the required columns loaded from the config file.
        expected_values: dict that maps a set of columns to their expected values, ie level.

    Returns:
        List of dicts with all the verified logs, dropping the lines with incorrect values or data types for int.
    """

    _verify_columns(log_dicts, expected_columns.keys())

    col_dtypes = list()
    verified_log_dicts = list()

    for col, data_type in expected_columns.items():
        if data_type == "int":
            col_dtypes.append(col)

    for line_number, log in enumerate(log_dicts, start=1):
        line_verified = _verify_col_dtype(log, col_dtypes, line_number)

        if not line_verified:
            continue

        line_verified = _verify_col_values(log, expected_values, line_number)

        if line_verified:
            verified_log_dicts.append(log)

    return verified_log_dicts


def _verify_columns(
    log_dicts: list[dict[str, Any]], expected_columns: KeysView[str]
) -> None:
    """Verifies that the parsed logs are not empty and contain the required
    columns.

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
    log_line: dict[str, Any], expected_dtypes: list[str], line_number: int
) -> bool:
    """Verify all the cols have the correct data type, for now only verifies
    INT dtype cols.

    Args:
        log_line: Dictionary containing 1 log line from the dataset
        expected_dtypes: List with the expected dtypes per col, for now it's only a list that has all the cols that are supposed to be a number.
        line_number: current line in the iteration.

    Returns:
        Whether or not the current line was verified: true/false.
    """

    for int_col in expected_dtypes:
        if not isinstance(log_line[int_col], int):
            logger.warning(
                f"The column {int_col} does not contain int data type at line {line_number}"
            )
            return False

    return True


def _verify_col_values(
    log_line: dict[str, Any], expected_values: dict[str, list[str]], line_number: int
) -> bool:
    """Verifies that the given columns had the corresponding expected values.

    Args:
        log_line: Dictionary containing 1 log line from the dataset.
        expected_values: contains a mapping of given columns to the possible values.
        line_number: current line in the iteration

    Returns:
        Whether or not the current line passed verification.
    """

    for column in expected_values.keys():
        if column == "http_response":
            if not _verify_response_field(
                log_line["http_response"], expected_values["http_response"], line_number
            ):
                return False
        elif column == "protocol_version" and log_line[column] is None:
            continue
        elif log_line[column] not in expected_values[column]:
            logger.warning(
                f"The column {column}, contains an unexpected value: {log_line[column]} at line {line_number}"
            )
            return False

    return True


def _verify_response_field(value, value_range, line_number):
    if value not in range(value_range[0], value_range[1]):
        logger.warning(
            f"The column http_response, contains an unexpected value {value} at line {line_number}"
        )
        return False
    return True


def convert_corr_matrix(logs_dataframe: pd.DataFrame) -> pd.DataFrame:
    """Converts the numeric type cols to a correlation matrix.

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


def get_metric_thresholds(
    logs_dataframe: pd.DataFrame,
    metric: str,
    thresholds: dict[str, dict[str, list[int]]],
) -> None:
    """Adds a column that based on predefined thresholds assigns a value of the
    status of the given metric.

    Args:
        logs_dataframe: DF of parsed logs.
        metric: name of the metric
        thresholds: To classify the logs per metric
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
