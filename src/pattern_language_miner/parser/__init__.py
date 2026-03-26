"""Parser sub-package.

Provides :class:`BaseParser` and concrete implementations for
text, Markdown, and HTML documents.
"""

from .base_parser import BaseParser
from .html_parser import HTMLParser
from .markdown_parser import MarkdownParser
from .text_parser import TextParser

__all__ = ["BaseParser", "HTMLParser", "MarkdownParser", "TextParser"]
