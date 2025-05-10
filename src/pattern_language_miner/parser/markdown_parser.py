from .base_parser import BaseParser
import markdown
from bs4 import BeautifulSoup


class MarkdownParser(BaseParser):
    def parse(self, content: str) -> dict:
        """
        Parses Markdown content by converting it to HTML and then parsing the HTML.

        Args:
            content (str): The raw Markdown content.

        Returns:
            dict: A dictionary containing the type and parsed HTML content.
        """
        html = markdown.markdown(content)
        soup = BeautifulSoup(html, "html.parser")
        return {
            "type": "markdown",
            "html": str(soup)
        }