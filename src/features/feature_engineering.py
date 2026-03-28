import pandas as pd


def orchestrate_features(
    logs_dataframe: pd.DataFrame, thresholds: dict[str, int]
) -> pd.DataFrame:
    """Orchestrates the different auxiliary functions to generate the feature engineering dataset

    Args:
        logs_dataframe: DF of parsed logs.
        thresholds: has the different thresholds defined in the config file for the feature engineering.

    Returns:
        A dataframe with the feature engineering cols only.
    """

    features_list = list()
    context_cols = ["timestamp", "service", "user"]

    features_list.append(_context_cols(logs_dataframe, context_cols))
    features_list.append(_is_error(logs_dataframe))
    features_list.append(_is_slow(logs_dataframe, thresholds["high_rt"]))

    return pd.concat(features_list, axis=1)


def _context_cols(
    logs_dataframe: pd.DataFrame, cols: list[str]
) -> pd.DataFrame | pd.Series:
    """Retrieves some context columns for the feature engineering dataset

    Args:
        logs_dataframe: DF of parsed logs.
        cols: context cols predefined in the orchestrator function

    Returns:
        Depending on the ammount of cols a series or a df with the context cols.
    """

    return logs_dataframe[cols]


def _is_error(logs_dataframe: pd.DataFrame) -> pd.Series:
    """Creates a series of bool values whether the level of the row is ERROR

    Args:
        logs_dataframe: DF of parsed logs.
    Returns:
        Series with the bool of whether the row has level error.
    """

    return (logs_dataframe["level"] == "ERROR").rename("is_error")


def _is_slow(logs_dataframe: pd.DataFrame, rt_threshold: int) -> pd.Series:
    """Creates a series of bool values whether the rt is high, depending on the predefined threshold.

    Args:
        logs_dataframe: DF of parsed logs
        rt_threshold: predefined threshold of high response time.

    Returns:
        Series with the bool of whether the row has high rt.
    """

    return (logs_dataframe["response_time"] >= rt_threshold).rename("is_slow")
