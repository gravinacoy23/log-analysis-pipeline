from src.analysis.log_visualizer import (
    plot_count_metric,
    plot_correlation,
    plot_distribution,
)

from src.analysis.log_analysis import convert_corr_matrix
from pathlib import Path
import pandas as pd
from matplotlib.figure import Figure


def report_pipeline(logs_dataframe: pd.DataFrame) -> None:
    """Run the pipeline to generate reports and visualizations and save them to the output dir.

    Args:
        logs_dataframe: Df of parsed logs.
    """

    plot_dir = _make_output_directory()

    plot_dict = dict()

    plot_dict.update(_count_report(logs_dataframe, "level"))
    plot_dict.update(_count_report(logs_dataframe, "service"))
    plot_dict.update(_corr_report(logs_dataframe))
    plot_dict.update(_dist_report(logs_dataframe, "response_time"))

    for file_name, plot in plot_dict.items():
        file_name = plot_dir / file_name

        plot.savefig(file_name)


def _make_output_directory() -> Path:
    """Makes the directory to save the outputs.

    Returns:
        Path object with the directory.
    """

    parent_path = Path(__file__).resolve().parents[1]
    plot_dir = parent_path / "output" / "plots"
    plot_dir.mkdir(parents=True, exist_ok=True)

    return plot_dir


def _count_report(logs_dataframe: pd.DataFrame, metric_name: str) -> dict[str, Figure]:
    """sub report to create a plot that counts the occurences of a given metric.

    Args:
        logs_dataframe: DF of parsed logs
        metric_name: Metric to plot

    Returns:
        A dict that contains the name of the file and the Figure object.
    """

    file_name = f"{metric_name}_count_plot.png"
    count_plot = plot_count_metric(logs_dataframe, metric_name)

    return {file_name: count_plot}


def _corr_report(logs_dataframe: pd.DataFrame) -> dict[str, Figure]:
    """sub report to create a plot that correlates all the numeric columns.

    Args:
        logs_dataframe: DF of parsed logs

    Returns:
        A dict that contains the name of the file and the Figure object.
    """

    file_name = "correlation_plot.png"
    corr_plot = plot_correlation(convert_corr_matrix(logs_dataframe))

    return {file_name: corr_plot}


def _dist_report(logs_dataframe: pd.DataFrame, metric_name: str) -> dict[str, Figure]:
    """sub report to create a plot that distributes a given metric.

    Args:
        logs_dataframe: DF of parsed logs
        metric_name: Metric to plot

    Returns:
        A dict that contains the name of the file and the Figure object.
    """

    file_name = "distribution_report.png"
    dist_plot = plot_distribution(logs_dataframe, metric_name)

    return {file_name: dist_plot}
