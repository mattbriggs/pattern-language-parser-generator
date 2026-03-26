"""Writer sub-package.

Provides :class:`~pattern_language_miner.writer.yaml_writer.YamlWriter`
for serialising patterns to YAML files.
"""

from .yaml_writer import YamlWriter

__all__ = ["YamlWriter"]
