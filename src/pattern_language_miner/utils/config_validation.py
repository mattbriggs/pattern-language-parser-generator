import json
import yaml
from pathlib import Path
from jsonschema import validate, ValidationError


def load_and_validate_config(config_path: Path, schema_path: Path) -> dict:
    """
    Load a YAML config file and validate it against a JSON Schema.

    Args:
        config_path: Path to the YAML config file.
        schema_path: Path to the JSON Schema file.

    Returns:
        dict: Parsed and validated configuration data.

    Raises:
        FileNotFoundError: If the config or schema file does not exist.
        ValidationError: If the config does not conform to the schema.
    """
    if not config_path.exists():
        raise FileNotFoundError(f"❌ Config file not found: {config_path}")

    if not schema_path.exists():
        raise FileNotFoundError(f"❌ Schema file not found: {schema_path}")

    with config_path.open("r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)

    with schema_path.open("r", encoding="utf-8") as f:
        schema = json.load(f)

    try:
        validate(instance=config_data, schema=schema)
    except ValidationError as e:
        raise ValidationError(f"❌ Config validation error: {e.message}")

    return config_data