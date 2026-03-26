"""Core ``Pattern`` data class.

A :class:`Pattern` represents a single reusable content pattern extracted
from a document corpus.  It maps directly to the JSON Schema defined in
``schema/pattern-schema.json``.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


class Pattern:
    """Represent a reusable content pattern extracted from a document corpus.

    A pattern encapsulates the *context*, *problem*, and *solution* triad
    made popular by Christopher Alexander's Pattern Language, extended with
    provenance and hierarchical relationship metadata.

    Args:
        pattern_id: Unique identifier for the pattern (e.g. ``"P-001"``).
        name: Human-readable short name.
        level: Hierarchical level — one of ``chunk``, ``section``, or
            ``document``.
        context: The situation in which this pattern typically occurs.
        problem: The problem or need that motivates the pattern.
        solution: How the pattern resolves the problem.
        example: A concrete usage example.
        sources: List of provenance records, each a dict with at least a
            ``file`` key.
        subpatterns: IDs of lower-level patterns contained within this one.
        superpattern: ID of the enclosing parent pattern, if any.
        related_patterns: IDs of semantically related patterns.
        info_type: Information type classification (e.g. ``"procedure"``,
            ``"concept"``).
        frequency: Number of times the pattern was observed in the corpus.

    Example:
        >>> p = Pattern("P-001", "Install Software", "chunk",
        ...             "User needs a package", "Package not installed",
        ...             "Run apt-get install", "apt-get install vim",
        ...             [{"file": "guide.md"}])
        >>> p.to_dict()["id"]
        'P-001'
    """

    def __init__(
        self,
        pattern_id: str,
        name: str,
        level: str,
        context: str,
        problem: str,
        solution: str,
        example: str,
        sources: List[Dict[str, str]],
        subpatterns: Optional[List[str]] = None,
        superpattern: Optional[str] = None,
        related_patterns: Optional[List[str]] = None,
        info_type: Optional[str] = None,
        frequency: Optional[int] = None,
    ) -> None:
        self.pattern_id = pattern_id
        self.name = name
        self.level = level
        self.context = context
        self.problem = problem
        self.solution = solution
        self.example = example
        self.sources = sources
        self.subpatterns: List[str] = subpatterns or []
        self.superpattern = superpattern
        self.related_patterns: List[str] = related_patterns or []
        self.info_type = info_type
        self.frequency = frequency

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the pattern to a plain dictionary.

        The returned dict includes a ``$schema`` reference so that YAML
        files written from this object remain self-describing.

        Returns:
            A dictionary suitable for YAML or JSON serialisation.
        """
        return {
            "$schema": "./pattern-schema.json",
            "id": self.pattern_id,
            "name": self.name,
            "level": self.level,
            "context": self.context,
            "problem": self.problem,
            "solution": self.solution,
            "example": self.example,
            "sources": self.sources,
            "subpatterns": self.subpatterns,
            "superpattern": self.superpattern,
            "related_patterns": self.related_patterns,
            "info_type": self.info_type,
            "frequency": self.frequency,
        }

    def __repr__(self) -> str:
        return (
            f"Pattern(id={self.pattern_id!r}, name={self.name!r}, "
            f"level={self.level!r})"
        )
