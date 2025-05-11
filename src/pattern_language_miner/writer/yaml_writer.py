import os
import re
import logging
import yaml
from pathlib import Path
from typing import List, Dict, Any


class YamlWriter:
    """Writes structured patterns to YAML files in a specified output directory."""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logging.debug(f"Initialized YamlWriter with output dir: {self.output_dir}")

    def sanitize_filename(self, text: str, default: str = "pattern") -> str:
        """Create a safe filename from a string."""
        sanitized = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
        return sanitized if sanitized else default

    def write(self, patterns: List[Dict[str, Any]]) -> None:
        """Write each pattern to a separate YAML file."""
        logging.info(f"📝 Writing {len(patterns)} pattern(s) to {self.output_dir}")

        for i, pattern in enumerate(patterns, start=1):
            title = pattern.get("title") or pattern.get("solution") or ""
            sanitized = self.sanitize_filename(title)
            if not sanitized:
                sanitized = "pattern"

            filename = f"{i:03d}-{sanitized}.yaml"
            path = self.output_dir / filename

            with open(path, "w", encoding="utf-8") as f:
                yaml.safe_dump(pattern, f)

            try:
                with open(path, "w", encoding="utf-8") as file:
                    yaml.safe_dump(pattern, file, sort_keys=False, allow_unicode=True)
                logging.debug(f"✅ Wrote {path}")
            except Exception as e:
                logging.error(f"❌ Failed to write {path}: {e}")
