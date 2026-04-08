from pathlib import Path
from typing import Any
import yaml


def load_config() -> dict[str, Any]:
    """Loads all the config in the config.yaml.

    Returns:
        All the config loaded in a dict

    Raises:
        ValueError: When one of the required keys is missing in the config file.
    """
    parent_path = Path(__file__).resolve().parents[1]
    config_file = parent_path / "config" / "config.yaml"

    required_keys = [
        "paths",
        "columns",
        "expected_values",
    ]

    with config_file.open("r") as f:
        data = yaml.safe_load(f)

        for key in required_keys:
            if not data.get(key):
                raise ValueError(
                    f"the required key {key} does not exist in the config file."
                )

        return data


if __name__ == "__main__":
    print(load_config())
