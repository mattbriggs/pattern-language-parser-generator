"""HTML document parser."""

from bs4 import BeautifulSoup

from .base_parser import BaseParser


class HTMLParser(BaseParser):
    """Parse HTML files using BeautifulSoup and return a normalised payload.

    Example:
        >>> parser = HTMLParser()
        >>> result = parser.parse("<p>Hello</p>")
        >>> result["type"]
        'html'
    """

    def parse(self, content: str) -> dict:
        """Normalise raw HTML content with BeautifulSoup.

        Args:
            content: Raw HTML source text.

        Returns:
            A dictionary with keys:

            - ``type`` (*str*): Always ``"html"``.
            - ``html`` (*str*): The normalised HTML string.
        """
        soup = BeautifulSoup(content, "html.parser")
        return {
            "type": "html",
            "html": str(soup),
        }
