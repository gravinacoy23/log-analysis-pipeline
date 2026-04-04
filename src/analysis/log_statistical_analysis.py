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


def create_confusion_matrix(
    results: list[bool], predictions: list[bool]
) -> tuple[int, int, int, int]:
    """Creates the confusion matrix given a list of results and predictions.

    Args:
        results: real results of the target value
        predictions: predictions of the model

    Returns:
        Tuple with the values of TP, TN, FP, FN.
    """

    true_positive = true_negative = false_positive = false_negative = 0
    for result, prediction in zip(results, predictions):
        if not isinstance(result, bool) or not isinstance(prediction, bool):
            continue

        if prediction:
            if result:
                true_positive += 1
            else:
                false_positive += 1
        else:
            if not result:
                true_negative += 1
            else:
                false_negative += 1

    return true_positive, true_negative, false_positive, false_negative


if __name__ == "__main__":
    results = [True, False, True, False, True]
    predictions = [True, False, 0, False, True]

    print(create_confusion_matrix(results, predictions))
