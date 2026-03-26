"""Plain-text document parser."""

from .base_parser import BaseParser


class TextParser(BaseParser):
    """Parse plain-text files by splitting content into individual lines.

    Example:
        >>> parser = TextParser()
        >>> result = parser.parse("line one\\nline two")
        >>> result["type"]
        'text'
    """

    def parse(self, content: str) -> dict:
        """Split plain text into lines and return a structured payload.

        Args:
            content: The raw plain-text content of a file.

        Returns:
            A dictionary with keys:

            - ``type`` (*str*): Always ``"text"``.
            - ``lines`` (*list[str]*): Non-empty lines from the source.
        """
        return {
            "type": "text",
            "lines": content.strip().splitlines(),
        }
