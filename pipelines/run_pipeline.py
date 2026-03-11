from src.ingestion.log_reader import load_service_logs
from src.processing.log_parser import parse_logs
from src.analysis.log_analysis import convert_to_dataframe


def run_pipeline(service):
    logs_list = load_service_logs(service)
    logs_dict = parse_logs(logs_list)
    logs_dataframe = convert_to_dataframe(logs_dict)

    return logs_dataframe


if __name__ == "__main__":
    print(run_pipeline("booking"))
