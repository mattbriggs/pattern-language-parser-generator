import pytest
from pattern_language_miner.parser.text_parser import TextParser
from pattern_language_miner.parser.markdown_parser import MarkdownParser
from pattern_language_miner.parser.html_parser import HTMLParser


def test_text_parser():
    parser = TextParser()
    content = "First line.\nSecond line.\nThird line."
    result = parser.parse(content)

    assert isinstance(result, dict)
    assert result["type"] == "text"
    assert result["lines"] == ["First line.", "Second line.", "Third line."]


def test_markdown_parser():
    parser = MarkdownParser()
    content = "# Heading\n\nThis is a paragraph with **bold** text."
    result = parser.parse(content)

    assert isinstance(result, dict)
    assert result["type"] == "markdown"
    assert "<h1>" in result["html"]
    assert "This is a paragraph" in result["html"]


def test_html_parser():
    parser = HTMLParser()
    content = "<html><body><h1>Title</h1><p>Paragraph</p></body></html>"
    result = parser.parse(content)

    assert isinstance(result, dict)
    assert result["type"] == "html"
    assert "<h1>Title</h1>" in result["html"]
    assert "<p>Paragraph</p>" in result["html"]