from abc import ABC, abstractmethod

class BaseParser(ABC):
    @abstractmethod
    def parse(self, content: str) -> dict:
        """Parses raw content and returns a structured representation."""
        pass
