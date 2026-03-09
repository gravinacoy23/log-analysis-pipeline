from src.ingestion.log_reader import load_service_logs
from src.processing.log_parser import parse_logs


def run_pipeline(service):
    logs_list = load_service_logs(service)
    logs_dict = parse_logs(logs_list)

    return logs_dict


if __name__ == "__main__":
    print(run_pipeline("booking"))
