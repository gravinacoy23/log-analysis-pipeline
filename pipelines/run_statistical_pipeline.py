from pathlib import Path
import pandas as pd
from src.analysis.log_statistical_analysis import orchestrate_statistics


def run_statistical_pipeline() -> None:
    """Orchestrates the creation and persistence of the training and testing
    data.
    """

    datasets_path = _get_directory()

    features_dataset = _load_features_dataset(datasets_path)
    train_data, test_data = orchestrate_statistics(features_dataset)

    train_data.to_csv(datasets_path / "training_data.csv", index=False)
    test_data.to_csv(datasets_path / "test_data.csv", index=False)


def _get_directory() -> Path:
    """Resolves the directory where the file is located.

    Returns:
        Directory of the file.
    """

    output_path = Path(__file__).resolve().parents[1] / "output" / "datasets"

    if not output_path.is_dir():
        raise ValueError("The output directory does not exist")

    return output_path


def _load_features_dataset(directory: Path) -> pd.DataFrame:
    """Loads the feature engineering dataset.

    Args:
        directory: where the file is located

    Returns:
        Dataframe with the data.
    """

    dataset_file = directory / "features.csv"

    return pd.read_csv(dataset_file)
