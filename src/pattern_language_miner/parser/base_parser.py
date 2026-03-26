"""Abstract base class for all document parsers."""

from abc import ABC, abstractmethod


class BaseParser(ABC):
    """Define the interface that every concrete parser must implement.

    Subclasses should override :meth:`parse` to convert raw file content
    into a structured dictionary understood by the rest of the pipeline.
    """

    @abstractmethod
    def parse(self, content: str) -> dict:
        """Parse raw document content into a structured representation.

        Args:
            content: The raw text content read from a file.

        Returns:
            A dictionary with at least a ``type`` key identifying the
            parser variant, plus additional payload keys defined by each
            concrete implementation.
        """
