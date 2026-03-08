import pytest
import unittest
from unittest.mock import patch, mock_open, MagicMock
from src.ingestion.log_reader import load_service_logs


def test_load_service_logs_returns_list():
    mock_file = MagicMock()
    mock_file.is_file.return_value = True
    mock_content = '2026-03-07T15:46:20Z service=booking user=1 cpu=54 mem=68 response_time=652 level=INFO msg="Booking confirmed"'

    with patch("src.ingestion.log_reader.Path.is_dir", return_value=True):
        with patch("src.ingestion.log_reader.Path.iterdir", return_value=[mock_file]):
            with patch("builtins.open", mock_open(read_data=mock_content)):
                with patch("builtins.readlines", return_value=[mock_file]):
                    result = load_service_logs("booking")
                    assert type(result) == list, "not a list"
                    assert len(result) > 0, "List is empty"
