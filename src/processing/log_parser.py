from datetime import datetime
from collections.abc import Iterator
from typing import Any
import logging

logger = logging.getLogger(__name__)


def parse_logs(logs: Iterator[str]) -> list[dict[str, Any]]:
    """Parses the raw logs received from the reader in an understandable format for pandas.

    Args:
        logs: Iterator containing the strings of all log lines.

    Returns:
        All the logs in an easy format to be processed by Pandas in the analysis layer.
    """

    log_dict_list = list()

    for line_number, log in enumerate(logs, start=1):
        before_message, _, message = log.partition(" msg=")
        metrics = before_message.split(" ")
        log_dict = _parse_fields(metrics, line_number)

        if log_dict is not None:
            log_dict["msg"] = message.strip('"\n')
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

        if split_log[1].isdigit():
            log_dict[split_log[0]] = int(split_log[1])
        elif split_log[0] == "timestamp":
            log_dict[split_log[0]] = datetime.fromisoformat(split_log[1])
        else:
            log_dict[split_log[0]] = split_log[1]

    return log_dict


if __name__ == "__main__":
    log = [
        'timestamp=2026-03-08T15:59:49Z service=booking user=80 cpu=65 mem=47 response_time=561 level=INFO msg"Seat booked"\n',
        'timestamp=2026-03-08T15:59:49Z service=booking user=100 cpu=60 mem=41 response_time=85 level=WARNING msg="Seat not booked"\n',
        'timestamp=2026-03-08T15:59:49Z service=booking user=100 cpu=60 mem=41 response_time=85 level=WARNING msg="booking failed"\n',
        'timestamp=2026-03-08T15:59:49Z service=booking user=100 cpu=60 mem=41 response_time=85 level=WARNING msg="booking confirmed"\n',
    ]

    print(parse_logs(log))
