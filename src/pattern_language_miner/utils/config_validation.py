"""YAML configuration loading and JSON Schema validation."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import yaml
from jsonschema import ValidationError, validate

logger = logging.getLogger(__name__)


def load_and_validate_config(config_path: Path, schema_path: Path) -> dict:
    """Load a YAML configuration file and validate it against a JSON Schema.

    Args:
        config_path: Path to the YAML configuration file.
        schema_path: Path to the JSON Schema (``*.json``) file.

    Returns:
        The parsed configuration as a plain Python dictionary.

    Raises:
        FileNotFoundError: If *config_path* or *schema_path* do not exist.
        ValidationError: If the configuration does not satisfy the schema.

    Example:
        >>> cfg = load_and_validate_config(
        ...     Path("config.yaml"), Path("schema/config_schema.json")
        ... )
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    with config_path.open("r", encoding="utf-8") as fh:
        config_data = yaml.safe_load(fh)

    with schema_path.open("r", encoding="utf-8") as fh:
        schema = json.load(fh)

    try:
        validate(instance=config_data, schema=schema)
    except ValidationError as exc:
        raise ValidationError(f"Config validation error: {exc.message}") from exc

    logger.debug("Configuration loaded and validated from %s", config_path)
    return config_data
