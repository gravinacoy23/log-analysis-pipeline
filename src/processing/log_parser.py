from datetime import datetime
from collections.abc import Iterator
from typing import Any
import logging

logger = logging.getLogger(__name__)


def parse_logs(logs: Iterator[str], expected_cols: list[str]) -> list[dict[str, Any]]:
    """Parses the raw logs received from the reader in an understandable format for pandas.

    Args:
        logs: Iterator containing the strings of all log lines.
        expected_cols: from the config file, all the expected_cols.

    Returns:
        All the logs in an easy format to be processed by Pandas in the analysis layer.
    """

    log_dict_list = list()

    for line_number, log in enumerate(logs, start=1):
        before_message, _, message = log.partition(" msg=")
        metrics = before_message.split(" ")
        parsed_message = message.strip('"\n')

        if not parsed_message:
            logger.warning(f"Missing message at line {line_number}")
            continue

        log_dict = _parse_fields(metrics, line_number)

        if log_dict is not None:
            log_dict["msg"] = parsed_message

            if not _verify_columns(log_dict, expected_cols, line_number):
                continue

            log_dict_list.append(log_dict)

    return log_dict_list


def _parse_fields(
    logs_without_message: list[str], line_number: int
) -> dict[str, Any] | None:
    """Parses the portion of the logs that do not contain the message.

    Args:
        logs_without_message: Partitioned log line prior to the message.
        line_number: Current line number.

    Returns:
        All the lines parsed in a dict.
    """

    log_dict = dict()
    for log in logs_without_message:
        split_log = log.split("=")

        if len(split_log) < 2:
            logger.warning(f"Malformed line skipped at line {line_number}")
            return None
        elif not split_log[1]:
            logger.warning(
                f"Missing {split_log[0]} at line {line_number}, line skipped"
            )
            return None

        if split_log[1].isdigit():
            log_dict[split_log[0]] = int(split_log[1])
        elif split_log[0] == "timestamp":
            log_dict[split_log[0]] = datetime.fromisoformat(split_log[1])
        else:
            log_dict[split_log[0]] = split_log[1]

    return log_dict


def _verify_columns(
    logs_dict: dict[str, Any], expected_cols: list[str], line_number: int
) -> bool:
    """Verifies that a given line in the logs has all the required columns.

    Args:
        logs_dict: contains the key value pairs of the log of the current iteration.
        expected_cols: from the config file, all the expected_cols.
        line_number: current line in log file

    Returns:
        Whether or not we were able to verify that all the expected columns are in the given log.
    """
    for expected in expected_cols:
        if expected not in logs_dict.keys():
            logger.warning(
                f"Missing column {expected} at line {line_number}, line skipped."
            )
            return False

    return True
