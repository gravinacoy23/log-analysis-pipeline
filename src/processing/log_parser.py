from datetime import datetime
from collections.abc import Iterator
from typing import Any
import logging

logger = logging.getLogger(__name__)


def parse_logs(
    logs: Iterator[str], expected_cols: list[str]
) -> tuple[list[dict[str, Any]], dict[str, int | float] | dict[str, int]]:
    """Parses the raw logs received from the reader in an understandable format
    for pandas.

    Args:
        logs: Iterator containing the strings of all log lines.
        expected_cols: from the config file, all the expected_cols.

    Returns:
        All the logs in an easy format to be processed by Pandas in the analysis layer, and three stats: lines processed, lines skipped and skip rate.
    """

    log_dict_list = list()
    skipped_lines = 0

    for line_number, log in enumerate(logs, start=1):
        before_message, _, message = log.partition(" msg=")
        metrics = before_message.split(" ")
        parsed_message = message.strip('"\n')

        if not parsed_message:
            logger.warning(f"Missing message at line {line_number}")
            skipped_lines += 1
            continue

        log_dict = _parse_fields(metrics, line_number)

        if log_dict is None:
            skipped_lines += 1
            continue

        log_dict["msg"] = parsed_message

        if not _verify_columns(log_dict, expected_cols, line_number):
            skipped_lines += 1
            continue

        log_dict_list.append(log_dict)

    log_stats = _skip_report(skipped_lines, len(log_dict_list))

    return log_dict_list, log_stats


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


def _skip_report(
    skipped_lines: int, lines_processed: int
) -> dict[str, int | float] | dict[str, int]:
    """Build and log a report of the processed and skipped lines.
    Args:
        skipped_lines: counter number of skipped lines
        lines_processed: num of lines processed.

    Returns:
        mapped stats.
    """

    log_stats: dict[str, int | float] = {
        "lines_processed": lines_processed,
        "skipped_lines": skipped_lines,
    }

    if skipped_lines == 0 and lines_processed == 0:
        logger.warning("Log file is empty")
        return log_stats

    log_stats["skip_rate"] = (skipped_lines / (skipped_lines + lines_processed)) * 100

    for metric, value in log_stats.items():
        logger.info(f"{metric}: {value}")

    return log_stats
