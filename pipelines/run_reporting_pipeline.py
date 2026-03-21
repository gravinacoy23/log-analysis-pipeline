from src.analysis.log_visualizer import plot_count_metric
from pathlib import Path
import pandas as pd


def _make_output_directory() -> Path:
    """Makes the directory to save the outputs.

    Returns:
        Path object with the directory.
    """

    parent_path = Path(__file__).resolve().parents[1]
    plot_dir = parent_path / "output" / "plots"
    plot_dir.mkdir(parents=True, exist_ok=True)

    return plot_dir


def report_level_pipeline(logs_dataframe: pd.DataFrame) -> None:
    """Run the pipeline to generate reports and visualizations and save them to the output dir.

    Args:
        logs_dataframe: Df of parsed logs.
    """

    plot_dir = _make_output_directory()
    plot_file = plot_dir / "level_plot.png"

    count_plot = plot_count_metric(logs_dataframe, "level")

    count_plot.savefig(plot_file)
