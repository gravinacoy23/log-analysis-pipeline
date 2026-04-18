import argparse
import logging
import pandas as pd
from src.config_loader import load_config
from pipelines.run_pipeline import run_pipeline
from pipelines.run_reporting_pipeline import run_report_pipeline
from pipelines.run_features_pipeline import run_features_pipeline
from pipelines.run_statistical_pipeline import run_statistical_pipeline


def main() -> pd.DataFrame:
    """Orchestrates all the configuration needed for the data pipelines.

    Returns:
        Parsed logs dataframe
    """

    config_data = load_config()

    logs_dataframe = run_pipeline(config_data)
    # Commenting out the following calls to pipeline function as these are
    # currently broken due to the migration to CLF logs.
    run_report_pipeline(logs_dataframe)
    # run_features_pipeline(logs_dataframe, config_data)
    # run_statistical_pipeline()

    return logs_dataframe


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    parser = argparse.ArgumentParser(
        prog="Main file for the log-analysis pipeline",
        description="File with the main funcion that calls pipelines",
    )

    print(main())
