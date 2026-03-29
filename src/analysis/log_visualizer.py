import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd


def plot_count_metric(logs_dataframe: pd.DataFrame, metric: str) -> Figure:
    """Plots the count per metric.

    Args:
        logs_dataframe: DF of logs
        metric: Name of the metric to plot

    Returns:
        Figure with the plot count per metric
    """
    figure, ax = plt.subplots()

    sns.countplot(logs_dataframe, x=metric, ax=ax)
    ax.set_title(f"plot count for {metric.capitalize()} metric")
    ax.set_xlabel(metric.capitalize())
    ax.set_ylabel("Occurences")

    return figure


def plot_correlation(corr_matrix: pd.DataFrame) -> Figure:
    """Plots the correlation of a given corr matrix.

    Args:
        corr_matrix: Matrix with the correlation values between all the numeric cols.

    Returns:
        Figure with the heatmap seaborn for correlation.
    """
    figure, ax = plt.subplots()

    sns.heatmap(corr_matrix, ax=ax)
    ax.set_title("Plot correlation of numeric cols")

    return figure


def plot_distribution(logs_dataframe: pd.DataFrame, column_name: str) -> Figure:
    """Plots the distribution of numeric data types.

    Args:
        logs_dataframe: DF of parsed logs
        column_name: Column to plot

    Returns:
        Figure of the distribution
    """
    figure, ax = plt.subplots()

    sns.histplot(logs_dataframe, x=column_name, ax=ax)

    ax.set_title(f"Plot distribution of {column_name}")

    return figure


if __name__ == "__main__":
    log_dicts = [
        {
            "timestamp": "datetime.datetime(2026, 3, 24, 3, 4, 22, tzinfo=datetime.timezone.utc)",
            "service": "booking",
            "user": 24,
            "cpu": 67,
            "mem": 43,
            "response_time": 694,
            "level": "INFO",
            "msg": "Booking confirmed",
        },
        {
            "timestamp": "datetime.datetime(2026, 3, 24, 3, 4, 22, tzinfo=datetime.timezone.utc)",
            "service": "booking",
            "user": 35,
            "cpu": 47,
            "mem": 43,
            "response_time": 226,
            "level": "INFO",
            "msg": "Booking confirmed",
        },
        {
            "timestamp": "datetime.datetime(2026, 3, 24, 3, 4, 22, tzinfo=datetime.timezone.utc)",
            "service": "booking",
            "user": 4,
            "cpu": 43,
            "mem": 46,
            "response_time": 457,
            "level": "INFO",
            "msg": "Booking confirmed",
        },
        {
            "timestamp": "datetime.datetime(2026, 3, 24, 3, 4, 22, tzinfo=datetime.timezone.utc)",
            "service": "booking",
            "user": 98,
            "cpu": 52,
            "mem": 60,
            "response_time": 718,
            "level": "INFO",
            "msg": "Seat booked",
        },
    ]

    logs_dataframe = pd.DataFrame(log_dicts)

    plot_distribution(logs_dataframe, "response_time")

    plt.show()
