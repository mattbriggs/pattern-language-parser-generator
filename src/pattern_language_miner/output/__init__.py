"""Output sub-package (legacy).

Contains :class:`~pattern_language_miner.output.yaml_writer.YAMLWriter` and
:class:`~pattern_language_miner.output.assembly_generator.AssemblyGenerator`.

.. deprecated::
    For YAML output prefer :class:`~pattern_language_miner.writer.yaml_writer.YamlWriter`.
"""

from .assembly_generator import AssemblyGenerator
from .yaml_writer import YAMLWriter

__all__ = ["AssemblyGenerator", "YAMLWriter"]
