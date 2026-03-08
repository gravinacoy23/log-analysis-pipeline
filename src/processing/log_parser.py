import logging

logger = logging.getLogger(__name__)


def parse_logs(log_list):
    log_dict_list = list()

    for line_number, log in enumerate(log_list, start=1):
        before_message, _, message = log.partition(" msg=")
        metrics = before_message.split(" ")
        log_dict = _parse_logs_without_message(metrics, line_number)

        if log_dict is not None:
            log_dict["msg"] = message.strip('"')
            log_dict_list.append(log_dict)

    return log_dict_list


def _parse_logs_without_message(logs_without_message, line_number):
    log_dict = dict()
    for log in logs_without_message:
        splitted_log = log.split("=")
        try:
            log_dict[splitted_log[0]] = int(splitted_log[1])
        except IndexError:
            logger.warning(f"Malformed line skipped at line {line_number}")
            return None
        except ValueError:
            log_dict[splitted_log[0]] = splitted_log[1]
    return log_dict


if __name__ == "__main__":
    log = [
        'timestamp=2026-03-08T15:59:49Z service=booking user=80 cpu=65 mem=47 response_time=561 level=INFO msg"Seat booked"',
        'timestamp=2026-03-08T15:59:49Z service=booking user=100 cpu=60 mem=41 response_time85 level=WARNING msg="Seat not booked"',
        'timestamp=2026-03-08T15:59:49Z service=booking user=100 cpu=60 mem=41 response_time85 level=WARNING msg="booking failed"',
        'timestamp=2026-03-08T15:59:49Z service=booking user=100 cpu=60 mem=41 response_time=85 level=WARNING msg="booking confirmed"',
    ]
    print(parse_logs(log))
