"""YAML pattern file writer.

Provides :class:`YamlWriter`, which serialises a list of pattern
dictionaries to individual, sequentially numbered YAML files with
sanitised filenames.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any, Dict, List

import yaml

logger = logging.getLogger(__name__)

#: Regex matching characters NOT allowed in file names.
_UNSAFE_CHARS = re.compile(r"[^a-zA-Z0-9]+")


class YamlWriter:
    """Write structured pattern dictionaries to YAML files.

    Files are named ``001-<sanitised-title>.yaml``,
    ``002-<sanitised-title>.yaml``, etc.

    Args:
        output_dir: Directory where YAML files are written.  Created
            automatically if it does not exist.

    Example:
        >>> writer = YamlWriter("./output")
        >>> writer.write([{"title": "Install Package", "solution": "..."}])
    """

    def __init__(self, output_dir: str | Path) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("YamlWriter initialised: output_dir=%s", self.output_dir)

    def sanitize_filename(self, text: str, default: str = "pattern") -> str:
        """Derive a safe, lower-case filename stem from *text*.

        Args:
            text: Source string (typically a pattern title or solution).
            default: Fallback stem when *text* reduces to an empty string.

        Returns:
            A filename-safe, lower-case, hyphen-separated string.

        Example:
            >>> writer = YamlWriter("/tmp")
            >>> writer.sanitize_filename("Install the Package!")
            'install-the-package'
        """
        sanitized = _UNSAFE_CHARS.sub("-", text).strip("-").lower()
        return sanitized or default

    def write(self, patterns: List[Dict[str, Any]]) -> None:
        """Serialise each pattern in *patterns* to its own YAML file.

        Args:
            patterns: List of pattern dictionaries to write.
        """
        logger.info(
            "Writing %d pattern(s) to %s.", len(patterns), self.output_dir
        )
        for i, pattern in enumerate(patterns, start=1):
            title = pattern.get("title") or pattern.get("solution") or ""
            stem = self.sanitize_filename(title)
            path = self.output_dir / f"{i:03d}-{stem}.yaml"
            try:
                with path.open("w", encoding="utf-8") as fh:
                    yaml.safe_dump(pattern, fh, sort_keys=False, allow_unicode=True)
                logger.debug("Wrote %s.", path)
            except OSError as exc:
                logger.error("Failed to write %s: %s", path, exc)
