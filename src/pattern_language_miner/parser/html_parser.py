from .base_parser import BaseParser
from bs4 import BeautifulSoup


class HTMLParser(BaseParser):
    def parse(self, content: str) -> dict:
        """
        Parses HTML content using BeautifulSoup and returns a structured representation.

        Args:
            content (str): The raw HTML content.

        Returns:
            dict: A dictionary containing the type and parsed HTML content.
        """
        soup = BeautifulSoup(content, "html.parser")
        return {
            "type": "html",
            "html": str(soup)
        }