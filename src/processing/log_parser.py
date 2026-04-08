from datetime import datetime
from collections.abc import Iterator
from typing import Any
import logging
import re

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
    log_pattern = re.compile(r"(\S+) (\S+) (\S+) \[(.+?)\] \"(.+?)\" (\d+) (\S+)")

    for line_number, log in enumerate(logs, start=1):
        split_log = log_pattern.match(log)

        if split_log is None:
            logger.warning(f"No match found for line {line_number}, line skipped")
            skipped_lines += 1
            continue

        log_dict = _parse_fields(split_log.groups(), line_number, expected_cols)

        if log_dict is None:
            skipped_lines += 1
            continue

        if not _verify_columns(log_dict, expected_cols, line_number):
            skipped_lines += 1
            continue

        log_dict_list.append(log_dict)

    log_stats = _skip_report(skipped_lines, len(log_dict_list))

    return log_dict_list, log_stats


def _parse_fields(
    split_log_line: tuple[str | Any, ...], line_number: int, expected_columns
) -> dict[str, Any] | None:
    """Parses all the fields of the log line.

    Args:
        split_log_line: Log line constructed with the match of the regex.
        line_number: Current line number.
        expected_columns: Defined in the config file for validation.

    Returns:
        Line parsed in a dict mapped to each value to corresponding column name.
    """

    log_dict = dict()
    new_split_line = _parse_request_line(split_log_line)

    for item, col_title in zip(new_split_line, expected_columns):
        if not item and col_title != "protocol_version":
            logger.warning(f"Missing value for {col_title} at line {line_number}")
            return None

        if col_title == "response_size":
            if item.isdigit():
                log_dict[col_title] = int(item)
            elif item == "-":
                log_dict[col_title] = 0
            else:
                logger.warning(f"Malformed line skipped at line {line_number}")
                return None
        elif col_title == "http_response":
            if item.isdigit():
                log_dict[col_title] = int(item)
            else:
                logger.warning(f"Malformed line skipped at line {line_number}")
                return None

        elif col_title == "timestamp":
            log_dict[col_title] = datetime.strptime(item, "%d/%b/%Y:%H:%M:%S %z")
        else:
            log_dict[col_title] = item

    return log_dict


def _parse_request_line(split_log_line: tuple[str | Any, ...]) -> tuple[str]:
    """Parses the request line dividing into the 3 corresponding sub-fields.

    Args:
        split_log_line: Log line constructed with the match of the regex

    Returns:
        Cleaned log line with all the expected fields.
    """

    request_line = split_log_line[4].split(" ")
    request_line_clean = [item for item in request_line if item.strip()]

    if len(request_line_clean) < 3:
        request_line_clean.append(None)
    elif len(request_line_clean) >= 3:
        if request_line_clean[-1].startswith("HTTP/"):
            request_line_clean = [
                request_line_clean[0],
                "".join(request_line_clean[1:-1]),
                request_line_clean[-1],
            ]
        else:
            request_line_clean = [
                request_line_clean[0],
                "".join(request_line_clean[1:]),
                None,
            ]

    return (
        *split_log_line[:4],
        *(request_line_clean),
        *split_log_line[5:],
    )  # pyright: ignore


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
