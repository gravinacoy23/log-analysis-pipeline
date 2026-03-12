import pandas as pd


def convert_to_dataframe(log_dicts):
    logs_dataframe = pd.DataFrame(log_dicts)

    return logs_dataframe


def filter_loglevel(logs_dataframe, level):
    return logs_dataframe.loc[logs_dataframe["level"] == level]


def select_col(logs_dataframe, column_name):
    return logs_dataframe[column_name]


def count_by_level(logs_dataframe, level):
    return (logs_dataframe["level"] == level).sum()


def count_by_level_all(logs_dataframe):
    return logs_dataframe.value_counts("level")


def count_by_service(logs_dataframe, service):
    return (logs_dataframe["service"] == service).sum()


def count_by_service_all(logs_dataframe):
    return logs_dataframe.value_counts("service")


def mean_rt_by_service(logs_dataframe):
    return logs_dataframe.groupby("service")["response_time"].mean()


def mean_cpu_by_level(logs_dataframe):
    return logs_dataframe.groupby("level")["cpu"].mean()


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
    logs_dataframe = convert_to_dataframe(log_dicts)

    # print(logs_dataframe.describe())
    print(logs_dataframe)
    print(count_by_level_all(logs_dataframe).to_dict())
    # print(mean_cpu_by_level(logs_dataframe))
