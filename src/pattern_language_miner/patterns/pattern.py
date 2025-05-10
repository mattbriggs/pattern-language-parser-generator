from typing import List, Optional, Dict


class Pattern:
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
        frequency: Optional[int] = None
    ):
        """
        Represents a reusable pattern extracted from documents.

        Args:
            pattern_id (str): Unique identifier for the pattern.
            name (str): Human-readable name of the pattern.
            level (str): Hierarchical level (chunk, section, document, etc.).
            context (str): The situation in which this pattern appears.
            problem (str): The problem this pattern addresses.
            solution (str): How the pattern solves the problem.
            example (str): An example usage of the pattern.
            sources (List[Dict[str, str]]): Locations where the pattern was found.
            subpatterns (List[str], optional): IDs of patterns this one contains.
            superpattern (str, optional): ID of the parent pattern.
            related_patterns (List[str], optional): IDs of semantically related patterns.
            info_type (str, optional): Information type (procedure, concept, etc.).
            frequency (int, optional): Number of times the pattern was detected.
        """
        self.pattern_id = pattern_id
        self.name = name
        self.level = level
        self.context = context
        self.problem = problem
        self.solution = solution
        self.example = example
        self.sources = sources
        self.subpatterns = subpatterns or []
        self.superpattern = superpattern
        self.related_patterns = related_patterns or []
        self.info_type = info_type
        self.frequency = frequency

    def to_dict(self) -> Dict:
        """
        Convert the Pattern object to a dictionary.

        Returns:
            Dict: Dictionary representation of the pattern.
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
            "frequency": self.frequency
        }