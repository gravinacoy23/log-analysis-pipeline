import pandas as pd
from sklearn.model_selection import train_test_split


def orchestrate_statistics(dataset: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Orchestrates the execution of statistical tasks.

    Args:
        dataset: dataframe with all the feature engineering rows and cols.

    Returns:
        A tuple with the 2 DFs for train and test
    """

    train_data, test_data = _split_dataset(dataset)

    return train_data, test_data


def general_statistics(logs_dataframe: pd.DataFrame) -> pd.DataFrame:
    """Analyze the Dataframe with basic statistical metrics.

    Args:
        logs_dataframe: PD of parsed logs.

    Returns:
        General statistical metrics.
    """

    return logs_dataframe.describe()


def _split_dataset(dataset: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split the dataset in train and test.

    Args:
        dataset: dataframe with all the feature engineering rows and cols.

    Returns:
        a tuple with the 2 DFs for train and test.
    """

    return train_test_split(
        dataset, test_size=0.2, stratify=dataset["is_error"], random_state=42
    )  # pyright: ignore
