"""Unit tests for the parser sub-package."""

from __future__ import annotations

import pytest

from pattern_language_miner.parser.base_parser import BaseParser
from pattern_language_miner.parser.html_parser import HTMLParser
from pattern_language_miner.parser.markdown_parser import MarkdownParser
from pattern_language_miner.parser.text_parser import TextParser
from pattern_language_miner.walker import ParserFactory


# ---------------------------------------------------------------------------
# TextParser
# ---------------------------------------------------------------------------


class TestTextParser:
    def test_returns_dict(self):
        parser = TextParser()
        result = parser.parse("hello\nworld")
        assert isinstance(result, dict)

    def test_type_key(self):
        assert TextParser().parse("x")["type"] == "text"

    def test_splits_lines(self):
        result = TextParser().parse("First line.\nSecond line.\nThird line.")
        assert result["lines"] == ["First line.", "Second line.", "Third line."]

    def test_strips_leading_trailing_whitespace(self):
        result = TextParser().parse("  hello  \n  world  ")
        assert result["lines"][0] == "  hello  "

    def test_empty_content(self):
        result = TextParser().parse("")
        assert result["lines"] == []

    def test_is_base_parser_subclass(self):
        assert isinstance(TextParser(), BaseParser)


# ---------------------------------------------------------------------------
# MarkdownParser
# ---------------------------------------------------------------------------


class TestMarkdownParser:
    def test_returns_dict(self):
        result = MarkdownParser().parse("# Hello")
        assert isinstance(result, dict)

    def test_type_key(self):
        assert MarkdownParser().parse("# Hello")["type"] == "markdown"

    def test_heading_rendered(self):
        result = MarkdownParser().parse("# Heading\n\nParagraph text.")
        assert "<h1>" in result["html"]
        assert "Paragraph text." in result["html"]

    def test_bold_rendered(self):
        result = MarkdownParser().parse("**bold**")
        assert "<strong>bold</strong>" in result["html"]

    def test_empty_content(self):
        result = MarkdownParser().parse("")
        assert result["html"] == ""

    def test_is_base_parser_subclass(self):
        assert isinstance(MarkdownParser(), BaseParser)


# ---------------------------------------------------------------------------
# HTMLParser
# ---------------------------------------------------------------------------


class TestHTMLParser:
    def test_returns_dict(self):
        result = HTMLParser().parse("<p>Hello</p>")
        assert isinstance(result, dict)

    def test_type_key(self):
        assert HTMLParser().parse("<p>x</p>")["type"] == "html"

    def test_preserves_structure(self):
        content = "<html><body><h1>Title</h1><p>Para</p></body></html>"
        result = HTMLParser().parse(content)
        assert "<h1>Title</h1>" in result["html"]
        assert "<p>Para</p>" in result["html"]

    def test_empty_content(self):
        result = HTMLParser().parse("")
        assert result["html"] == ""

    def test_is_base_parser_subclass(self):
        assert isinstance(HTMLParser(), BaseParser)


# ---------------------------------------------------------------------------
# ParserFactory
# ---------------------------------------------------------------------------


class TestParserFactory:
    @pytest.mark.parametrize("ext", [".md", ".markdown"])
    def test_returns_markdown_parser(self, ext):
        assert isinstance(ParserFactory.get_parser(ext), MarkdownParser)

    @pytest.mark.parametrize("ext", [".html", ".htm"])
    def test_returns_html_parser(self, ext):
        assert isinstance(ParserFactory.get_parser(ext), HTMLParser)

    def test_returns_text_parser(self):
        assert isinstance(ParserFactory.get_parser(".txt"), TextParser)

    def test_raises_on_unsupported_extension(self):
        with pytest.raises(ValueError, match="Unsupported"):
            ParserFactory.get_parser(".pdf")

    def test_case_insensitive(self):
        assert isinstance(ParserFactory.get_parser(".MD"), MarkdownParser)
