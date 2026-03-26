"""Legacy YAML writer in the ``output`` sub-package.

.. deprecated::
    Use :class:`~pattern_language_miner.writer.yaml_writer.YamlWriter` instead.
    This module is retained for backwards compatibility.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict

import yaml

logger = logging.getLogger(__name__)


class YAMLWriter:
    """Write individual pattern dictionaries to YAML files.

    Args:
        output_dir: Directory where YAML files are written.  Created
            automatically if it does not exist.

    .. deprecated::
        Prefer :class:`~pattern_language_miner.writer.yaml_writer.YamlWriter`.

    Example:
        >>> writer = YAMLWriter("./output")
        >>> writer.write_pattern({"id": "P-001"}, "p001.yaml")
    """

    def __init__(self, output_dir: str) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write_pattern(self, pattern: Dict, filename: str) -> None:
        """Serialise *pattern* to *filename* inside :attr:`output_dir`.

        Args:
            pattern: Pattern dictionary to serialise.
            filename: Target filename (without directory path).
        """
        file_path = self.output_dir / filename
        with file_path.open("w", encoding="utf-8") as fh:
            yaml.dump(
                pattern,
                fh,
                allow_unicode=True,
                sort_keys=False,
                default_flow_style=False,
            )
        logger.debug("Wrote %s.", file_path)

    def write_patterns(self, patterns: Dict[str, Dict]) -> None:
        """Write each pattern in *patterns* to its own file.

        Args:
            patterns: Mapping of filename to pattern dictionary.
        """
        for filename, pattern in patterns.items():
            self.write_pattern(pattern, filename)
