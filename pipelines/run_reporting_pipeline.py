from src.analysis.log_visualizer import plot_metric
from src.analysis.log_analysis import count_by_level_all
from pathlib import Path


def make_output_directory():
    parent_path = Path(__file__).resolve().parents[1]
    plot_dir = parent_path / "output" / "plots"
    plot_dir.mkdir(parents=True, exist_ok=True)

    return plot_dir


def report_level_pipeline(logs_dataframe):
    plot_dir = make_output_directory()
    plot_file = plot_dir / "level_plot.png"
    metric_dict = count_by_level_all(logs_dataframe).to_dict()

    figure = plot_metric(metric_dict, "level")

    figure.savefig(plot_file)
