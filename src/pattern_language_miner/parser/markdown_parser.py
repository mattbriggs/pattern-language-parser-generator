"""Markdown document parser."""

import markdown
from bs4 import BeautifulSoup

from .base_parser import BaseParser


class MarkdownParser(BaseParser):
    """Convert Markdown files to an HTML representation via BeautifulSoup.

    The parser converts Markdown syntax to HTML using the ``markdown``
    library, then normalises it with BeautifulSoup before returning the
    result.

    Example:
        >>> parser = MarkdownParser()
        >>> result = parser.parse("# Hello")
        >>> result["type"]
        'markdown'
    """

    def parse(self, content: str) -> dict:
        """Convert Markdown content to a normalised HTML string.

        Args:
            content: Raw Markdown source text.

        Returns:
            A dictionary with keys:

            - ``type`` (*str*): Always ``"markdown"``.
            - ``html`` (*str*): The rendered, normalised HTML string.
        """
        html = markdown.markdown(content)
        soup = BeautifulSoup(html, "html.parser")
        return {
            "type": "markdown",
            "html": str(soup),
        }
