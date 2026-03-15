from pathlib import Path
from typing import Any
import yaml


def load_config() -> dict[str, Any]:
    """Loads all the config in the config.yaml

    Returns:
        All the config loaded in a dict

    Raises:
        ValueError: When the columns do not exist in the config file
    """
    parent_path = Path(__file__).resolve().parents[1]
    config_file = parent_path / "config" / "config.yaml"

    with config_file.open("r") as f:
        data = yaml.safe_load(f)

        if not data.get("columns"):
            raise ValueError("Your columns do not exist in the config file.")

        return data


if __name__ == "__main__":
    print(load_config())
