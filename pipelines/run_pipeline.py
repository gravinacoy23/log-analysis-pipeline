from src.config_loader import load_config
from src.ingestion.log_reader import load_service_logs
from src.processing.log_parser import parse_logs
from src.analysis.log_analysis import convert_to_dataframe


def run_pipeline(service):
    raw_data = load_config()
    raw_logs = load_service_logs(service)
    parsed_logs = parse_logs(raw_logs)
    logs_dataframe = convert_to_dataframe(parsed_logs, raw_data["columns"])

    return logs_dataframe


if __name__ == "__main__":
    print(run_pipeline("booking"))
