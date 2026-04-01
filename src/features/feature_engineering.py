import pandas as pd


def orchestrate_features(
    logs_dataframe: pd.DataFrame, thresholds: dict[str, int], services: list[str]
) -> pd.DataFrame:
    """Orchestrates the different auxiliary functions to generate the feature
    engineering dataset.

    Args:
        logs_dataframe: DF of parsed logs.
        thresholds: has the different thresholds defined in the config file for the feature engineering.
        services: All available services.

    Returns:
        A dataframe with the feature engineering a context cols.
    """

    features_list = list()
    context_cols = ["timestamp", "service", "user"]

    features_list.append(_context_cols(logs_dataframe, context_cols))
    features_list.append(_service_encoded(logs_dataframe, services))
    features_list.append(_hour_of_day(logs_dataframe))
    features_list.append(_is_error(logs_dataframe))
    features_list.append(_is_slow(logs_dataframe, thresholds["high_rt"]))
    features_list.append(_cpu_mem_ratio(logs_dataframe))

    return pd.concat(features_list, axis=1)


def _context_cols(logs_dataframe: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Retrieves some context columns for the feature engineering dataset.

    Args:
        logs_dataframe: DF of parsed logs.
        cols: context cols predefined in the orchestrator function

    Returns:
        Df with the context cols.
    """

    return logs_dataframe[cols]  # type: ignore


def _is_error(logs_dataframe: pd.DataFrame) -> pd.Series:
    """Creates a series of bool values whether the level of the row is ERROR.

    Args:
        logs_dataframe: DF of parsed logs.
    Returns:
        Series with the bool of whether the row has level error.
    """

    return (logs_dataframe["level"] == "ERROR").rename("is_error")


def _is_slow(logs_dataframe: pd.DataFrame, rt_threshold: int) -> pd.Series:
    """Creates a series of bool values whether the rt is high, depending on the
    predefined threshold.

    Args:
        logs_dataframe: DF of parsed logs
        rt_threshold: predefined threshold of high response time.

    Returns:
        Series with the bool of whether the row has high rt.
    """

    return (logs_dataframe["response_time"] >= rt_threshold).rename("is_slow")


def _hour_of_day(logs_dataframe: pd.DataFrame) -> pd.Series:
    """Extracts the hr of the day in which the transaction happened.

    Args:
        logs_dataframe: DF of parser logs

    Returns:
        hour of the day of each row
    """

    return logs_dataframe["timestamp"].dt.hour.rename("hour_of_day")


def _service_encoded(logs_dataframe: pd.DataFrame, services: list[str]) -> pd.Series:
    """Encodes the name of the service so it's easier to process down the line.

    Args:
        logs_dataframe: DF of parsed logs.
        services: Available services.

    Returns:
        Encoded series of services.
    """

    services_map = dict()

    for index, service in enumerate(services, start=1):
        services_map[service] = index

    return logs_dataframe["service"].map(services_map).rename("service_encoded")  # type: ignore


def _cpu_mem_ratio(logs_dataframe: pd.DataFrame) -> pd.Series:
    """Calculates de ratio of CPU to memory.

    Args:
        logs_dataframe: DF of parsed logs.

    Returns:
        series with the ratio of CPU to mem.
    """

    return (logs_dataframe["cpu"] / logs_dataframe["mem"]).rename("cpu_mem_ratio")
