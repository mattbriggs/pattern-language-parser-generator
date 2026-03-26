"""Document assembly generator.

Provides :class:`AssemblyGenerator`, which builds structured assembly
instructions from a hierarchy of document-level patterns.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

import yaml

logger = logging.getLogger(__name__)


class AssemblyGenerator:
    """Generate assembly instructions from a pattern hierarchy.

    An *assembly* maps each document-level pattern name to its ordered
    list of sub-pattern IDs plus optional authoring notes.

    Example:
        >>> gen = AssemblyGenerator()
        >>> assembly = gen.generate([
        ...     {"name": "User Guide", "structure": ["intro", "steps"], "notes": ""}
        ... ])
        >>> print(gen.to_yaml(assembly))
    """

    def __init__(self) -> None:
        self.instructions: List[Any] = []

    def generate(
        self, document_patterns: List[Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """Build an assembly map from *document_patterns*.

        Args:
            document_patterns: List of document-level pattern dictionaries.
                Each dict should contain at least ``name`` and ``structure``
                keys.

        Returns:
            A dict mapping each pattern name to a sub-dict with keys
            ``structure`` (list of sub-pattern IDs) and ``notes`` (str).
        """
        assembly_map: Dict[str, Dict[str, Any]] = {}
        for pattern in document_patterns:
            name = pattern.get("name", "unnamed_pattern")
            assembly_map[name] = {
                "structure": pattern.get("structure", []),
                "notes": pattern.get("notes", ""),
            }
        logger.debug("Generated assembly for %d pattern(s).", len(assembly_map))
        return assembly_map

    def to_yaml(self, assembly_map: Dict[str, Dict[str, Any]]) -> str:
        """Serialise *assembly_map* to a YAML-formatted string.

        Args:
            assembly_map: Output of :meth:`generate`.

        Returns:
            A YAML string representation of the assembly.
        """
        return yaml.dump(
            {"document_patterns": assembly_map},
            sort_keys=False,
            default_flow_style=False,
        )
