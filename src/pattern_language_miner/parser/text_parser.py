from .base_parser import BaseParser


class TextParser(BaseParser):
    def parse(self, content: str) -> dict:
        """
        Parses plain text content by splitting it into lines.

        Args:
            content (str): The raw plain text content.

        Returns:
            dict: A dictionary containing the type and a list of text lines.
        """
        return {
            "type": "text",
            "lines": content.strip().splitlines()
        }